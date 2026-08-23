# Markdown library map

This is the directory of directories for all private documentation. It is
organized by the question being answered, not by filename alone.

## Documents to open first

1. [Ultimate exam navigator](exam-navigator.md) — the tutor-style route
   from receiving the paper to submitting the final Keil project.
2. [Live exam companion](live-exam-guide.md) — checkpoint-by-checkpoint
   directions to follow after the paper is placed in front of you.
3. [USB package instructions](usb-package-guide.md) — what to copy, edit and submit.
4. [Code-template index](../Exam%20Atlas%20and%20Code%20Patterns/CODE_TEMPLATES/00_TEMPLATE_INDEX.md)
   — direct access to reusable C and assembly source patterns.
5. [API and assembly coverage](api-and-pattern-coverage.md) — all 28
   recurring tags mapped to APIs, source templates, indexed questions and gaps.
6. [Template cleanup and improvements](template-cleanup-and-improvements.md) —
   the clean submission layout, completed cleanup and remaining verification work.

## “I need to recognize this question”

- [Quick pattern lookup](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/QUICK_PATTERN_LOOKUP.md)
  maps common exam wording to pattern families.
- [Code-first pattern index](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/CODE_PATTERN_INDEX.md)
  maps a required operation to actual source code.
- [Tag dictionary](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/TAG_DICTIONARY.md)
  explains the normalized `alg:`, `mem:`, `board:`, `abi:` and `risk:` tags.
- [Pattern library index](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/INDEX.md)
  lists every canonical technique.

## “I remember a previous exam”

- [Full exam chronology](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/exams/INDEX.md)
  links all 23 indexed papers.
- [Atlas home](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/INDEX.md)
  explains exam IDs, question IDs, patterns and verification labels.
- Year indexes:
  [2023](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/exams/2023/INDEX.md),
  [2024](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/exams/2024/INDEX.md),
  [2025](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/exams/2025/INDEX.md),
  [2026](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/exams/2026/INDEX.md).

Each exam directory follows the same four-file structure:

| File | Purpose |
|---|---|
| `CODE_START_HERE.md` | Fastest code-oriented entry point |
| `EXAM_CARD.md` | Requirements, source, tags, risks and related exams |
| `Q1_ASSEMBLY.md` | Assembly interpretation and linked solution |
| `Q2_BOARD.md` | C/peripheral interpretation and linked solution |

The corresponding answer projects are under
[`Solved Exams`](../Solved%20Exams). Use the audit before trusting an older
answer: [solution-completeness audit](../Tests%20and%20Reports/FINAL_PROJECT_TEMPLATE_AND_EXAM_AUDIT.md).

## “I need an assembly pattern”

- ABI and stack:
  [four arguments](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-FOUR-ARGS-001.md),
  [non-leaf calls](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-NONLEAF-001.md),
  [stack safety](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-STACK-SAFETY-001.md),
  [stacked arguments](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-STACKED-ARGS-001.md).
- Memory:
  [byte arrays](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-BYTE-ARRAY-001.md),
  [word arrays](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-WORD-ARRAY-001.md),
  [row-major matrices](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-MATRIX-ROW-MAJOR-001.md).
- Algorithms:
  [sorting](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-SORTING-001.md),
  [recurrence](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-RECURRENCE-001.md),
  [graph search](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-GRAPH-SEARCH-001.md),
  [frequency counting](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-FREQUENCY-COUNT-001.md),
  [fixed point](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-FIXED-POINT-001.md).
- CPU behavior:
  [flags](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/exceptions/PAT-CPU-FLAGS-001.md),
  [SVC](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/exceptions/PAT-CPU-SVC-001.md),
  [exception frame](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/exceptions/PAT-CPU-EXCEPTION-FRAME-001.md).

## “I need C or a peripheral”

- [GPIO event pattern](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/gpio-input/PAT-GPIO-EVENT-001.md)
- [Joystick pattern](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/gpio-input/PAT-GPIO-JOYSTICK-001.md)
- [Debounce](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/state-machines/PAT-STATE-DEBOUNCE-001.md)
- [Interrupt-to-foreground handoff](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/state-machines/PAT-STATE-IRQ-HANDOFF-001.md)
- [Event loop](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/state-machines/PAT-STATE-EVENT-LOOP-001.md)
- [Periodic timer](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/timers/PAT-TIMER-PERIODIC-001.md)
- [Free-running timer](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/timers/PAT-TIMER-FREE-RUNNING-001.md)
- [Timer ownership](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/timers/PAT-TIMER-OWNERSHIP-001.md)
- [Vector ownership](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/timers/PAT-TIMER-VECTOR-OWNERSHIP-001.md)
- [ADC sampling](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/adc-dac/PAT-ADC-SAMPLE-001.md)
- [DAC streaming](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/adc-dac/PAT-DAC-STREAM-001.md)

## “I want to practise and debug”

- [Learning-project index](../Practice%20Projects/README.md)
- [Bulls and Cows debug lab](../Practice%20Projects/BULLS_AND_COWS_DEBUG_LAB/DEBUG_AND_LEARN.md)
- [Bulls and Cows solution notes](../Practice%20Projects/BULLS_AND_COWS_DEBUG_LAB/SOLUTION_NOTES.md)
- [Five-minute checklist](../Practice%20Projects/BULLS_AND_COWS_DEBUG_LAB/Documentation/FIVE_MINUTE_CHECKLIST.md)
- [Peripheral recipes](../Practice%20Projects/BULLS_AND_COWS_DEBUG_LAB/Documentation/PERIPHERAL_RECIPES.md)
- [Complete API/function guide](../Practice%20Projects/BULLS_AND_COWS_DEBUG_LAB/Documentation/COMPLETE_FUNCTION_GUIDE.md)

## Evidence and reports

All build logs, coverage matrices and validation results belong in
[`Tests and Reports`](../Tests%20and%20Reports). These files are evidence,
not exam instructions. The most important current report is the
[final project and solution audit](../Tests%20and%20Reports/FINAL_PROJECT_TEMPLATE_AND_EXAM_AUDIT.md).

Local documentation links are checked by
`Tools/test-markdown-links.ps1`. Its latest machine-readable
result is [MARKDOWN_LINK_TEST.csv](../Tests%20and%20Reports/MARKDOWN_LINK_TEST.csv).
The current package-wide result is **597 local links checked, 0 failures**.

## Original and legacy material

The professor templates, original v1/v2 kits, previous deliverables, previous
atlas and previous tool environment are preserved as verified ZIP archives.
See the [original and legacy archive index](../Original%20and%20Legacy%20Archives/README.md).

## Deliberately excluded topics

The 23-exam history contains no CAN, MIDI/music, LCD/GLCD, touch-panel or PCON
question. Those professor samples are not part of the lean submission project.
