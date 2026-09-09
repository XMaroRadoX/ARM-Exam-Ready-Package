# Reviewed update: July 1 seed-1 LCG solutions

The previous Q2 mapping incorrectly described the Q1 reset-array test. The question mapping and complete commented answers now follow the attached 20250701.pdf.

- Q1: actual Reset_Handler executed as Thumb code; expected ten bytes, restored stack, and no array overrun confirmed.
- Q2: complete C and assembly compiled/linked for Cortex-M3 with LLVM; six fixture assertions verify ten calls, LED order, and timer stop.
- Q3: complete C and assembly compiled/linked for Cortex-M3 with LLVM; 21 fixture assertions cover first responses, held directions, wrong answers, centre/select, simultaneous directions, missed rounds, final-round response, ties, wins, and stable result LEDs.
- Execution checks validate callee-saved registers, restored SP, and 8-byte public-call alignment.
- LLVM translates ARMASM directives. Native Keil ARMASM compilation has not been performed.
- Peripheral checks use mocks. Physical-board execution and mechanical input debounce are not claimed.

Rerun 01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/VERIFY_20250701.py.

[Machine-readable evidence](../../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/LCG_20250701_VALIDATION.json)

The input PDF says A2; the collection's stable ID E2025-07-01-A1 is retained because its seed-1, multiplier-131 formula is the match.
