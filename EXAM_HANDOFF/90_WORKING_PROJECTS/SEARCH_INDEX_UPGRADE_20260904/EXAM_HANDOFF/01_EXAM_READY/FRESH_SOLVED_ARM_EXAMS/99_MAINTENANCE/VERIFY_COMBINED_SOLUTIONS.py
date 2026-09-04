"""Verify that every canonical exam answer matches the sole Combined API."""

from __future__ import annotations

import re
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SOLUTIONS = (
    PACKAGE
    / "03_COPY_PASTE_LIBRARY"
    / "CANONICAL_WORKSTATION"
    / "exam-solutions"
)
API_HEADER = (
    PACKAGE.parent
    / "02_STARTING_TEMPLATES"
    / "Official Combined Exam API"
    / "Source"
    / "exam_api"
    / "exam_api.h"
)

EXPECTED_QUESTIONS = 48
EXPECTED_C_FILES = 21
EXPECTED_ASSEMBLY_FILES = 28

BANNED_TOKENS = (
    "button_callback_t",
    "exam_button_event_t",
    "EXAM_PRESS",
    "joystick_callback_t",
    "rit_scheduler_start",
    "timer_configure_match",
    "timer_every_ms",
    "timer_match_occurred",
    "timer_read_counter",
    "timer_set_clock_divider",
    "timer_set_prescaler",
    "potentiometer_read",
    "JOYSTICK_SELECT",
    "JOYSTICK_UP",
    "JOYSTICK_DOWN",
    "JOYSTICK_LEFT",
    "JOYSTICK_RIGHT",
)


def names(pattern: str, text: str) -> set[str]:
    return set(re.findall(pattern, text, flags=re.MULTILINE))


def main() -> int:
    issues: list[str] = []
    question_dirs = sorted(path for path in SOLUTIONS.iterdir() if path.is_dir())
    c_files = sorted(SOLUTIONS.glob("*/main.c"))
    assembly_files = sorted(SOLUTIONS.glob("*/assembly.s"))

    if len(question_dirs) != EXPECTED_QUESTIONS:
        issues.append(
            f"expected {EXPECTED_QUESTIONS} question directories, found "
            f"{len(question_dirs)}"
        )
    if len(c_files) != EXPECTED_C_FILES:
        issues.append(f"expected {EXPECTED_C_FILES} C files, found {len(c_files)}")
    if len(assembly_files) != EXPECTED_ASSEMBLY_FILES:
        issues.append(
            f"expected {EXPECTED_ASSEMBLY_FILES} assembly files, found "
            f"{len(assembly_files)}"
        )

    for directory in question_dirs:
        if not any((directory / name).is_file() for name in ("main.c", "assembly.s")):
            issues.append(f"{directory.name}: no main.c or assembly.s")

    header_text = API_HEADER.read_text(encoding="utf-8")
    declared_api = names(r"\b(exam_[A-Za-z0-9_]+)\s*\(", header_text)
    if len(declared_api) != 52:
        issues.append(
            f"canonical header declares {len(declared_api)} exam_ calls, expected 52"
        )

    all_assembly = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in assembly_files
    )
    assembly_exports = names(
        r"^\s*(?:EXPORT|GLOBAL)\s+([A-Za-z_][A-Za-z0-9_]*)",
        all_assembly,
    )

    used_api: set[str] = set()
    for path in c_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        label = path.relative_to(SOLUTIONS).as_posix()
        used_api.update(names(r"\b(exam_[A-Za-z0-9_]+)\s*\(", text))

        if text.count('#include "exam_api.h"') != 1:
            issues.append(f"{label}: must include exam_api.h exactly once")
        for token in BANNED_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", text):
                issues.append(f"{label}: obsolete token {token}")
        if re.search(r"LPC_TIM[0-3]->IR|LPC_SC->EXTINT", text):
            issues.append(f"{label}: bypasses canonical IRQ acknowledgement")

        for timer in range(4):
            handler = f"TIMER{timer}_IRQHandler"
            if handler in text and (
                f"exam_timer_ack(EXAM_TIMER{timer})" not in text
            ):
                issues.append(f"{label}: {handler} does not acknowledge Timer{timer}")
        if "RIT_IRQHandler" in text and "exam_rit_ack()" not in text:
            issues.append(f"{label}: RIT_IRQHandler does not acknowledge RIT")
        if "ADC_IRQHandler" in text and "exam_adc_irq_capture()" not in text:
            issues.append(f"{label}: ADC_IRQHandler does not capture the result")
        if "exam_adc_take(" in text and "exam_adc_start()" not in text:
            issues.append(f"{label}: ADC consumer never starts a conversion")
        if "exam_dac_write(" in text and "exam_dac_init()" not in text:
            issues.append(f"{label}: DAC is written without exam_dac_init")
        if "exam_joystick_read(" in text and "exam_joystick_init()" not in text:
            issues.append(f"{label}: joystick is read without exam_joystick_init")

        externs = names(
            r"^\s*extern\s+(?:[A-Za-z_][A-Za-z0-9_]*\s+)*"
            r"([A-Za-z_][A-Za-z0-9_]*)\s*\(",
            text,
        )
        for function in sorted(externs - assembly_exports):
            issues.append(f"{label}: assembly export missing for {function}")

    for function in sorted(used_api - declared_api):
        issues.append(f"solution calls undeclared API function {function}")

    if issues:
        print(f"Combined solution verification failed with {len(issues)} issue(s):")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Combined solution verification passed")
    print(
        f"Questions={len(question_dirs)} C={len(c_files)} "
        f"Assembly={len(assembly_files)} API used={len(used_api)}/52"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
