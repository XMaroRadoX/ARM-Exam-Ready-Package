#!/usr/bin/env python3
"""Build the offline ARM exam workstation from the canonical package indexes."""

from __future__ import annotations

import csv
import html
import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote

from canonical_portal_content import ALGORITHM_VARIANTS, EXTRA_ALGORITHMS
import existing_algorithm_repairs
import exam_algorithms_numeric, exam_algorithms_arrays, exam_algorithms_strings, exam_algorithms_matrices
import exam_algorithms_fundamentals_arrays, exam_algorithms_fundamentals_strings
import exam_algorithms_fundamentals_arithmetic, exam_algorithms_fundamentals_bits
import exam_algorithms_fundamentals_matrices
from algorithm_catalog import ENTRIES as NEW_ALGORITHMS
from algorithm_review import source_details, VARIANT_SUFFIX
from algorithm_pages import body as algorithm_page_body, readable_c
from legacy_algorithm_tests import entries as legacy_test_entries
from canonical_api_reference import (
    API_DOCS,
    GROUP_DESCRIPTIONS,
    GROUP_ORDER,
    LEGACY_GAPS,
    PUBLIC_CONSTANTS,
    PUBLIC_GLOBALS,
    PUBLIC_TYPES,
    SCENARIOS,
    STATUS_VALUES,
    VALUE_GUIDANCE,
    render_gap_report,
    render_quick_reference,
)


ROOT = Path(__file__).resolve().parents[3]
LIBRARY = ROOT / "01_EXAM_READY" / "FRESH_SOLVED_ARM_EXAMS"
GUIDES = LIBRARY / "01_GUIDES_AND_INDEXES"
COURSE = GUIDES / "EXAM_COURSE"
MAINTENANCE = LIBRARY / "99_MAINTENANCE"
PORTAL = GUIDES / "PORTAL"
ASSETS = PORTAL / "assets"
HOME = ROOT / "START_HERE.html"
ALGORITHM_LIBRARY = ROOT / "03_ADDITIONAL_STUDY_MATERIAL" / "02 - Code Recipes" / "11 - Maximum Algorithm Reference"
GENERATED_SOURCES = LIBRARY / "03_COPY_PASTE_LIBRARY" / "CANONICAL_WORKSTATION"
ALGORITHM_INVENTORY_OUTPUT = MAINTENANCE / "ALGORITHM_INVENTORY.json"
API_HEADER = ROOT / "01_EXAM_READY" / "02_STARTING_TEMPLATES" / "Official Combined Exam API" / "Source" / "exam_api" / "exam_api.h"
STARTING_TEMPLATE = ROOT / "01_EXAM_READY" / "02_STARTING_TEMPLATES" / "Official Combined Exam API"
TEMPLATE_REFERENCE = STARTING_TEMPLATE.with_name("Official Combined Exam API Reference")
API_REFERENCE = TEMPLATE_REFERENCE / "EXAM_API_QUICK_REFERENCE.md"
API_GAP_REPORT = TEMPLATE_REFERENCE / "API_GAP_REPORT.md"
TEMPLATE_INTEGRATION = GUIDES / "USING_SOLVED_ANSWERS_WITH_OFFICIAL_TEMPLATE.md"

NAV = [
    ("Home", HOME),
    ("Past Exams", PORTAL / "exams" / "index.html"),
    ("Solution Patterns", PORTAL / "patterns" / "index.html"),
    ("API", PORTAL / "api" / "index.html"),
    ("Algorithms", PORTAL / "algorithms" / "index.html"),
    ("Guides", PORTAL / "guides" / "index.html"),
]

SECTION_META = {
    "exams": ("Past Exams", "Browse every reviewed paper, its questions, solution method, code, and related techniques."),
    "patterns": ("Solution Patterns", "Recognize recurring problem shapes and follow a reliable method before writing code."),
    "api": ("API", "Find the exact calls available in the current exam template and see minimal working examples."),
    "algorithms": ("Algorithms", "Study the algorithm families and data structures that match past and possible questions."),
    "guides": ("Guides", "Choose a goal and follow the shortest route from setup to a working answer."),
}

GUIDE_GOALS = [
    ("start-from-zero", "Start from zero", "Understand the package, the exam workflow, and what to open first."),
    ("solve-a-past-exam", "Solve a past exam", "Move from reading a question to a checked C and assembly answer."),
    ("start-a-working-project", "Start a working project", "Use the supplied template and preserve the expected project structure."),
    ("learn-c", "Learn C for the exam", "Focus on the C syntax, control flow, arrays, pointers, and functions used in questions."),
    ("learn-assembly", "Learn ARM assembly", "Build the register, stack, calling-convention, and loop skills needed for answers."),
    ("use-peripherals", "Use peripherals", "Use the sole Official Combined Exam API reference for buttons, timers, ADC, DAC, and interrupts."),
    ("combine-c-and-assembly", "Combine C and assembly", "Pass arguments safely and divide ownership between the two languages."),
    ("choose-interface", "Choose API, professor functions, or registers", "Match the interface to the question without mixing incompatible ownership models."),
    ("debug-common-failures", "Debug common failures", "Trace build, logic, interrupt, timer, stack, and hardware symptoms systematically."),
]

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "item"


def split_tags(*values: str) -> list[str]:
    found: list[str] = []
    for value in values:
        for part in re.split(r"[|,;/]+", value or ""):
            part = part.strip()
            if part and part.lower() not in {x.lower() for x in found}:
                found.append(part)
    return found


def rel(target: Path, source: Path, fragment: str = "", query: str = "") -> str:
    path = os.path.relpath(target, source.parent).replace("\\", "/")
    encoded = quote(path, safe="/._-")
    if query:
        encoded += "?" + query
    if fragment:
        encoded += "#" + quote(fragment, safe="-_.:")
    return encoded


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def strip_internal(value: str) -> str:
    value = re.sub(r"\bPAT-(?:[A-Z0-9]+-)+\d+\b", "", value or "", flags=re.I)
    value = re.sub(r"\b(?:sha256|hash|verification|evidence|generation code)\b[^.;<]*[.;]?", "", value, flags=re.I)
    return re.sub(r"\s{2,}", " ", value).strip(" -:;,")


def href(target: Path, source: Path, label: str, cls: str = "") -> str:
    class_attr = f' class="{esc(cls)}"' if cls else ""
    return f'<a{class_attr} href="{rel(target, source)}">{esc(label)}</a>'


def tags(values: list[str]) -> str:
    return "".join(f'<span class="tag">{esc(value)}</span>' for value in values if value)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def page(source: Path, title: str, description: str, body: str, crumbs: list[tuple[str, Path]], section: str = "", extra_head: str = "") -> str:
    nav = "".join(
        f'<a href="{rel(target, source)}"{(" aria-current=\"page\"" if label == section else "")}>{esc(label)}</a>'
        for label, target in NAV
    )
    breadcrumb = '<nav class="breadcrumbs" aria-label="Breadcrumb">' + "<span aria-hidden=\"true\">›</span>".join(
        f'<a href="{rel(target, source)}">{esc(label)}</a>' if index < len(crumbs) - 1 else f'<span aria-current="page">{esc(label)}</span>'
        for index, (label, target) in enumerate(crumbs)
    ) + "</nav>"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(description)}">
  <title>{esc(title)} · ARM Exam Workstation</title>
  <link rel="stylesheet" href="{rel(ASSETS / 'portal.css', source)}">
  {extra_head}
</head>
<body data-section="{esc(section)}">
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <a class="brand" href="{rel(HOME, source)}"><span class="brand-mark" aria-hidden="true">ARM</span><span>Exam Workstation</span></a>
    <nav class="primary-nav" aria-label="Primary navigation">{nav}</nav>
  </header>
  <main id="main-content" tabindex="-1">
    {breadcrumb}
    <header class="page-heading"><p class="eyebrow">{esc(section or 'ARM Exam Workstation')}</p><h1>{esc(title)}</h1><p>{esc(description)}</p></header>
    {body}
  </main>
  <footer><p>Offline ARM exam study package · All links stay inside this folder.</p></footer>
  <script src="{rel(ASSETS / 'portal.js', source)}"></script>
</body>
</html>'''


def card(title: str, summary: str, target: Path, source: Path, label: str, metadata: str = "", attrs: str = "") -> str:
    return f'''<article class="card" {attrs}>
      <div class="card-body"><h2>{esc(title)}</h2><p>{esc(summary)}</p>{metadata}</div>
      <a class="card-link" href="{rel(target, source)}">{esc(label)} <span aria-hidden="true">→</span></a>
    </article>'''


def resolve_index_path(value: str, base: Path = GUIDES) -> Path | None:
    if not value:
        return None
    clean = unquote(value.split("#", 1)[0]).replace("/", os.sep)
    candidates = [base / clean, LIBRARY / clean, ROOT / clean]
    for candidate in candidates:
        try:
            candidate = candidate.resolve()
            if candidate.exists():
                return candidate
        except OSError:
            pass
    return None


def normalized_heading(value: str) -> str:
    value = re.sub(r"[*_~]", "", value.replace(chr(96), ""))
    value = re.sub(r"^\s*(?:lesson\s+)?\d+\s*[.:\-–—]\s*", "", value, flags=re.I)
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def extract_markdown_section(path: Path, title: str, lesson_number: int | None = None) -> str:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    wanted = normalized_heading(title)
    start = None
    level = None
    for index, line in enumerate(lines):
        match = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        heading = normalized_heading(match.group(2))
        lesson_match = re.match(r"^lesson\s+(\d+)\b", match.group(2), flags=re.I)
        if (lesson_number is not None and lesson_match and int(lesson_match.group(1)) == lesson_number) or (
            lesson_number is None and heading == wanted
        ):
            start = index + 1
            level = len(match.group(1))
            break
    if start is None or level is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        match = re.match(r"^(#{2,6})\s+", lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    selected = lines[start:end]
    cleaned: list[str] = []
    skipping_level = None
    banned_sections = {"physical check", "what successful verification actually means"}
    for line in selected:
        match = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if match:
            current_level = len(match.group(1))
            if skipping_level is not None and current_level <= skipping_level:
                skipping_level = None
            if normalized_heading(match.group(2)) in banned_sections:
                skipping_level = current_level
                continue
        if skipping_level is None:
            cleaned.append(line)
    return "\n".join(cleaned).strip()


def markdown_inline(value: str, origin: Path, destination: Path) -> str:
    tokens: list[str] = []

    def hold(rendered: str) -> str:
        tokens.append(rendered)
        return f"@@HTML{len(tokens) - 1}@@"

    def link(match: re.Match[str]) -> str:
        label, target_value = match.group(1), match.group(2).strip()
        if target_value.startswith(("http://", "https://", "mailto:")):
            target = target_value
        else:
            base_value, sep, fragment = target_value.partition("#")
            target_path = origin if not base_value else (origin.parent / unquote(base_value)).resolve()
            target = rel(target_path, destination, fragment if sep else "")
        return hold(f'<a href="{esc(target)}">{esc(label)}</a>')

    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, value)
    marker = chr(96)
    value = re.sub(
        re.escape(marker) + r"([^" + re.escape(marker) + r"]+)" + re.escape(marker),
        lambda match: hold(f"<code>{esc(match.group(1))}</code>"),
        value,
    )
    value = html.escape(value, quote=False)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    for index, rendered in enumerate(tokens):
        value = value.replace(f"@@HTML{index}@@", rendered)
    return value


def markdown_fragment(markdown: str, origin: Path, destination: Path) -> str:
    if not markdown:
        return ""
    lines = markdown.splitlines()
    output: list[str] = []
    index = 0

    def starts_block(line: str) -> bool:
        return bool(
            not line.strip()
            or line.startswith(chr(96) * 3)
            or re.match(r"^#{2,6}\s+", line)
            or re.match(r"^\s*[-*]\s+", line)
            or re.match(r"^\s*\d+\.\s+", line)
            or line.lstrip().startswith(">")
            or line.lstrip().startswith("|")
            or line.lstrip().startswith("<!--")
        )

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("<!--"):
            while index < len(lines) and "-->" not in lines[index]:
                index += 1
            index += 1
            continue
        if line.startswith(chr(96) * 3):
            language = line[3:].strip().lower() or "text"
            index += 1
            code: list[str] = []
            while index < len(lines) and not lines[index].startswith(chr(96) * 3):
                code.append(lines[index])
                index += 1
            index += 1
            label = "assembly" if language in {"asm", "assembly", "s"} else language.upper()
            output.append(f'<details class="code-panel"><summary>Show {esc(label)} code</summary><pre tabindex="0"><code class="language-{esc(language)}">{esc(chr(10).join(code))}</code></pre></details>')
            continue
        heading = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if heading:
            rendered_level = min(4, max(2, len(heading.group(1)) - 1))
            output.append(f"<h{rendered_level}>{markdown_inline(heading.group(2), origin, destination)}</h{rendered_level}>")
            index += 1
            continue
        if line.lstrip().startswith("|") and index + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1]):
            table_lines = [line]
            index += 2
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            rows = [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in table_lines]
            header = "".join(f"<th>{markdown_inline(cell, origin, destination)}</th>" for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{markdown_inline(cell, origin, destination)}</td>" for cell in row) + "</tr>" for row in rows[1:])
            output.append(f'<div class="table-wrap"><table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table></div>')
            continue
        list_match = re.match(r"^\s*([-*]|\d+\.)\s+(.+)", line)
        if list_match:
            ordered = list_match.group(1)[0].isdigit()
            tag_name = "ol" if ordered else "ul"
            entries: list[str] = []
            while index < len(lines):
                current = re.match(r"^\s*([-*]|\d+\.)\s+(.+)", lines[index])
                if not current or current.group(1)[0].isdigit() != ordered:
                    break
                entries.append(f"<li>{markdown_inline(current.group(2), origin, destination)}</li>")
                index += 1
            output.append(f"<{tag_name}>{''.join(entries)}</{tag_name}>")
            continue
        if line.lstrip().startswith(">"):
            quotes: list[str] = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                quotes.append(lines[index].lstrip()[1:].strip())
                index += 1
            output.append(f'<blockquote>{markdown_inline(" ".join(quotes), origin, destination)}</blockquote>')
            continue
        paragraph = [stripped]
        index += 1
        while index < len(lines) and not starts_block(lines[index]):
            paragraph.append(lines[index].strip())
            index += 1
        output.append(f"<p>{markdown_inline(' '.join(paragraph), origin, destination)}</p>")
    return "".join(output)


def language_of(row: dict[str, str]) -> str:
    raw = " ".join([row.get("languages", ""), row.get("architecture", ""), row.get("answer_file", ""), row.get("c_source", ""), row.get("arm_source", "")]).lower()
    has_c = bool(re.search(r"\bc\b|main\.c|c_source|\.c\b", raw))
    has_asm = "assembly" in raw or ".s" in raw or "arm" in raw
    if has_c and has_asm:
        return "Both"
    if has_asm:
        return "Assembly"
    return "C"


def history_of(row: dict[str, str]) -> str:
    raw = " ".join(row.values()).lower()
    if row.get("question_count", "").isdigit() and int(row["question_count"]) > 0:
        return "seen"
    if any(term in raw for term in ("extra practice", "supplement", "rare")):
        return "extra"
    return "possible"


def public_history(value: str) -> str:
    return {"seen": "Appeared in past exams", "possible": "Possible variation", "extra": "Extra practice"}.get(value, "Possible variation")


def pattern_family(row: dict[str, str]) -> str:
    raw = " ".join(row.get(key, "") for key in ("family", "tag", "title", "source_page")).lower()
    tests = [
        ("Graphs and mazes", ("graph", "maze", "bfs", "dfs", "kruskal", "shortest")),
        ("Recurrences", ("recurr", "sequence", "fibonacci")),
        ("Interrupts", ("interrupt", "irq", "svc", "exception", "event")),
        ("Timers", ("timer", "systick", "rit", "period", "capture", "pwm")),
        ("Peripheral workflows", ("adc", "dac", "button", "joystick", "led", "speaker", "peripheral", "board")),
        ("ABI and stack", ("abi", "stack", "argument", "register", "caller", "callee", "ownership")),
        ("Arrays and memory", ("array", "memory", "pointer", "matrix", "buffer", "mem")),
        ("Arithmetic and bits", ("arithmetic", "bit", "decimal", "fixed", "divide", "multiply", "shift", "cpu")),
        ("Loops and state", ("loop", "state", "flow", "counter", "game")),
    ]
    for family, needles in tests:
        if any(needle in raw for needle in needles):
            return family
    return "Loops and state"


def pattern_guidance(family: str, title: str, clues: list[str]) -> str:
    guidance = {
        "Arrays and memory": (
            "A base address, an element count, explicit element widths, and a result value or output buffer.",
            "Validate the count and capacity, choose the correct load/store width, keep a bounded index, and state the loop invariant before writing output.",
            "Use fixed-width types, keep indexes unsigned, validate before dereferencing, and make output capacity explicit.",
            "Keep the base pointer separate from the index, scale addresses by element width, and use signed branches only for signed data.",
            "Reading element zero from an empty input, mixing byte and word accesses, and writing past output capacity.",
        ),
        "Loops and state": (
            "An initial state, an event or repeated step, a bounded stopping rule, and a final state or result.",
            "Name every state, write the transition conditions, update one step at a time, and prove how the loop or machine terminates.",
            "Use an enum for states, isolate each transition, and keep repeated work bounded.",
            "Assign long-lived state to preserved registers or memory and keep every branch target and exit balanced.",
            "Hidden state changes, off-by-one exits, accidental fall-through, and treating a held input as repeated edges.",
        ),
        "ABI and stack": (
            "An exact C prototype, argument widths, the first four argument words, any caller-stack arguments, and the return contract.",
            "Draw the entry register/stack map, calculate the frame, preserve required registers, keep eight-byte alignment, and recalculate offsets after every prologue change.",
            "Declare one matching fixed-width prototype and pass arguments in the documented order.",
            "Use R0-R3 for the first four words, load later words from caller SP plus the exact frame size, preserve R4-R11, and balance SP on every return.",
            "Stale fifth-argument offsets, mismatched prototypes, lost LR across BL, and unbalanced early returns.",
        ),
        "Arithmetic and bits": (
            "Operand widths and signedness, the required result width, rounding or overflow rules, and any bit positions or masks.",
            "Write the mathematical contract, widen before risky operations, isolate masks and shifts, and check zero, limits, carry, and sign behavior.",
            "Use unsigned operations for defined wraparound and wider intermediates when multiplication or addition can overflow.",
            "Choose signed or unsigned instructions and conditions deliberately; track flags only when the contract requires them.",
            "Undefined signed overflow, shifting by an invalid amount, losing high words, and confusing carry with signed overflow.",
        ),
        "Recurrences": (
            "Seed values, a recurrence rule, an output count or capacity, and the required numeric width.",
            "Handle seed-only cases first, generate exactly one new term per iteration, store only within capacity, and document overflow behavior.",
            "Separate input length from output capacity and use widened intermediates where required.",
            "Keep seeds and loop bounds stable in preserved registers and use the exact element width for loads and stores.",
            "Generating too many terms, reading a seed that does not exist, overwriting earlier state, and silent overflow.",
        ),
        "Graphs and mazes": (
            "A graph or grid representation, start and goal, visited state, bounded work storage, and a traversal or cost result.",
            "Choose DFS, BFS, shortest path, or MST from the question, initialize visited/work structures, process each item once, and enforce all bounds.",
            "Use explicit arrays for visited, queue, stack, parent, distance, or edge state and pass capacities separately.",
            "Keep addressing simple and bounded; complex graph control is usually clearer in C unless assembly is explicitly required.",
            "Unbounded queue/stack growth, revisiting nodes, invalid neighbors, wrong matrix stride, and missing unreachable cases.",
        ),
        "Interrupts": (
            "An interrupt source, the flag that identifies it, a short handler action, shared event state, and foreground work.",
            "Initialize shared state, configure and clear the source, enable it last, publish a small event in the handler, and consume it once in main.",
            "Use volatile only for direct asynchronous state and use a bounded event or critical-section helper for compound updates.",
            "Preserve the exception contract, clear the correct hardware flag, and avoid calling long or blocking work from an IRQ.",
            "Multiple owners for one vector, uncleared flags, lost read-modify-write updates, and long interrupt handlers.",
        ),
        "Timers": (
            "A timer number, clock assumption, period and units, mode, callback or event, and ownership of the handler.",
            "Convert units once, configure the selected mode, clear pending state, enable the interrupt, start last, and keep one owner for reconfiguration.",
            "Use named time units and keep timer configuration outside the interrupt unless the question requires a bounded update.",
            "Use the required API or exact registers, clear match/capture flags, and account for counter wraparound.",
            "Wrong clock or units, periodic versus one-shot mismatch, two modules owning one timer, and failure to clear the flag.",
        ),
        "Peripheral workflows": (
            "A concrete input or output device, its initialization, event or sample timing, conversion or scaling, and final output.",
            "Make the peripheral work alone first, then connect it through one event path and one owner to the algorithm or display.",
            "Initialize before use, check completion or validity, scale within the destination range, and keep hardware calls out of pure algorithms.",
            "Let C own peripheral setup and IRQs unless the paper explicitly assigns direct-register work to assembly.",
            "Mixing interfaces, reading before completion, incorrect active-low logic, unbounded scaling, and competing timer ownership.",
        ),
    }
    inputs, method, c_approach, assembly, mistakes = guidance[family]
    clue_text = ", ".join(clues[:8]) if clues else title
    return f'''<h2>How to recognize it</h2><p>Look for: <strong>{esc(clue_text)}</strong>. Confirm that the question really has the same data shape, ownership, and stopping rule.</p>
      <h2>Inputs and outputs</h2><p>{esc(inputs)}</p>
      <h2>Solving method</h2><p>{esc(method)}</p>
      <h2>C approach</h2><p>{esc(c_approach)}</p>
      <h2>Assembly considerations</h2><p>{esc(assembly)}</p>
      <h2>Common mistakes</h2><p>{esc(mistakes)}</p>'''


def parse_api() -> list[dict[str, object]]:
    text = API_HEADER.read_text(encoding="utf-8", errors="replace")
    prototype = re.compile(
        r"\b(exam_status_t|void|uint8_t|uint32_t)\s+"
        r"(exam_[A-Za-z0-9_]+)\s*\((.*?)\)\s*;",
        re.S,
    )

    def group_for(name: str) -> str:
        if name == "exam_init": return "Core"
        if name.startswith("exam_led"): return "LEDs"
        if name.startswith(("exam_button", "exam_debounce")): return "Buttons"
        if name.startswith("exam_timer"): return "Timers"
        if name.startswith("exam_systick"): return "SysTick"
        if name.startswith("exam_rit"): return "RIT"
        if name.startswith("exam_joystick"): return "Joystick"
        if name.startswith("exam_adc"): return "ADC"
        if name.startswith("exam_dac"): return "DAC"
        if name.startswith(("exam_events", "exam_critical")): return "Events"
        if name.startswith("exam_fault"): return "Faults"
        if name.startswith("exam_svc"): return "SVC"
        return "Core"

    records: list[dict[str, object]] = []
    for match in prototype.finditer(text):
        return_type, title, raw_parameters = match.groups()
        parameters = re.sub(r"\s+", " ", raw_parameters.strip())
        declaration = f"{return_type} {title}({parameters});"
        records.append({
            "group": group_for(title),
            "title": title,
            "declaration": declaration,
            "description": "",
        })
    declared = {str(record["title"]) for record in records}
    documented = set(API_DOCS)
    if declared != documented:
        raise SystemExit(
            "Canonical API documentation differs from exam_api.h: "
            f"missing {sorted(declared - documented)}, extra {sorted(documented - declared)}"
        )
    for record in records:
        name = str(record["title"])
        declared_params = {param_name for param_name, _ in api_parameters(str(record["declaration"]))}
        documented_params = set(API_DOCS[name]["params"])
        if declared_params != documented_params:
            raise SystemExit(
                f"Parameter documentation differs for {name}: "
                f"missing {sorted(declared_params - documented_params)}, "
                f"extra {sorted(documented_params - declared_params)}"
            )
        record["description"] = API_DOCS[name]["summary"]
    return records


def source_code(path: Path | None) -> str:
    if not path or not path.exists():
        return "Source file is not available in this copy."
    return path.read_text(encoding="utf-8", errors="replace")


def details_code(label: str, code: str, raw: Path | None, destination: Path, language: str, expanded: bool = False) -> str:
    raw_link = href(raw, destination, f"Open raw {language} file", "raw-link") if raw and raw.exists() else ""
    open_attr = " open" if expanded else ""
    return f'''<details class="code-panel"{open_attr}><summary>{esc(label)}</summary>
      <div class="code-actions">{raw_link}</div><pre tabindex="0"><code class="language-{esc(language.lower())}">{esc(code)}</code></pre>
    </details>'''


def reference_code(path: Path | None, languages: tuple[str, ...]) -> str:
    if not path or not path.exists():
        return "No code reference is available in this copy."
    text = source_code(path)
    if path.suffix.lower() not in {".md", ".markdown", ".html", ".htm"}:
        return text
    language_pattern = "|".join(re.escape(language) for language in languages)
    match = re.search(rf"```(?:{language_pattern})\s*\n(.*?)```", text, re.I | re.S)
    if match:
        return next((group for group in match.groups() if group is not None), match.group(0)).strip()
    fallback = re.search(r"```[A-Za-z0-9_+-]*\s*\n(.*?)```", text, re.S)
    return fallback.group(1).strip() if fallback else text


def build_assets() -> None:
    css = r''':root{--navy:#102a43;--navy-2:#163d63;--ink:#152536;--muted:#546779;--line:#ced9e2;--paper:#fff;--wash:#f3f7fa;--blue:#1565c0;--gold:#f3b61f;--focus:#ffbf47;--radius:.65rem;--shadow:0 2px 10px rgba(16,42,67,.08);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:var(--wash)}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0}a{color:#075aa5;text-underline-offset:.16em}a:hover{text-decoration-thickness:2px}.skip-link{position:fixed;left:1rem;top:-5rem;background:#fff;color:#000;padding:.75rem 1rem;z-index:20}.skip-link:focus{top:1rem}.site-header{background:var(--navy);color:#fff;padding:.75rem clamp(1rem,4vw,3rem);display:flex;gap:1.5rem;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:10;box-shadow:0 2px 8px #0003}.brand{display:flex;align-items:center;gap:.65rem;color:#fff;text-decoration:none;font-weight:800;white-space:nowrap}.brand-mark{display:grid;place-items:center;background:var(--gold);color:#102a43;width:2.6rem;height:2.6rem;border-radius:.45rem;font-size:.78rem;letter-spacing:.05em}.primary-nav{display:flex;gap:.25rem;overflow-x:auto;padding:.15rem}.primary-nav a{color:#eaf4ff;text-decoration:none;padding:.5rem .65rem;border-radius:.35rem;white-space:nowrap;font-size:.9rem}.primary-nav a:hover,.primary-nav a[aria-current=page]{background:#fff;color:var(--navy)}main{width:min(1180px,calc(100% - 2rem));margin:0 auto;padding:1.25rem 0 4rem}.breadcrumbs{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;font-size:.9rem;color:var(--muted);margin:.25rem 0 1rem}.page-heading{background:linear-gradient(120deg,#fff,#eaf2f8);border-left:.4rem solid var(--blue);padding:clamp(1.15rem,4vw,2.25rem);border-radius:var(--radius);box-shadow:var(--shadow);margin-bottom:1.25rem}.page-heading h1{font-size:clamp(2rem,5vw,3.35rem);line-height:1.05;margin:.15rem 0 .7rem;letter-spacing:-.035em}.page-heading p:last-child{max-width:75ch;color:var(--muted);font-size:1.05rem;margin-bottom:0}.eyebrow{text-transform:uppercase;letter-spacing:.11em;font-size:.75rem;font-weight:800;color:#075aa5;margin:0}.home-hero{padding:clamp(1.5rem,6vw,4rem);background:linear-gradient(135deg,var(--navy),var(--navy-2));color:#fff;border-radius:var(--radius);box-shadow:var(--shadow);margin-bottom:1.4rem}.home-hero h1{font-size:clamp(2.25rem,6vw,4.4rem);line-height:1;margin:.2rem 0 1rem;letter-spacing:-.045em}.home-hero p{max-width:65ch;color:#dbe9f5;font-size:1.1rem}.search-form{display:grid;grid-template-columns:1fr auto;gap:.6rem;margin-top:1.5rem}.search-form input,.filter-bar select,.filter-bar input{min-height:2.8rem;border:2px solid #8ca3b7;border-radius:.4rem;padding:.65rem .75rem;font:inherit;background:#fff;color:var(--ink)}button,.button{min-height:2.8rem;border:0;border-radius:.4rem;padding:.65rem 1rem;background:var(--gold);color:#122536;font:inherit;font-weight:800;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:1rem}.card{background:#fff;border:1px solid var(--line);border-top:.28rem solid var(--blue);border-radius:var(--radius);box-shadow:var(--shadow);display:flex;flex-direction:column;min-width:0}.card-body{padding:1rem 1rem .7rem;flex:1}.card h2,.card h3{font-size:1.15rem;line-height:1.25;margin:0 0 .5rem}.card p{color:var(--muted);margin:.25rem 0 .7rem}.card-link{display:flex;justify-content:space-between;gap:.5rem;padding:.8rem 1rem;border-top:1px solid var(--line);font-weight:750;text-decoration:none}.card-link:hover{background:#edf5fb}.tag-list{display:flex;flex-wrap:wrap;gap:.35rem;margin:.65rem 0}.tag{display:inline-flex;background:#eaf2f8;color:#173c5e;border-radius:999px;padding:.18rem .55rem;font-size:.76rem;font-weight:700}.filter-panel{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1rem;margin:1rem 0}.filter-bar{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.75rem}.filter-bar label{font-size:.85rem;font-weight:750;display:grid;gap:.25rem}.results-note{color:var(--muted);margin:.75rem 0 0}.section-block{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:clamp(1rem,3vw,1.7rem);margin:1rem 0;box-shadow:var(--shadow)}.section-block h2{margin-top:0}.summary-grid,.fact-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.7rem}.fact{background:#eef4f8;border-radius:.45rem;padding:.8rem}.fact dt{font-size:.75rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);font-weight:800}.fact dd{margin:.2rem 0 0;font-weight:700}table{width:100%;border-collapse:collapse;display:block;overflow-x:auto;margin:1rem 0}th,td{border:1px solid var(--line);padding:.65rem;text-align:left;vertical-align:top}th{background:#eaf2f8;color:var(--navy)}.question{border-left:.25rem solid var(--gold);padding:.4rem 1rem;margin:1rem 0;background:#fffaf0}.question h3{margin:.2rem 0}.code-panel{border:1px solid #93a8ba;border-radius:.45rem;margin:1rem 0;background:#fff}.code-panel summary{cursor:pointer;padding:.8rem 1rem;font-weight:800;background:#eaf2f8}.code-actions{padding:.5rem 1rem 0}.raw-link{font-weight:700}pre{background:#0b1f33;color:#e9f2f9;border-radius:.4rem;padding:1rem;overflow:auto;white-space:pre;max-height:34rem}code{font: .9rem/1.5 ui-monospace,SFMono-Regular,Consolas,monospace}.notice{border-left:.3rem solid var(--gold);background:#fff8df;padding:.8rem 1rem;border-radius:.3rem}.flow{font-family:ui-monospace,Consolas,monospace;background:#eaf2f8;padding:.8rem;border-radius:.4rem;overflow-wrap:anywhere}.search-group{margin:1.5rem 0}.search-group h2{border-bottom:2px solid var(--navy);padding-bottom:.4rem}.empty-state{text-align:center;color:var(--muted);padding:2rem;background:#fff;border:1px dashed #90a4b5;border-radius:.5rem}.contents{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}.contents a{background:#eaf2f8;border-radius:.35rem;padding:.4rem .65rem;text-decoration:none}footer{background:#e1eaf1;color:#425466;padding:1.5rem;text-align:center;font-size:.85rem}:focus-visible{outline:4px solid var(--focus);outline-offset:3px}.hidden,[hidden]{display:none!important}@media(max-width:900px){.site-header{position:static;align-items:flex-start;flex-direction:column}.primary-nav{width:100%}}@media(max-width:560px){main{width:min(100% - 1rem,1180px)}.search-form{grid-template-columns:1fr}.page-heading{padding:1.1rem}.home-hero{padding:1.25rem}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}'''
    js = r'''(()=>{"use strict";const norm=v=>(v||"").toString().toLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g,"");const split=v=>norm(v).split(/\s+/).filter(Boolean);function initFilters(){document.querySelectorAll("[data-filter-scope]").forEach(scope=>{const controls=[...scope.querySelectorAll("[data-filter]")],cards=[...scope.querySelectorAll("[data-filter-item]")],note=scope.querySelector("[data-results-note]");const apply=()=>{let shown=0;cards.forEach(card=>{const ok=controls.every(control=>{const wanted=norm(control.value);if(!wanted)return true;const hay=norm(card.dataset[control.dataset.filter]||card.textContent);return hay.includes(wanted)});card.hidden=!ok;if(ok)shown++});if(note)note.textContent=`${shown} item${shown===1?"":"s"} shown`;};controls.forEach(c=>c.addEventListener(c.tagName==="INPUT"?"input":"change",apply));apply()})}function score(item,q){if(!q)return 1;const title=norm(item.title),aliases=norm((item.aliases||[]).join(" ")),topics=norm([...(item.topics||[]),...(item.components||[])].join(" ")),summary=norm(item.summary),words=split(q);let total=0;if(title===q)total+=1000;if(title.startsWith(q))total+=400;if(title.includes(q))total+=220;if(aliases.includes(q))total+=180;if(topics.includes(q))total+=120;if(summary.includes(q))total+=50;words.forEach(w=>{if(title.includes(w))total+=35;if(aliases.includes(w))total+=25;if(topics.includes(w))total+=18;if(summary.includes(w))total+=5});return words.every(w=>(title+" "+aliases+" "+topics+" "+summary).includes(w))?total:0}function initSearch(){const root=document.querySelector("[data-global-search]");if(!root||!window.ARM_PORTAL_DATA)return;const form=root.querySelector("form"),input=root.querySelector("[name=q]"),results=root.querySelector("[data-search-results]"),controls=[...root.querySelectorAll("[data-search-filter]")],params=new URLSearchParams(location.search);input.value=params.get("q")||"";const render=()=>{const q=norm(input.value.trim()),filters=Object.fromEntries(controls.map(c=>[c.dataset.searchFilter,norm(c.value)]));let items=window.ARM_PORTAL_DATA.items.map(item=>({item,rank:score(item,q)})).filter(x=>x.rank>0).filter(({item})=>Object.entries(filters).every(([key,value])=>!value||norm(Array.isArray(item[key])?item[key].join(" "):item[key]).includes(value))).sort((a,b)=>b.rank-a.rank||a.item.title.localeCompare(b.item.title));const groups=new Map;items.forEach(({item})=>{if(!groups.has(item.kind))groups.set(item.kind,[]);groups.get(item.kind).push(item)});results.replaceChildren();if(!items.length){results.innerHTML='<p class="empty-state">No matches. Try a function name, exam topic, peripheral, or problem shape.</p>';return}for(const [kind,group] of groups){const section=document.createElement("section");section.className="search-group";const heading=document.createElement("h2");heading.textContent=`${kind} (${group.length})`;section.append(heading);const grid=document.createElement("div");grid.className="grid";group.forEach(item=>{const article=document.createElement("article");article.className="card";const body=document.createElement("div");body.className="card-body";const h=document.createElement("h3");h.textContent=item.title;const p=document.createElement("p");p.textContent=item.summary;const meta=document.createElement("div");meta.className="tag-list";[item.examHistory,...(item.languages||[]),...(item.components||[]).slice(0,3)].filter(Boolean).forEach(v=>{const tag=document.createElement("span");tag.className="tag";tag.textContent=v;meta.append(tag)});const a=document.createElement("a");a.className="card-link";a.href=item.route;a.textContent=`View ${item.kind.toLowerCase()} →`;body.append(h,p,meta);article.append(body,a);grid.append(article)});section.append(grid);results.append(section)}};form.addEventListener("submit",event=>{event.preventDefault();const url=new URL(location.href);url.searchParams.set("q",input.value.trim());history.replaceState(null,"",url);render()});controls.forEach(c=>c.addEventListener("change",render));render()}document.addEventListener("DOMContentLoaded",()=>{initFilters();initSearch()})})();'''
    css += r'''
body[data-section=API] main{width:min(1380px,calc(100% - 2rem))}
.api-shell{display:grid;grid-template-columns:minmax(235px,285px) minmax(0,1fr);gap:1.25rem;align-items:start}
.api-sidebar{position:sticky;top:5.25rem;max-height:calc(100vh - 6.5rem);overflow:auto;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1rem;box-shadow:var(--shadow)}
.api-sidebar>label{display:block;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;font-weight:800;color:var(--muted);margin-bottom:.3rem}
.api-sidebar>input{width:100%;min-height:2.6rem;border:2px solid #8ca3b7;border-radius:.4rem;padding:.55rem .65rem;font:inherit}
.api-nav-count{font-size:.8rem;color:var(--muted);margin:.45rem 0}
.api-sidebar section{border-top:1px solid var(--line);padding-top:.65rem;margin-top:.65rem}
.api-sidebar h3{font-size:.78rem;text-transform:uppercase;letter-spacing:.07em;margin:0 0 .35rem}
.api-sidebar h3 a{color:var(--navy);text-decoration:none}
.api-sidebar ul{list-style:none;margin:0;padding:0;display:grid;gap:.08rem}
.api-sidebar li a{display:block;padding:.28rem .4rem;border-radius:.3rem;text-decoration:none;overflow-wrap:anywhere}
.api-sidebar li a:hover,.api-sidebar li a[aria-current=page]{background:#dcebf6;color:#073d6c}
.api-sidebar code{font-size:.77rem}
.api-content{min-width:0}
.api-signature{background:#102a43;color:#fff;border-radius:var(--radius);padding:clamp(1rem,3vw,1.7rem);box-shadow:var(--shadow);margin-bottom:1rem}
.api-signature h2{margin:.15rem 0 .6rem;font-size:1rem;color:#dbe9f5}
.api-signature pre{margin:0;background:#071727;border:1px solid #37536d;max-height:none}
.api-content .section-block h3{font-size:1rem;color:var(--navy);margin:1.25rem 0 .35rem}
.api-content .section-block h2+h3{margin-top:.25rem}
.api-none{color:var(--muted);font-style:italic}
.api-warning,.api-exam-note{border-left:.3rem solid #c73b31;padding:.55rem 1rem;margin-top:1rem;background:#fff1ef}
.api-exam-note{border-left-color:var(--blue);background:#eef6fc}
.api-warning h3,.api-exam-note h3{margin:.1rem 0!important}
.api-value-table td:first-child{font-weight:750;white-space:nowrap}.api-value-evidence{color:var(--muted);font-size:.9rem}.api-scenario{border:1px solid var(--line);border-left:.3rem solid var(--gold);border-radius:.45rem;padding:1rem;margin:1rem 0;background:#fffdf7}.api-scenario h3{margin-top:0!important}.api-scenario-basis{color:var(--muted)}.evidence-badge{display:inline-flex;background:#eaf2f8;color:#173c5e;border-radius:999px;padding:.15rem .5rem;margin-right:.35rem;font-size:.75rem;font-weight:800}.api-evidence-key{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem}.api-evidence-key div{border:1px solid var(--line);border-radius:.45rem;padding:.8rem}.api-evidence-key strong{display:block;color:var(--navy);margin-bottom:.25rem}
.api-related{columns:2;column-gap:2rem}
.api-pager{display:flex;justify-content:space-between;gap:1rem;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1rem;margin-top:1rem}
.api-pager span:last-child{text-align:right}
.api-actions{display:flex;flex-wrap:wrap;gap:.6rem}
.api-rule-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.7rem;margin-top:1rem}
.api-rule-grid div{display:grid;gap:.15rem;background:#eef4f8;border-radius:.45rem;padding:.8rem}
.api-rule-grid span{color:var(--muted)}
.api-group-section{scroll-margin-top:5.5rem}
.api-group-section table{display:table}
@media(max-width:900px){body[data-section=API] main{width:min(100% - 1rem,1380px)}.api-shell{grid-template-columns:1fr}.api-sidebar{position:static;max-height:24rem}.api-sidebar nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:0 1rem}.api-content{grid-row:1}.api-sidebar{grid-row:2}.api-rule-grid,.api-evidence-key{grid-template-columns:1fr}.api-group-section table{display:block}}
@media(max-width:560px){.api-related{columns:1}.api-pager{display:grid}.api-pager span:last-child{text-align:left}.api-actions{display:grid}.api-actions .button{width:100%}}
'''
    js += r'''
;(()=>{"use strict";function initApiNavigation(){document.querySelectorAll("[data-api-nav-search]").forEach(input=>{const sidebar=input.closest(".api-sidebar"),entries=[...sidebar.querySelectorAll("[data-api-entry]")],groups=[...sidebar.querySelectorAll("[data-api-group]")],count=sidebar.querySelector("[data-api-nav-count]");const apply=()=>{const words=input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);let shown=0;entries.forEach(entry=>{const match=words.every(word=>entry.textContent.toLowerCase().includes(word));entry.hidden=!match;if(match)shown++});groups.forEach(group=>{group.hidden=![...group.querySelectorAll("[data-api-entry]")].some(entry=>!entry.hidden)});count.textContent=`${shown} of ${entries.length} functions`};input.addEventListener("input",apply);apply()})}if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",initApiNavigation);else initApiNavigation()})();
'''
    write(ASSETS / "portal.css", css)
    write(ASSETS / "portal.js", js)


def build_home() -> None:
    cards = card(
        "Starting Template",
        "Open the restored Official Combined Exam API project before starting a new solution.",
        STARTING_TEMPLATE / "sample.uvprojx",
        HOME,
        "Open Starting Template",
    ) + "".join(
        card(title, summary, PORTAL / key / "index.html", HOME, f"Browse {title}")
        for key, (title, summary) in SECTION_META.items()
    )
    body = f'''<section class="home-hero"><p class="eyebrow">Local, portable, exam-focused</p><h1>ARM Exam Workstation</h1>
      <p>Search the complete study package or go straight to the exact kind of help you need. Every exam, method, Official Combined API call, algorithm, and guide is at most two choices away.</p>
      <form class="search-form" action="{rel(PORTAL / 'search.html', HOME)}" method="get"><label class="hidden" for="home-search">Search exams, functions, algorithms, and peripherals</label><input id="home-search" name="q" type="search" placeholder="Try Mastermind, fifth argument, exam_timer_config_ms, or ADC"><button type="submit">Search everything</button></form>
    </section><section aria-labelledby="destinations"><h2 id="destinations">Choose a destination</h2><div class="grid">{cards}</div></section>'''
    html_text = page(HOME, "ARM Exam Workstation", "Direct access to the ARM exam material.", body, [("Home", HOME)])
    html_text = html_text.replace('<header class="page-heading"><p class="eyebrow">ARM Exam Workstation</p><h1>ARM Exam Workstation</h1><p>Direct access to the ARM exam material.</p></header>', "")
    write(HOME, html_text)


def build_search(items: list[dict[str, object]]) -> None:
    target = PORTAL / "search.html"
    kinds = [value[0] for value in SECTION_META.values()]
    body = f'''<section class="filter-panel" data-global-search><form class="search-form"><label class="hidden" for="global-q">Search the workstation</label><input id="global-q" name="q" type="search" placeholder="Search by title, alias, topic, component, or summary"><button type="submit">Search</button></form>
      <div class="filter-bar"><label>Section<select data-search-filter="kind"><option value="">All sections</option>{''.join(f'<option>{esc(x)}</option>' for x in kinds)}</select></label><label>Language<select data-search-filter="languages"><option value="">All languages</option><option>C</option><option>Assembly</option><option>Both</option></select></label><label>Component<select data-search-filter="components"><option value="">All components</option>{''.join(f'<option>{x}</option>' for x in ['LED','Buttons','Joystick','Timer','RIT','SysTick','ADC','DAC','SVC'])}</select></label><label>Exam history<select data-search-filter="examHistory"><option value="">All history</option><option>Appeared in past exams</option><option>Possible variation</option><option>Extra practice</option></select></label></div><div data-search-results aria-live="polite"></div></section>'''
    extra = f'<script data-search-corpus data-src="{rel(ASSETS / "portal-data.js", target)}"></script>'
    write(target, page(target, "Search everything", "Search all six sections from one place.", body, [("Home", HOME), ("Search", target)], extra_head=extra))
    public = {"items": items}
    write(ASSETS / "portal-data.js", "window.ARM_PORTAL_DATA=" + json.dumps(public, ensure_ascii=False, separators=(",", ":")) + ";\n")


BASE_BUILD_SEARCH = build_search


def connect_related(items: list[dict[str, object]], only_kind: str = "") -> None:
    for item in items:
        if only_kind and item.get("kind") != only_kind:
            continue
        item_terms = {slug(str(value)) for value in list(item.get("components", [])) + list(item.get("topics", [])) if value}
        scored = []
        for candidate in items:
            if candidate["id"] == item["id"]:
                continue
            candidate_terms = {slug(str(value)) for value in list(candidate.get("components", [])) + list(candidate.get("topics", [])) if value}
            score = len(item_terms & candidate_terms)
            if score:
                scored.append((score, str(candidate["title"]), str(candidate["id"])))
        scored.sort(key=lambda value: (-value[0], value[1]))
        item["relatedIds"] = [value[2] for value in scored[:8]]


def build_exams(exams: list[dict[str, str]], questions: list[dict[str, str]], solutions: list[dict[str, str]], pattern_links: dict[str, Path], algorithm_links: dict[str, Path], combo_links: dict[str, Path], items: list[dict[str, object]]) -> None:
    from question_review import read_reviews, render as render_question_review, assembly_dependency
    reviews = read_reviews()
    index = PORTAL / "exams" / "index.html"
    solution_by_id = {row.get("exam_id", ""): row for row in solutions}
    question_manifest: list[dict[str, object]] = []
    cards: list[str] = []
    years, variants, components = set(), set(), set()
    for row in exams:
        exam_id = row.get("exam_id") or row.get("date") or row.get("project") or "exam"
        date = row.get("date", "").strip()
        project_title = row.get("project", "").replace("_", " ").strip()
        project_title = re.sub(rf"^{re.escape(date)}\s*", "", project_title)
        project_title = re.sub(r"\bARM\s*(\d+)\b", r"ARM \1", project_title, flags=re.I)
        title = f"{date} {project_title}".strip()
        destination = PORTAL / "exams" / f"{slug(exam_id)}.html"
        project_parts = row.get("project", "").split("_")
        question_prefix = "_".join(project_parts[:2]) if len(project_parts) >= 2 else row.get("project", "")
        exam_questions = [q for q in questions if question_prefix and q.get("question_id", "").startswith(question_prefix + "-Q")]
        if not exam_questions:
            exam_questions = [q for q in questions if q.get("question_id", "").startswith(exam_id)]
        if not exam_questions:
            exam_questions = [q for q in questions if q.get("date") == date]
        component_list = split_tags(*(q.get("peripheral_tags", "") for q in exam_questions), *(q.get("interrupt_tags", "") for q in exam_questions), *(q.get("timing_tags", "") for q in exam_questions))
        algorithm_list = split_tags(*(q.get("algorithm_tags", "") for q in exam_questions))
        year = (row.get("date") or "Unknown")[:4]
        variant = project_title or "Standard"
        years.add(year); variants.add(variant); components.update(component_list)
        summary = "; ".join(strip_internal(q.get("requirement_summary", "")) for q in exam_questions[:2]) or "Reviewed ARM exam with linked solutions and methods."
        attrs = f'data-filter-item data-year="{esc(year)}" data-variant="{esc(variant)}" data-component="{esc(" ".join(component_list))}"'
        question_shortcuts = " · ".join(href(PORTAL / "exams" / f"{slug(q.get('question_id','question'))}.html", index, f"Read {q.get('question') or 'question'}") for q in exam_questions)
        metadata = f'<div class="tag-list">{tags([year, variant] + algorithm_list[:3] + component_list[:4])}</div><p>{len(exam_questions)} question{("" if len(exam_questions)==1 else "s")}</p><p>{question_shortcuts}</p>'
        cards.append(card(title, summary, destination, index, "View exam and solutions", metadata, attrs))

        sol = solution_by_id.get(exam_id, {})
        c_path = resolve_index_path(sol.get("current_c_source", ""), LIBRARY) or resolve_index_path(row.get("main_c", ""), LIBRARY)
        asm_path = resolve_index_path(sol.get("current_assembly_source", ""), LIBRARY) or resolve_index_path(row.get("assembly_s", ""), LIBRARY)
        pdf_path = resolve_index_path(row.get("source_pdf", ""), LIBRARY)
        facts = f'''<dl class="fact-grid"><div class="fact"><dt>Date</dt><dd>{esc(row.get('date'))}</dd></div><div class="fact"><dt>Variant</dt><dd>{esc(variant)}</dd></div><div class="fact"><dt>Questions</dt><dd>{len(exam_questions)}</dd></div><div class="fact"><dt>Components</dt><dd>{esc(', '.join(component_list) or 'Core CPU')}</dd></div></dl>'''
        pdf = f'<p>{href(pdf_path, destination, "View exam PDF", "button")}</p>' if pdf_path else '<p class="notice">The source PDF is not present in this copy.</p>'
        qhtml = []
        for number, q in enumerate(exam_questions, 1):
            qtitle = q.get("question", "") or f"Question {number}"
            qsummary = strip_internal(q.get("requirement_summary", ""))
            question_algorithms = split_tags(q.get("algorithm_tags", ""))
            qtags = split_tags(q.get("algorithm_tags", ""), q.get("peripheral_tags", ""), q.get("architecture_tags", ""), q.get("timing_tags", ""))
            related = []
            for tag in question_algorithms:
                match = next((path for label, path in algorithm_links.items() if slug(tag) in slug(label)), None)
                if match:
                    related.append(href(match, destination, f"Study {tag}"))
            question_destination = PORTAL / "exams" / f"{slug(q.get('question_id') or f'{exam_id}-q{number}')}.html"
            qhtml.append(f'<article class="question"><h3>{esc(qtitle)}</h3><p>{esc(qsummary)}</p><div class="tag-list">{tags(qtags)}</div><p>{href(question_destination, destination, f"Read complete solution for {qtitle}")}</p>{("<p>" + " · ".join(related) + "</p>" if related else "")}</article>')

            fields = {"Goal": qsummary, "Data/ABI": q.get("argument_mapping", ""), "Implementation": "Use the exact paper interface, keep hardware ownership in C unless the question assigns it elsewhere, and keep the tested computation bounded."}
            requested_files = q.get("answer_file", "").lower()
            needs_c = any(token in requested_files for token in (".c", "main.c", "sample.c", "irq_"))
            needs_asm = any(token in requested_files for token in (".s", "asm_", "assembly"))
            if not needs_c and not needs_asm:
                needs_c = True
            review = reviews[q["question_id"]]
            dependency = assembly_dependency(review)
            question_raw_dir = GENERATED_SOURCES / "exam-solutions" / slug(q.get("question_id") or f"{exam_id}-q{number}")
            question_c_path = question_raw_dir / "main.c" if needs_c else None
            question_asm_path = question_raw_dir / "assembly.s" if needs_asm or dependency else None
            # Optional reviewed per-question answers override the whole project.
            question_source_dir = c_path.parent / qtitle if c_path else None
            question_notes = question_source_dir / "README.md" if question_source_dir else None
            extra_answer_paths = []
            if question_c_path:
                specific = question_source_dir / "main.c" if question_source_dir else None
                write(question_c_path, source_code(specific if specific and specific.exists() else c_path))
            if question_asm_path:
                specific = question_source_dir / "assembly.s" if question_source_dir else None
                write(question_asm_path, source_code(dependency or (specific if specific and specific.exists() else asm_path)))
            if question_source_dir and question_source_dir.exists():
                for companion in sorted(question_source_dir.glob("IRQ_*.c")):
                    target = question_raw_dir / companion.name
                    write(target, source_code(companion))
                    extra_answer_paths.append(target)
                if question_notes.exists():
                    write(question_raw_dir / "README.md", source_code(question_notes))
            code_sections = ""
            if needs_c:
                code_sections += f'<h2>Complete C answer</h2>{details_code("Show complete C solution", source_code(question_c_path), question_c_path, question_destination, "C", True)}'
            if question_asm_path:
                code_sections += f'<h2>Complete ARM assembly answer</h2>{details_code("Show complete assembly solution", source_code(question_asm_path), question_asm_path, question_destination, "Assembly", True)}'
            for companion in extra_answer_paths:
                code_sections += f'<h2>Complete replacement: {esc(companion.name)}</h2>{details_code("Show complete " + companion.name, source_code(companion), companion, question_destination, "C", True)}'
            relevant_algorithms = [href(path, question_destination, f"Study {label}") for label, path in algorithm_links.items() if any(slug(tag) in slug(label) or slug(label) in slug(tag) for tag in question_algorithms)][:6]
            paper = ROOT / review['paper']
            paper_links = '<p>' + ' · '.join('<a class="button" href="' + esc(rel(paper, question_destination)) + '#page=' + str(n) + '">Original paper — page ' + str(n) + '</a>' for n in review['pages']) + '</p>'
            related = ('<ul>'+''.join(f'<li>{x}</li>' for x in relevant_algorithms)+'</ul>') if relevant_algorithms else '<p>Use the Algorithms and Solution Patterns sections for related methods.</p>'
            notes_link = '<p>' + href(question_raw_dir / 'README.md', question_destination, 'Existing detailed walkthrough and placement table') + '</p>' if question_notes and question_notes.exists() else ''
            question_body = render_question_review(review, code_sections, paper_links, related, notes_link)
            write(question_destination, page(question_destination, f"{title} — {qtitle}", qsummary, question_body, [("Home", HOME), ("Past Exams", index), (title, destination), (qtitle, question_destination)], "Past Exams"))
            items.append({"id": f"question-{slug(q.get('question_id',''))}", "kind": "Past Exams", "title": f"{title} — {qtitle}", "summary": qsummary, "route": rel(question_destination, PORTAL / "search.html"), "examHistory": "Appeared in past exams", "languages": ["Both" if needs_c and question_asm_path else "C" if needs_c else "Assembly"], "components": qtags, "topics": question_algorithms, "aliases": split_tags(q.get("keywords", ""), q.get("function_or_handler", "")), "relatedIds": []})
            question_manifest.append({"questionId": q.get("question_id"), "examId": exam_id, "date": date, "variant": variant, "question": qtitle, "statement": qsummary, "constraints": q.get("constants", ""), "requiredInterface": q.get("architecture", ""), "requiredFiles": [str(path.relative_to(ROOT)).replace("\\", "/") for path in (question_c_path, question_asm_path, *extra_answer_paths) if path], "algorithms": question_algorithms, "components": qtags, "functionsOrHandlers": q.get("function_or_handler", ""), "apiCalls": sorted(set(re.findall(r"\bexam_[A-Za-z0-9_]+(?=\s*\()", (source_code(question_c_path) if question_c_path else "") + (source_code(question_asm_path) if question_asm_path else "")))), "compileStatus": review["verification"]["nativeBuild"]["status"] + ": " + review["verification"]["nativeBuild"]["detail"], "behaviorStatus": review["reviewStatus"] + "; physical board UNVERIFIED", "reviewedOn": review["reviewedOn"], "limitations": review["limitations"]})
        related_patterns = [href(path, destination, label) for label, path in list(pattern_links.items()) if any(slug(token) in slug(label) for token in algorithm_list + component_list)][:8]
        related_algorithms = [href(path, destination, label) for label, path in algorithm_links.items() if any(slug(token) in slug(label) for token in algorithm_list)][:8]
        related_combos = [href(path, destination, label) for label, path in combo_links.items() if any(slug(token) in slug(label) for token in component_list)][:6]
        related_html = "<ul>" + "".join(f"<li>{value}</li>" for value in (related_patterns + related_algorithms + related_combos)) + "</ul>" if related_patterns or related_algorithms or related_combos else "<p>Use the section links above to browse related methods.</p>"
        c_role = f"C owns initialization, the foreground state machine, and these hardware components: {', '.join(component_list) or 'core CPU only'}."
        asm_role = f"Assembly owns the requested computation: {', '.join(algorithm_list) or 'the paper-specific algorithm'}. It must match the C prototype and preserve the ARM calling convention."
        body = f'''<section class="section-block"><h2>Exam overview</h2>{facts}{pdf}</section><section class="section-block"><h2>Questions and complete answers</h2>{''.join(qhtml)}</section><section class="section-block"><h2>Whole-project answer</h2><p><strong>C:</strong> {esc(c_role)}</p><p><strong>Assembly:</strong> {esc(asm_role)}</p>{details_code('Show whole historical C answer', source_code(c_path), c_path, destination, 'C')}{details_code('Show whole historical assembly answer', source_code(asm_path), asm_path, destination, 'Assembly')}</section><section class="section-block"><h2>Related study material</h2>{related_html}</section>'''
        if c_path:
            companions = ''.join(details_code('Show whole-project ' + p.name, source_code(p), p, destination, 'C') for p in sorted(c_path.parent.glob('IRQ_*.c')))
            body += '<section class="section-block"><h2>Whole-project companion files</h2>' + companions + '<p>Use each question page for the exact template placement steps and evidence applicable to that answer.</p></section>' if companions else ''
        whole_notes = c_path.parent / "README.md" if c_path else None
        if whole_notes and whole_notes.exists():
            body = '<section class="section-block">' + markdown_fragment(source_code(whole_notes), whole_notes, destination) + '</section>' + body
        write(destination, page(destination, title, summary, body, [("Home", HOME), ("Past Exams", index), (title, destination)], "Past Exams"))
        items.append({"id": f"exam-{slug(exam_id)}", "kind": "Past Exams", "title": title, "summary": summary, "route": rel(destination, PORTAL / "search.html"), "examHistory": "Appeared in past exams", "languages": ["Both"], "components": component_list, "topics": algorithm_list, "aliases": split_tags(row.get("date", ""), row.get("project", ""), *(q.get("keywords", "") for q in exam_questions)), "relatedIds": []})

    filters = f'''<section class="filter-panel" data-filter-scope><div class="filter-bar"><label>Search exams<input type="search" data-filter="text" placeholder="Question, topic, or hardware"></label><label>Year<select data-filter="year"><option value="">All years</option>{''.join(f'<option>{esc(x)}</option>' for x in sorted(years))}</select></label><label>Variant<select data-filter="variant"><option value="">All variants</option>{''.join(f'<option>{esc(x)}</option>' for x in sorted(variants))}</select></label><label>Component<select data-filter="component"><option value="">All components</option>{''.join(f'<option>{esc(x)}</option>' for x in sorted(components))}</select></label></div><p class="results-note" data-results-note aria-live="polite"></p><div class="grid">{''.join(cards)}</div></section>'''
    write(index, page(index, "Past Exams", SECTION_META["exams"][1], filters, [("Home", HOME), ("Past Exams", index)], "Past Exams"))
    write(GENERATED_SOURCES / "exam-solutions" / "manifest.json", json.dumps({"exams": len(exams), "questions": question_manifest}, indent=2, ensure_ascii=False) + "\n")


def build_patterns(rows: list[dict[str, str]], exams: list[dict[str, str]], solutions: list[dict[str, str]], items: list[dict[str, object]]) -> dict[str, Path]:
    index = PORTAL / "patterns" / "index.html"
    links: dict[str, Path] = {}
    cards = []
    families, languages, histories = set(), set(), set()
    exam_ids = sorted((row.get("exam_id", "") for row in exams), key=len, reverse=True)
    solution_by_id = {row.get("exam_id", ""): row for row in solutions}
    for row in rows:
        title = strip_internal(row.get("title", "")) or "Solution pattern"
        destination = PORTAL / "patterns" / f"{slug(title)}.html"
        family, language, history = pattern_family(row), language_of(row), history_of(row)
        families.add(family); languages.add(language); histories.add(history)
        links[title] = destination
        summary = f"A reusable {family.lower()} method: recognize the shape, map inputs and outputs, then implement it safely."
        clues = split_tags(row.get("tag", ""), row.get("family", ""), title)
        fragment = pattern_guidance(family, title, clues)
        relationship_ids = split_tags(row.get("exam_ids", ""))
        related_exam_ids = []
        for relationship_id in relationship_ids:
            related_exam_id = next((value for value in exam_ids if relationship_id == value or relationship_id.startswith(value + "-Q")), "")
            if related_exam_id and related_exam_id not in related_exam_ids:
                related_exam_ids.append(related_exam_id)
        fragment += "<p>The complete baseline below is the implementation for this pattern. Related exams are supporting references.</p>"
        appeared = split_tags(row.get("exam_ids", ""))
        exam_links = []
        linked_exam_ids = []
        for relationship_id in appeared:
            exam_id = next((value for value in exam_ids if relationship_id == value or relationship_id.startswith(value + "-Q")), "")
            if exam_id and exam_id not in linked_exam_ids:
                linked_exam_ids.append(exam_id)
                target = PORTAL / "exams" / f"{slug(exam_id)}.html"
                exam_links.append(href(target, destination, exam_id))
        body = f'''<section class="section-block"><dl class="fact-grid"><div class="fact"><dt>Problem family</dt><dd>{esc(family)}</dd></div><div class="fact"><dt>Language</dt><dd>{esc(language)}</dd></div><div class="fact"><dt>Exam history</dt><dd>{esc(public_history(history))}</dd></div></dl></section><section class="section-block lesson-content">{fragment}</section><section class="section-block"><h2>Exams where it appeared</h2>{('<ul>'+''.join(f'<li>{x}</li>' for x in exam_links)+'</ul>') if exam_links else '<p>This is a possible variation or extra-practice pattern.</p>'}</section>'''
        write(destination, page(destination, title, summary, body, [("Home", HOME), ("Solution Patterns", index), (title, destination)], "Solution Patterns"))
        attrs = f'data-filter-item data-family="{esc(family)}" data-language="{esc(language)}" data-history="{esc(public_history(history))}"'
        cards.append(card(title, summary, destination, index, "Read solution method", f'<div class="tag-list">{tags([family, language, public_history(history)])}</div>', attrs))
        items.append({"id": f"pattern-{slug(title)}", "kind": "Solution Patterns", "title": title, "summary": summary, "route": rel(destination, PORTAL / "search.html"), "examHistory": public_history(history), "languages": [language], "components": split_tags(row.get("tag", ""), row.get("family", "")), "topics": [family], "aliases": split_tags(row.get("tag", ""), title), "relatedIds": []})
    body = f'''<section class="filter-panel" data-filter-scope><div class="filter-bar"><label>Search patterns<input type="search" data-filter="text" placeholder="Problem shape or clue"></label><label>Problem family<select data-filter="family"><option value="">All families</option>{''.join(f'<option>{esc(x)}</option>' for x in sorted(families))}</select></label><label>Language<select data-filter="language"><option value="">All languages</option>{''.join(f'<option>{esc(x)}</option>' for x in sorted(languages))}</select></label><label>Exam history<select data-filter="history"><option value="">All history</option>{''.join(f'<option>{esc(public_history(x))}</option>' for x in sorted(histories))}</select></label></div><p class="results-note" data-results-note aria-live="polite"></p><div class="grid">{''.join(cards)}</div></section>'''
    write(index, page(index, "Solution Patterns", SECTION_META["patterns"][1], body, [("Home", HOME), ("Solution Patterns", index)], "Solution Patterns"))
    return links


def algorithm_family(title: str) -> str:
    text = title.lower()
    rules = [
        ("ARM ABI and memory", ("asm", "memory", "memmove", "argument", "stack", "packed", "transpose")),
        ("Graphs", ("graph", "bfs", "dfs", "dijkstra", "component", "union", "kruskal", "prim", "bellman", "floyd", "topological", "bipartite")),
        ("Sorting", ("sort", "quicksort", "partition")),
        ("Trees and heaps", ("tree", "heap", "priority queue", "bst")),
        ("Strings", ("string", "substring", "token", "palindrome", "character")),
        ("Recursion and dynamic programming", ("recurrence", "knapsack", "coin", "edit distance", "fibonacci", "subset", "lcs", "memo")),
        ("Arithmetic and number theory", ("gcd", "lcm", "prime", "sqrt", "power", "division", "decimal", "base conversion", "factorial", "modular")),
        ("Bits and fixed-point work", ("bit", "popcount", "parity", "saturat", "fixed", "rotate", "overflow", "crc")),
        ("Embedded streams and signals", ("moving average", "filter", "debounce", "hysteresis", "waveform", "quantization", "edge detection", "lcg")),
        ("State machines and timing", ("state", "event", "timeout", "schedule", "timestamp", "producer", "rate division")),
        ("Data structures", ("linked", "queue", "deque", "ring buffer", "hash table", "stack")),
        ("Mazes and backtracking", ("maze", "flood", "a-star", "permutation", "combination", "backtracking")),
        ("Searching and selection", ("search", "select", "majority", "bound", "occurrence")),
        ("Arrays and matrices", ("array", "matrix", "histogram", "prefix", "window", "two pointer", "rotation", "reversal", "extrema", "reduction", "horner", "run-length")),
    ]
    return next((family for family, words in rules if any(word in text for word in words)), "Arrays and matrices")


def clean_algorithm_code(code: str, public_slug: str) -> str:
    """Remove maintenance identifiers from public source without changing behavior."""
    names = sorted(set(re.findall(r"\bpat_(?:alg|data|ds|mem)_[a-z0-9_]+_001(?=\b|_)", code)), key=len, reverse=True)
    replacement = "algorithm_" + public_slug.replace("-", "_")
    for number, name in enumerate(names):
        code = re.sub(rf"\b{re.escape(name)}(?=\b|_)", replacement if number == 0 else f"{replacement}_variant_{number}", code)
    code = re.sub(r"(?im)^\s*;?\s*Verification status:.*$", "", code)
    return code


def read_algorithm_source(folder: Path) -> dict[str, object]:
    readme = source_code(folder / "README.md")
    heading = next((line for line in readme.splitlines() if line.startswith("# ")), folder.name)
    title = heading.split(":", 1)[-1].strip() if ":" in heading else heading[2:].strip()
    recognition_match = re.search(r"## Recognition phrases\s+(.*?)(?=\n## )", readme, re.S)
    procedure_match = re.search(r"## Pseudocode\s+(.*?)(?=\n## )", readme, re.S)
    complexity_match = re.search(r"## Complexity\s+(.*?)(?=\n## )", readme, re.S)
    history = "Extra practice" if "No historical occurrence is claimed" in readme else "Appeared in past exams"
    public_slug = slug(title)
    c_code = source_code(folder / "c" / "reference.c").split("#ifdef PATTERN_HOST_TEST")[0]
    asm_code = source_code(folder / "arm" / "implementation.s")
    recognition = re.sub(r"\s+", " ", recognition_match.group(1)).strip() if recognition_match else f"The question has the same input, output, and stopping rule as {title.lower()}."
    procedure = procedure_match.group(1).strip() if procedure_match else "1. Validate the contract.\n2. Establish the invariant.\n3. Run the bounded update.\n4. Return the documented result."
    complexity = re.sub(r"\s+", " ", complexity_match.group(1)).strip() if complexity_match else "See the implementation for its exact loop and storage bounds."
    return {"title": title, "slug": public_slug, "recognition": recognition, "procedure": procedure, "complexity": complexity, "history": history, "c": c_code, "assembly": asm_code, **source_details(folder)}


def procedure_html(text: str) -> str:
    steps = [re.sub(r"^\s*\d+[.)]\s*", "", line).strip() for line in text.splitlines() if re.match(r"^\s*\d+[.)]", line)]
    if not steps:
        return f"<p>{esc(re.sub(r'\s+', ' ', text).strip())}</p>"
    return "<ol>" + "".join(f"<li>{esc(step)}</li>" for step in steps) + "</ol>"


def algorithm_test_vectors(family: str) -> str:
    cases = {
        "Sorting": [("Empty", "[]", "[]; no read"), ("One", "[7]", "[7]"), ("Duplicates", "[3,1,3,1]", "[1,1,3,3]"), ("Boundary", "INT_MIN, 0, INT_MAX", "signed order without subtraction overflow")],
        "Searching and selection": [("Empty", "n=0", "not-found result"), ("One", "[7], key 7", "index 0"), ("Duplicates", "[1,2,2,4], key 2", "document first, last, or range"), ("Boundary", "key INT_MIN / INT_MAX", "comparison remains defined")],
        "Graphs": [("Empty", "V=0", "empty result; no vertex read"), ("One", "one vertex, no edges", "one reachable component"), ("Repeated edge", "two equal edges", "no duplicate visit or double union"), ("Boundary", "unreachable distance=INT_MAX", "never add to infinity")],
        "Mazes and backtracking": [("Empty", "0x0 grid", "failure without access"), ("One", "start equals goal", "path length zero"), ("Blocked", "goal surrounded", "no path"), ("Boundary", "queue/stack at capacity", "no write past scratch space")],
        "Strings": [("Empty", '""', "length zero / empty output"), ("One", '"A"', "one character plus terminator"), ("Repeated", '"AAAA"', "all occurrences handled"), ("Boundary", "capacity exactly length+1", "terminator fits")],
        "Arithmetic and number theory": [("Zero", "0", "documented zero result"), ("One", "1", "base case"), ("Repeated factor", "36", "2,2,3,3 or requested aggregate"), ("Boundary", "UINT_MAX / INT limits", "widen, clamp, or reject before overflow")],
        "Bits and fixed-point work": [("Zero", "0x00000000", "all bits clear"), ("One bit", "0x80000000", "width-accurate result"), ("Repeated bits", "0xFFFFFFFF", "all positions handled"), ("Boundary", "shift 0 and word width", "no undefined full-width shift")],
    }
    rows = cases.get(family, [("Empty", "count=0", "no dereference and documented result"), ("One", "one valid element", "direct base path"), ("Duplicate", "repeated equal values", "consume/count exactly as promised"), ("Boundary", "maximum capacity and integer limits", "no out-of-bounds access or undefined overflow")])
    return '<table><thead><tr><th>Case</th><th>Input</th><th>Expected check</th></tr></thead><tbody>' + ''.join(f'<tr><td>{esc(name)}</td><td><code>{esc(value)}</code></td><td>{esc(expected)}</td></tr>' for name, value, expected in rows) + '</tbody></table>'


def build_algorithms(exams: list[dict[str, str]], items: list[dict[str, object]]) -> dict[str, Path]:
    index = PORTAL / "algorithms" / "index.html"
    raw_root = GENERATED_SOURCES / "algorithms"
    links: dict[str, Path] = {}
    cards: list[str] = []
    inventory = []
    fundamental_links: list[tuple[str, str, Path]] = []
    families: set[str] = set()
    legacy_tests = {e["slug"]: e["test"] for e in legacy_test_entries()}
    primary = [read_algorithm_source(folder) for folder in sorted(ALGORITHM_LIBRARY.iterdir()) if folder.is_dir() and (folder / "c" / "reference.c").exists()]
    by_source = {folder.name: data for folder, data in zip([f for f in sorted(ALGORITHM_LIBRARY.iterdir()) if f.is_dir() and (f / "c" / "reference.c").exists()], primary)}
    entries: list[dict[str, object]] = []
    for data in primary:
        entries.append({**data, "family": algorithm_family(str(data["title"])), "summary": data["contract"], "test": legacy_tests[data["source_id"].lower()], "questions": []})
    for source_name, variant_title, variant_family, variant_focus, variant_complexity in ALGORITHM_VARIANTS:
        source = by_source.get(source_name)
        if not source:
            raise SystemExit(f"Missing algorithm source for {variant_title}")
        entry = {**source, "title": variant_title, "family": variant_family, "focus": variant_focus, "complexity": variant_complexity, "slug": slug(variant_title), "recognition": variant_focus, "summary": variant_focus, "history": "Possible variation", "questions": [], "shared_source": True, "test": legacy_tests[source["source_id"].lower()]}
        primary_name=source_name.lower().replace("-", "_")
        suffix=VARIANT_SUFFIX.get(variant_title,"")
        entry["focus_entry"]=primary_name+suffix
        if variant_title=="Seven-argument component merge":
            entry["title"]="Five-argument component-label replacement"
            entry["summary"]="A bounded label-replacement helper with its fifth argument on the stack."
            entry["recognition"]=entry["summary"]
        # Variants share the tested source; their actual complexity is unchanged.
        entry["complexity"]=source["complexity"]
        entries.append(entry)
    for extra in [*EXTRA_ALGORITHMS, *NEW_ALGORITHMS]:
        entries.append({**extra, "assembly": extra.get("assembly", ""), "procedure": extra["method"], "recognition": extra["recognition"]})
    if len(entries) < 100:
        raise SystemExit(f"Expected at least 100 substantive algorithms, found {len(entries)}")
    for data in entries:
        title = str(data["title"])
        public_slug = str(data.get("slug") or slug(title))
        destination = PORTAL / "algorithms" / f"{public_slug}.html"
        if destination in links.values():
            title = f"{title} — focused method"
            public_slug = f"{public_slug}-focused-method"
            destination = PORTAL / "algorithms" / f"{public_slug}.html"
        links[title] = destination
        family = str(data.get("family") or algorithm_family(title))
        families.add(family)
        history = str(data.get("history") or "Extra practice")
        c_code = readable_c(clean_algorithm_code(str(data["c"] if "c" in data else data["code"]), public_slug))
        asm_code = clean_algorithm_code(str(data.get("assembly", "")), public_slug)
        raw_dir = raw_root / public_slug
        c_path = raw_dir / "reference.c"
        asm_path = raw_dir / "implementation.s" if asm_code.strip() else None
        write(c_path, c_code)
        if asm_path:
            write(asm_path, asm_code)
        recognition = str(data.get("recognition") or data.get("summary") or title)
        method = str(data.get("procedure") or data.get("method") or "Validate inputs, maintain the invariant, stop at the documented bound, and return the result.")
        complexity = str(data.get("complexity") or "The implementation states its exact time and storage bounds.")
        vector_table = algorithm_test_vectors(family)
        data["family"]=family
        for field in ("prototype","focus_entry"):
            data[field]=clean_algorithm_code(str(data.get(field,"")),public_slug)
        fixture=readable_c(clean_algorithm_code(str(data.get("test","")),public_slug))
        test_path=raw_dir/"test_vectors.c"
        # Fixtures can run on a host with the reference, or as test_main in a simulator.
        fixture = "#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)\n" + fixture
        write(test_path,fixture)
        if not asm_path: raise ValueError("Assembly missing for "+public_slug)
        questions = [str(q) for q in data.get("questions", [])]
        exam_links = [href(PORTAL / "exams" / f"{slug(q)}.html", destination, q) for q in questions]
        asm_section = details_code("Show ARM assembly implementation", asm_code, asm_path, destination, "Assembly") if asm_path else "<p>This entry is kept in C because its allocation, library, or graph bookkeeping would make a standalone assembly listing less useful than the ABI-focused implementations elsewhere in this handbook.</p>"
        inventory.append({"slug":public_slug,"title":title,"source_group":data.get("source_id",public_slug),
                          "shared_source":bool(data.get("shared_source")),"history":history,
                          "fundamentals_group":data.get("fundamentals_group", ""),
                          "focus_entry":data.get("focus_entry",""),"prototype":data.get("prototype",""),
                          "assembly_exports":re.findall(r"(?m)^\s*EXPORT\s+(\w+)",asm_code),
                          "reference":c_path.relative_to(ROOT).as_posix(),
                          "assembly":asm_path.relative_to(ROOT).as_posix()})
        body = algorithm_page_body(data,c_code,asm_code,fixture,c_path,asm_path,test_path,destination,details_code,href)
        write(destination, page(destination, title, str(data.get("summary") or recognition), body, [("Home", HOME), ("Algorithms", index), (title, destination)], "Algorithms"))
        attrs = f'data-filter-item data-family="{esc(family)}" data-language="{esc("Both" if asm_path else "C")}" data-history="{esc(history)}"'
        cards.append(card(title, str(data.get("summary") or recognition), destination, index, "Study algorithm", f'<div class="tag-list">{tags([family, "Both" if asm_path else "C", history])}</div>', attrs))
        items.append({"id": f"algorithm-{public_slug}", "kind": "Algorithms", "title": title, "summary": str(data.get("summary") or recognition), "route": rel(destination, PORTAL / "search.html"), "examHistory": history, "languages": ["Both" if asm_path else "C"], "components": [], "topics": [family, title], "aliases": split_tags(title, recognition), "relatedIds": []})
        if data.get("fundamentals_group"):
            fundamental_links.append((str(data["fundamentals_group"]), title, destination))
    basics = PORTAL / "algorithms" / "basic-exam-algorithms.html"
    group_order = ["Count and measure", "Compare and test", "Copy and move", "Search", "Transform", "Strings", "Arithmetic", "Bits and bytes", "Matrices"]
    basic_sections = []
    for group in group_order:
        links_in_group = [(title, destination) for entry_group, title, destination in fundamental_links if entry_group == group]
        if links_in_group:
            basic_sections.append(f'<section class="section-block"><h2>{esc(group)}</h2><ul>' + ''.join(f'<li>{href(destination, basics, title)}</li>' for title, destination in links_in_group) + '</ul></section>')
    basic_body = f'<section class="notice"><strong>{len(fundamental_links)} separate exam prompts.</strong> Each link opens one question with its own contract, ARMASM, matching C, register map, trace, and executable tests.</section>' + ''.join(basic_sections)
    write(basics, page(basics, "Basic Exam Algorithms", "Direct links to one-prompt fundamentals.", basic_body, [("Home", HOME), ("Algorithms", index), ("Basic Exam Algorithms", basics)], "Algorithms"))
    body = f'''<section class="notice"><strong>{len(entries)} one-prompt study entries:</strong> every entry includes ARM assembly, matching C, its contract, a worked trace, and expected-output tests. {href(basics, index, f'Open the {len(fundamental_links)}-entry Basic Exam Algorithms index')}.</section><section class="filter-panel" data-filter-scope><div class="filter-bar"><label>Search algorithms<input type="search" data-filter="text" placeholder="Quicksort, array length, string append, matrix trace..."></label><label>Problem family<select data-filter="family"><option value="">All families</option>{''.join(f'<option>{esc(x)}</option>' for x in sorted(families))}</select></label><label>Language<select data-filter="language"><option value="">All languages</option><option>C</option><option>Both</option></select></label><label>Exam history<select data-filter="history"><option value="">All history</option><option>Appeared in past exams</option><option>Possible variation</option><option>Extra practice</option></select></label></div><p class="results-note" data-results-note aria-live="polite"></p><div class="grid">{''.join(cards)}</div></section>'''
    write(ALGORITHM_INVENTORY_OUTPUT,json.dumps(inventory,indent=2)+"\n")
    write(index, page(index, "Algorithms", SECTION_META["algorithms"][1], body, [("Home", HOME), ("Algorithms", index)], "Algorithms"))
    return links


def api_components(group: str, title: str) -> list[str]:
    raw = f"{group} {title}".lower()
    mapping = {"led": "LED", "button": "Buttons", "joystick": "Joystick", "timer": "Timer", "rit": "RIT", "systick": "SysTick", "adc": "ADC", "potentiometer": "ADC", "dac": "DAC", "sound": "DAC", "svc": "SVC", "event": "Events"}
    return [label for needle, label in mapping.items() if needle in raw]


def api_task(group: str, title: str) -> str:
    raw = f"{group} {title}".lower()
    tasks = [
        ("Show a value on LEDs", "led"), ("Read buttons without bounce", "button"),
        ("Detect joystick edges", "joystick"), ("Measure time or capture an interval", "timer"),
        ("Schedule periodic work", "rit"), ("Schedule periodic work", "systick"),
        ("Read and scale ADC values", "adc"), ("Read and scale ADC values", "potentiometer"),
        ("Generate DAC output or sound", "dac"), ("Transfer work from IRQ to main", "event"),
        ("Transfer work from IRQ to main", "critical"),
    ]
    return next((task for task, needle in tasks if needle in raw), "Start the board safely")


def api_parameters(declaration: str) -> list[tuple[str, str]]:
    match = re.search(r"\((.*)\)", declaration)
    if not match or match.group(1).strip() in {"", "void"}:
        return []
    result = []
    for parameter in match.group(1).split(","):
        parameter = parameter.strip()
        name_match = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*$", parameter)
        name = name_match.group(1) if name_match else "value"
        result.append((name, parameter[: name_match.start()].strip() if name_match else parameter))
    return result



def api_sidebar(records: list[dict[str, object]], source: Path, current: str = "") -> str:
    groups: list[str] = []
    for record in records:
        group = str(record["group"])
        if group not in groups:
            groups.append(group)
    sections = []
    index = PORTAL / "api" / "index.html"
    for group in groups:
        entries = []
        for record in records:
            if str(record["group"]) != group:
                continue
            name = str(record["title"])
            target = PORTAL / "api" / f"{slug(name)}.html"
            active = ' aria-current="page"' if name == current else ""
            entries.append(f'<li data-api-entry><a href="{rel(target, source)}"{active}><code>{esc(name)}</code></a></li>')
        sections.append(
            f'<section data-api-group><h3><a href="{rel(index, source, "api-group-" + slug(group))}">{esc(group)}</a></h3>'
            f'<ul>{"".join(entries)}</ul></section>'
        )
    return f'''<aside class="api-sidebar" aria-label="API reference navigation">
      <label for="api-nav-search-{slug(current or 'index')}">Filter API functions</label>
      <input id="api-nav-search-{slug(current or 'index')}" type="search" data-api-nav-search placeholder="timer, ADC, events...">
      <p class="api-nav-count" data-api-nav-count aria-live="polite"></p>
      <nav>{''.join(sections)}</nav>
    </aside>'''


def definition_table(values: list[tuple[str, str]], first_heading: str) -> str:
    rows = ''.join(f'<tr><td><code>{esc(name)}</code></td><td>{esc(meaning)}</td></tr>' for name, meaning in values)
    return f'<table><thead><tr><th>{esc(first_heading)}</th><th>Meaning</th></tr></thead><tbody>{rows}</tbody></table>'


def exam_evidence(exams: list[str], destination: Path) -> str:
    if not exams:
        return ""
    links = ", ".join(href(PORTAL / "exams" / f"{exam}.html", destination, exam) for exam in exams)
    return f' <span class="api-value-evidence">Reviewed exam: {links}</span>'


def api_value_guidance(name: str, destination: Path) -> str:
    rows = []
    for item in VALUE_GUIDANCE[name]:
        rows.append(
            f'<tr><td><code>{esc(item["value"])}</code></td><td>{esc(item["use"])}</td>'
            f'<td><span class="evidence-badge">{esc(item["basis"])}</span>{exam_evidence(item["exams"], destination)}</td></tr>'
        )
    return '<table class="api-value-table"><thead><tr><th>Suggested value</th><th>When to use</th><th>Evidence</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'


def api_scenario_usage(name: str, destination: Path) -> str:
    matching = [scenario for scenario in SCENARIOS if name in scenario["functions"]]
    cards = []
    for scenario in matching:
        cards.append(
            f'<article class="api-scenario" id="scenario-{esc(scenario["id"])}"><h3>{esc(scenario["title"])}</h3>'
            f'<p class="api-scenario-basis">{esc(scenario["basis"])}{exam_evidence(scenario["exams"], destination)}</p>'
            f'<pre tabindex="0"><code class="language-c">{esc(scenario["code"])}</code></pre></article>'
        )
    return ''.join(cards)


def build_api(records: list[dict[str, object]], items: list[dict[str, object]]) -> dict[str, Path]:
    index = PORTAL / "api" / "index.html"
    write(API_REFERENCE, render_quick_reference(records))
    write(API_GAP_REPORT, render_gap_report())
    links: dict[str, Path] = {}
    ordered_names = [str(record["title"]) for record in records]
    for position, record in enumerate(records):
        group, title = str(record["group"]), str(record["title"])
        destination = PORTAL / "api" / f"{slug(title)}.html"
        links[title] = destination
        doc = API_DOCS[title]
        description = str(doc["summary"])
        declaration = str(record["declaration"])
        declared_params = api_parameters(declaration)
        param_docs = doc["params"]
        if declared_params:
            parameter_rows = ''.join(
                f'<tr><td><code>{esc(name)}</code></td><td><code>{esc(type_name)}</code></td>'
                f'<td>{esc(param_docs[name]["direction"])}</td><td>{esc(param_docs[name]["description"])}</td></tr>'
                for name, type_name in declared_params
            )
            parameter_table = (
                '<table><thead><tr><th>Parameter</th><th>Type</th><th>Direction</th><th>Meaning and valid values</th></tr></thead>'
                f'<tbody>{parameter_rows}</tbody></table>'
            )
        else:
            parameter_table = '<p class="api-none">This function has no parameters.</p>'
        related = [name for name in doc["related"] if name in links or name in ordered_names]
        related_links = ''.join(
            f'<li>{href(PORTAL / "api" / f"{slug(name)}.html", destination, name)}</li>' for name in related
        ) or '<li>No direct companion call.</li>'
        previous_link = ""
        next_link = ""
        if position > 0:
            previous_name = ordered_names[position - 1]
            previous_link = href(PORTAL / "api" / f"{slug(previous_name)}.html", destination, f"Previous: {previous_name}")
        if position + 1 < len(ordered_names):
            next_name = ordered_names[position + 1]
            next_link = href(PORTAL / "api" / f"{slug(next_name)}.html", destination, f"Next: {next_name}")
        body = f'''<div class="api-shell">{api_sidebar(records, destination, title)}<article class="api-content">
          <section class="api-signature"><div class="tag-list">{tags([group] + api_components(group, title))}</div><h2>Exact declaration</h2><pre tabindex="0"><code class="language-c">{esc(declaration)}</code></pre></section>
          <section class="section-block"><h2>Contract</h2><h3>Preconditions</h3><p>{esc(doc['preconditions'])}</p><h3>Parameters</h3>{parameter_table}<h3>Return value</h3><p>{esc(doc['returns'])}</p><h3>Side effects</h3><p>{esc(doc['side_effects'])}</p><h3>Timing and call context</h3><p>{esc(doc['context'])}</p></section>
          <section class="section-block"><h2>Typical exam values</h2><p>Use the evidence label before copying a number: observed values come from reviewed solutions; maintained recipes and safe illustrations are explicitly identified.</p>{api_value_guidance(title, destination)}</section>
          <section class="section-block"><h2>Scenario usage</h2>{api_scenario_usage(title, destination)}</section>
          <section class="section-block"><h2>Minimal example</h2><pre tabindex="0"><code class="language-c">{esc(doc['example'])}</code></pre><div class="api-warning"><h3>Common mistake</h3><p>{esc(doc['mistake'])}</p></div><div class="api-exam-note"><h3>Exam use</h3><p>{esc(doc['exam_note'])}</p></div></section>
          <section class="section-block"><h2>Related functions</h2><ul class="api-related">{related_links}</ul><h2>Authoritative source</h2><p>{href(API_HEADER, destination, 'Read the current exam_api.h declaration')} · {href(API_REFERENCE, destination, 'Read the complete generated Markdown reference')}</p><p>{href(PORTAL / 'guides' / 'choose-interface.html', destination, 'Choose API versus professor functions versus registers')}</p></section>
          <nav class="api-pager" aria-label="Adjacent API functions"><span>{previous_link}</span><span>{next_link}</span></nav>
        </article></div>'''
        write(destination, page(destination, title, description, body, [("Home", HOME), ("API", index), (title, destination)], "API"))
        components = api_components(group, title)
        items.append({
            "id": f"api-{slug(title)}", "kind": "API", "title": title,
            "summary": description, "route": rel(destination, PORTAL / "search.html"),
            "examHistory": "Possible variation", "languages": ["C"], "components": components,
            "topics": [group, declaration, str(doc["exam_note"])] + [str(item["value"]) + " " + str(item["use"]) for item in VALUE_GUIDANCE[title]] + [str(scenario["title"]) for scenario in SCENARIOS if title in scenario["functions"]],
            "aliases": split_tags(title.replace("_", " "), str(doc["summary"])),
            "relatedIds": [f"api-{slug(name)}" for name in related],
        })

    group_sections = []
    for group in GROUP_ORDER:
        group_records = [record for record in records if str(record["group"]) == group]
        if not group_records:
            continue
        rows = ''.join(
            f'<tr><td>{href(PORTAL / "api" / f"{slug(str(record["title"]))}.html", index, str(record["title"]))}</td>'
            f'<td>{esc(API_DOCS[str(record["title"])]["summary"])}</td></tr>'
            for record in group_records
        )
        group_sections.append(
            f'<section id="api-group-{slug(group)}" class="section-block api-group-section"><h2>{esc(group)}</h2>'
            f'<p>{esc(GROUP_DESCRIPTIONS[group])}</p><table><thead><tr><th>Function</th><th>Purpose</th></tr></thead><tbody>{rows}</tbody></table></section>'
        )
    gap_items = ''.join(f'<li>{esc(item)}</li>' for item in LEGACY_GAPS)
    from peripheral_helper_docs import TIMER_BEHAVIOUR
    timer_effects = '<table><thead><tr><th>Call</th><th>Counter</th><th>Configuration and interrupts</th></tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+esc(value)+'</td>' for value in row)+'</tr>' for row in TIMER_BEHAVIOUR) + '</tbody></table>'
    overview = f'''<div class="api-shell">{api_sidebar(records, index)}<article class="api-content">
      <section class="notice"><strong>Current interface:</strong> all {len(records)} function pages are generated from the current official header and this reference's validated function-specific contracts.</section>
      <p class="api-actions">{href(STARTING_TEMPLATE / 'sample.uvprojx', index, 'Open the Official Combined Exam API project', 'button')} {href(API_REFERENCE, index, 'Open the complete Markdown reference', 'button')} {href(API_GAP_REPORT, index, 'Open the API gap report', 'button')}</p>
      <section class="section-block"><h2>Required include and initialization</h2><pre tabindex="0"><code class="language-c">#include &quot;exam_api.h&quot;

int main(void) {{
  exam_init();
  /* Initialize only the peripherals required by the question. */
  for (;;) {{ __WFI(); }}
}}</code></pre><p><code>exam_init()</code> initializes system and LED support and clears API software state. It does not initialize or start every peripheral.</p></section>
      <section class="section-block"><h2>Ownership and data flow</h2><ol><li>Use one owner for each peripheral and each IRQ vector.</li><li>Initialize shared state, clear pending hardware state, enable interrupts, and start the time source last.</li><li>In the IRQ, acknowledge the real source and capture a small value or publish an event.</li><li>In <code>main()</code>, atomically take that state and perform longer processing.</li></ol><div class="api-rule-grid"><div><strong>Timer / RIT</strong><span>Configuration leaves the counter stopped; start explicitly.</span></div><div><strong>SysTick</strong><span>Successful configuration starts it immediately.</span></div><div><strong>ADC</strong><span>Start → IRQ capture → foreground take.</span></div><div><strong>Buttons</strong><span>Choose raw acknowledgement or one debounce workflow.</span></div></div></section>
      <section class="section-block"><h2>Exam-grounded values and scenarios</h2><p>Every function page now separates evidence from teaching defaults. A number observed in one question is not automatically correct for another clock, timer mode, or requirement.</p><div class="api-evidence-key"><div><strong>Observed in reviewed solutions</strong><span>Linked to the maintained solved exam where the value or pattern appears.</span></div><div><strong>Recommended maintained recipe</strong><span>A practical package default, such as 10 ms sampling and 50 ms button confirmation, not a claimed paper constant.</span></div><div><strong>Safe illustration or API contract</strong><span>Valid current-template usage with no claim that a reviewed exam used that exact value.</span></div></div></section>
      <section class="section-block"><h2>Status values</h2>{definition_table(STATUS_VALUES, 'Value')}<h2>Public types</h2>{definition_table(PUBLIC_TYPES, 'Type')}<h2>Public constants</h2>{definition_table(PUBLIC_CONSTANTS, 'Constant')}<h2>Public fault globals</h2>{definition_table(PUBLIC_GLOBALS, 'Global')}</section>
      <section class="section-block"><h2>Choose the correct interface</h2><table><thead><tr><th>Situation</th><th>Use</th></tr></thead><tbody><tr><td>The Combined API is permitted</td><td>Use the declarations documented here exactly.</td></tr><tr><td>The paper supplies a named function</td><td>Use the professor's exact interface.</td></tr><tr><td>The paper tests registers or handler ownership</td><td>Use the required native/register implementation.</td></tr></tbody></table><p class="notice">Never configure the same timer, interrupt, or peripheral through two interfaces.</p></section>
      <section class="section-block"><h2>Capabilities not present in the current API</h2><p>These older conveniences are intentionally reported as gaps, not restored or presented as current declarations.</p><ul>{gap_items}</ul></section>
      <section class="section-block"><h2>Timer call effects</h2>{timer_effects}<p>Basic tick, millisecond and hertz configuration sets PR=0. Apply advanced prescaler and clock-divider changes afterward, while stopped. Preserve a paper's exact tick thresholds.</p></section>
      <section><h2>Function groups</h2>{''.join(group_sections)}</section>
    </article></div>'''
    write(index, page(index, "Official Combined Exam API", "Source-grounded reference for every current function, type, constant, ownership rule, and interrupt boundary.", overview, [("Home", HOME), ("API", index)], "API"))
    return links



def guide_body(key: str, peripheral_cards: str, destination: Path) -> str:
    route = lambda section, label: href(PORTAL / section / "index.html", destination, label)
    content = {
        "start-from-zero": f'''<h2>Use this order</h2><ol><li>{route('guides','Read the goal-based guides')}</li><li>{route('exams','Open one past exam')}</li><li>{route('patterns','Find its problem shape')}</li><li>{route('api','Check the sole Official Combined API')}</li></ol><p class="notice">Start with one complete question. Do not try to memorize the whole library before solving anything.</p>''',
        "solve-a-past-exam": f'''<h2>Exam workflow</h2><ol><li>Read the PDF and rewrite the required input, output, constants, and timing in plain language.</li><li>Choose a {route('patterns','solution pattern')} and, if needed, an {route('algorithms','algorithm family')}.</li><li>Decide whether the paper expects the supplied API, professor functions, or direct registers.</li><li>When the supplied API is allowed, confirm every declaration in the {route('api','Official Combined API quick reference')}.</li><li>Write C first when possible, translate only the requested computation to assembly, then test edge cases.</li></ol>''',
        "start-a-working-project": '''<h2>Safe starting sequence</h2><ol><li>Copy the supplied starting template for the chosen exam.</li><li>Keep the existing project files and startup code in place.</li><li>Edit only the answer surfaces requested by the question.</li><li>Build once before adding logic so setup failures are separated from answer failures.</li><li>Add one feature at a time and rebuild.</li></ol><p class="notice">Use relative package paths. Do not rename startup, project, or board-support files unless the exam explicitly requires it.</p>''',
        "learn-c": f'''<h2>What to learn first</h2><ol><li>Types, constants, expressions, and integer limits</li><li><code>if</code>, loops, and bounded iteration</li><li>Arrays, pointers, and indexes</li><li>Functions, return values, and output parameters</li><li><code>volatile</code> shared event state</li></ol><p>Practice each skill through {route('patterns','solution patterns')} and the C skeletons in {route('algorithms','algorithms')}.</p>''',
        "learn-assembly": f'''<h2>What to learn first</h2><ol><li>Registers, flags, loads, stores, and addresses</li><li>Compare, branch, and counted loops</li><li>Stack alignment and the ARM calling convention</li><li>The fifth argument and later arguments on the stack</li><li>Preserving registers and returning values safely</li></ol><p>Use the assembly considerations in {route('patterns','solution patterns')} and compare them with reviewed exam solutions.</p>''',
        "use-peripherals": f'''<h2>Learn one responsibility at a time</h2><p>All 14 lessons below were rewritten for the sole Official Combined Exam API. Each lesson uses declarations present in its canonical header and states when direct registers are still required.</p><div class="grid">{peripheral_cards}</div><p>{route('api','Read the Official Combined Exam API quick reference')}</p>''',
        "combine-c-and-assembly": f'''<h2>Ownership rule</h2><p>Let C own initialization, interrupts, timers, and peripherals. Give assembly a clear computation with explicit arguments and results unless the question says otherwise.</p><ol><li>Write the C prototype.</li><li>Map arguments 1–4 to registers and later arguments to the stack.</li><li>Preserve required registers and stack alignment.</li><li>Return one result in <code>r0</code> or write through an explicit pointer.</li><li>Test the C call with the smallest and largest inputs.</li></ol><p>{route('patterns','Find ABI and stack patterns')}</p>''',
        "choose-interface": f'''<h2>Choose one interface per resource</h2><dl class="fact-grid"><div class="fact"><dt>Official Combined API</dt><dd>Use the sole supplied template when the exam permits its helpers.</dd></div><div class="fact"><dt>Professor functions</dt><dd>Use their exact names, declarations, behavior, and ownership when supplied by the question.</dd></div><div class="fact"><dt>Direct registers</dt><dd>Use only when the question requires register-level configuration or the supplied interface does not cover the task.</dd></div></dl><p class="notice">Do not configure the same timer, interrupt, or peripheral through two interfaces.</p><p>{route('api','Browse the Official Combined API quick reference')}</p>''',
        "debug-common-failures": '''<h2>Debug in this order</h2><ol><li><strong>Build:</strong> check the first compiler or linker error, not the last.</li><li><strong>Call boundary:</strong> confirm prototypes, argument order, stack arguments, and preserved registers.</li><li><strong>Initialization:</strong> confirm every required peripheral is initialized before use.</li><li><strong>Interrupts:</strong> confirm the right source is enabled, the flag is cleared, and the handler is short.</li><li><strong>Timing:</strong> confirm clock, period units, timer mode, and ownership.</li><li><strong>Logic:</strong> test empty, one-item, maximum, duplicate, and wraparound cases.</li><li><strong>Output:</strong> confirm scaling and the final LED, DAC, or memory destination.</li></ol>''',
    }
    return content[key]


def build_guides(peripheral_rows: list[dict[str, str]], items: list[dict[str, object]]) -> None:
    index = PORTAL / "guides" / "index.html"
    source_file = GUIDES / "PERIPHERALS_CANONICAL.md"
    peripheral_cards: list[str] = []
    for row in peripheral_rows:
        title = strip_internal(row.get("title", ""))
        destination = PORTAL / "guides" / f"peripheral-{slug(title)}.html"
        lesson_match = re.match(r"\s*(\d+)", title)
        lesson_number = int(lesson_match.group(1)) if lesson_match else None
        fragment = markdown_fragment(extract_markdown_section(source_file, title, lesson_number), source_file, destination)
        summary = strip_internal(row.get("summary", ""))
        if not fragment:
            raise SystemExit(f"Missing canonical peripheral lesson: {title}")
        body = f'''<section class="section-block"><div class="tag-list">{tags(split_tags(row.get('peripheral_tags',''), row.get('interrupt_tags',''), row.get('timing_tags','')))}</div>{fragment}<p>{href(source_file, destination, 'Read the complete peripheral guide')}</p></section><section class="section-block"><h2>Canonical contract</h2><p>{href(API_REFERENCE, destination, 'Read the Official Combined Exam API quick reference')} · {href(API_HEADER, destination, 'Read exam_api.h')}</p></section>'''
        write(destination, page(destination, title, summary, body, [("Home", HOME), ("Guides", index), (title, destination)], "Guides"))
        peripheral_cards.append(card(title, summary, destination, PORTAL / "guides" / "use-peripherals.html", "Read peripheral lesson", f'<div class="tag-list">{tags(split_tags(row.get("peripheral_tags", "")))}</div>'))
        items.append({"id": f"guide-peripheral-{slug(title)}", "kind": "Guides", "title": title, "summary": summary, "route": rel(destination, PORTAL / "search.html"), "examHistory": "Possible variation", "languages": ["C"], "components": split_tags(row.get("peripheral_tags", ""), row.get("interrupt_tags", ""), row.get("timing_tags", "")), "topics": ["Peripheral lesson", "Official Combined API"], "aliases": split_tags(row.get("usage_tags", "")), "relatedIds": []})
    joined_peripherals = "".join(peripheral_cards)
    goal_cards = []
    for key, title, summary in GUIDE_GOALS:
        destination = PORTAL / "guides" / f"{key}.html"
        body = f'<section class="section-block">{guide_body(key, joined_peripherals, destination)}</section>'
        if key == "start-a-working-project":
            body += f'<section class="section-block"><h2>Canonical template</h2><p>{href(STARTING_TEMPLATE / "sample.uvprojx", destination, "Use the Official Combined Exam API")} · {href(TEMPLATE_INTEGRATION, destination, "Read the solved-answer integration guide")}</p><p>Copy the complete maintained answer into <code>Source/sample.c</code> so its handlers, static state, and helpers stay together. Remove only conflicting handler definitions from the existing template IRQ sources, following the integration guide. The API contract is <code>Source/exam_api/exam_api.h</code>.</p></section>'
        write(destination, page(destination, title, summary, body, [("Home", HOME), ("Guides", index), (title, destination)], "Guides"))
        goal_cards.append(card(title, summary, destination, index, f"Read: {title}"))
        items.append({"id": f"guide-{key}", "kind": "Guides", "title": title, "summary": summary, "route": rel(destination, PORTAL / "search.html"), "examHistory": "Extra practice", "languages": ["Both"], "components": [], "topics": split_tags(title, summary), "aliases": [], "relatedIds": []})
    body = f'''<section><h2>Choose your goal</h2><div class="grid">{''.join(goal_cards)}</div></section><section class="section-block"><h2>Canonical sources</h2><p>Use the human-readable raw links on each exam and algorithm page. For hardware, rely only on {href(API_HEADER, index, 'the Official Combined exam_api.h header')} and {href(API_REFERENCE, index, 'its quick reference')}.</p></section>'''
    write(index, page(index, "Guides", SECTION_META["guides"][1], body, [("Home", HOME), ("Guides", index)], "Guides"))


def main() -> None:
    global PORTAL, ASSETS, GENERATED_SOURCES, ALGORITHM_INVENTORY_OUTPUT
    import sys
    source_assets = ASSETS
    output_options = [arg.split("=", 1)[1] for arg in sys.argv if arg.startswith("--output-root=")]
    if output_options:
        stage_root = Path(output_options[-1]).resolve()
        if stage_root != ROOT.resolve() and ROOT.resolve() not in stage_root.parents:
            raise SystemExit("--output-root must remain inside the package workspace")
        PORTAL = stage_root / "PORTAL"
        ASSETS = PORTAL / "assets"
        GENERATED_SOURCES = stage_root / "CANONICAL_WORKSTATION"
        ALGORITHM_INVENTORY_OUTPUT = stage_root / "ALGORITHM_INVENTORY.json"
    exams = read_csv(COURSE / "REVIEWED_EXAM_INDEX.csv")
    questions = read_csv(GUIDES / "QUESTION_INDEX.csv")
    patterns = read_csv(COURSE / "CANONICAL_PATTERN_INDEX.csv")
    solutions = read_csv(GUIDES / "CURRENT_TEMPLATE_SOLUTION_INDEX.csv")
    peripheral_rows = read_csv(MAINTENANCE / "PERIPHERAL_GUIDE_INDEX.csv")
    api = parse_api()
    counts = {"exams": len(exams), "questions": len(questions), "patterns": len(patterns), "api": len(api), "algorithms": 50 + len(ALGORITHM_VARIANTS) + len(EXTRA_ALGORITHMS) + len(NEW_ALGORITHMS), "peripheral lessons": len(peripheral_rows)}
    expected = {"exams": 23, "questions": 48, "patterns": 78, "peripheral lessons": 14}
    for key, value in expected.items():
        if counts[key] != value:
            raise SystemExit(f"Canonical {key} count changed: expected {value}, found {counts[key]}")
    if counts["algorithms"] < 100:
        raise SystemExit(f"Expected at least 100 algorithms, found {counts['algorithms']}")
    if "--algorithms-only" in sys.argv:
        data_text=(source_assets/"portal-data.js").read_text(encoding="utf-8")
        existing=json.loads(re.fullmatch(r"\s*window\.ARM_PORTAL_DATA=(.*);\s*",data_text,re.S).group(1))["items"]
        items=[item for item in existing if not item["id"].startswith(("algorithm-", "text-"))]
        build_algorithms(exams,items)
        connect_related(items, "Algorithms")
        from REFRESH_SEARCH import refresh
        refresh(globals(), items)
        print("Updated algorithms and search without replacing exam solutions or API pages")
        print(json.dumps(counts,indent=2))
        return
    if PORTAL.exists():
        shutil.rmtree(PORTAL)
    if GENERATED_SOURCES.exists() and "--reuse-pattern-projects" not in sys.argv:
        shutil.rmtree(GENERATED_SOURCES)
    globals()["reuse_pattern_projects"] = "--reuse-pattern-projects" in sys.argv
    build_assets()
    items: list[dict[str, object]] = []
    api_links = build_api(api, items)
    algorithm_links = build_algorithms(exams, items)
    pattern_links = build_patterns(patterns, exams, solutions, items)
    counts["patterns"] = len(pattern_links)
    build_exams(exams, questions, solutions, pattern_links, algorithm_links, {}, items)
    build_guides(peripheral_rows, items)
    connect_related(items)
    build_search(items)
    build_home()
    print("Built ARM Exam Workstation")
    print(json.dumps(counts, indent=2))
    print(f"Search items: {len(items)}")


if __name__ == "__main__":
    from portal_presentation import install
    install(globals())
    from workstation_extensions import install as install_extensions
    install_extensions(globals())
    from asm_reference import install as install_asm_reference
    install_asm_reference(globals())
    from pattern_runnable import install as install_runnable
    install_runnable(globals())
    from scenario_library import install as install_scenarios
    install_scenarios(globals())
    main()
