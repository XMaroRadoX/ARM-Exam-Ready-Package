#!/usr/bin/env python3
"""Structural regression checks for the exam project's optional startup flags."""

from pathlib import Path


HANDOFF = Path(__file__).resolve().parents[2]
PROJECT = HANDOFF / "ARM_Exam_Project"
CONFIG = (PROJECT / "Source/platform/exam_config.h").read_text(encoding="utf-8")
BOARD_C = (PROJECT / "Source/platform/exam_board.c").read_text(encoding="utf-8")
BOARD_H = (PROJECT / "Source/platform/exam_board.h").read_text(encoding="utf-8")

FLAGS = {
    "BUTTONS": "buttons_init(0)",
    "JOYSTICK": "joystick_init(0)",
    "TIMER0": "auto_init_timer(0u, AUTO_INIT_TIMER0)",
    "TIMER1": "auto_init_timer(1u, AUTO_INIT_TIMER1)",
    "TIMER2": "auto_init_timer(2u, AUTO_INIT_TIMER2)",
    "TIMER3": "auto_init_timer(3u, AUTO_INIT_TIMER3)",
    "RIT": "rit_scheduler_start()",
    "SYSTICK": "systick_start_periodic_ms(EXAM_AUTO_SYSTICK_PERIOD_MS)",
    "ADC": "potentiometer_start()",
    "DAC": "dac_init()",
}

for name, startup_call in FLAGS.items():
    flag = f"EXAM_AUTO_START_{name}"
    assert f"#ifndef {flag}" in CONFIG, f"missing configurable {flag}"
    assert f"#define {flag} 0" in CONFIG, f"{flag} must default off"
    assert startup_call in BOARD_C, f"missing startup path for {name}"
    assert f"AUTO_INIT_{name}" in BOARD_H, f"missing result bit for {name}"

assert "EXAM_RIT_DIRECT_MODE && (EXAM_AUTO_START_BUTTONS" in CONFIG
assert "EXAM_AUTO_START_BUTTONS && (EXAM_OWN_EINT0_HANDLER" in CONFIG
assert "EXAM_AUTO_START_SYSTICK && EXAM_OWN_SYSTICK_HANDLER" in CONFIG
assert "EXAM_AUTO_START_ADC && EXAM_OWN_ADC_HANDLER" in CONFIG
assert "exam_auto_init_started" in BOARD_C and "exam_auto_init_failures" in BOARD_C
assert "board_auto_init();" in BOARD_C

all_started_mask = sum(1 << bit for bit in range(len(FLAGS)))
assert all_started_mask == 0x3FF

print(f"AUTO_INIT_STRUCTURAL_PASS flags={len(FLAGS)} all_started_mask=0x{all_started_mask:03X}")
