# E2025-07-01-A1

- Date: `2025-07-01`
- Variant: `ARM1`
- Source PDF: `Exams/24-25/2025_07_01/ARM1.pdf`
- SHA-256: `62e6a6f5101df35128b299c565c82f3338a8474dfb83b30e87efb2916a401843`
- Answer collection: `Study Material/Solved Exams/2025-07-01_ARM1_LCG_Rhythm`
- Tags: `abi:nonleaf`, `abi:stacked-args`, `alg:recurrence`, `board:gpio`, `board:joystick`, `board:timer`, `cpu:flags`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-AAPCS-STACKED-ARGS-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-GPIO-EVENT-001`, `PAT-GPIO-JOYSTICK-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2026-02-03-A3`, `E2025-07-01-A2`, `E2026-06-25-B2`, `E2026-06-25-B1`, `E2026-02-18-A2`

## Questions

### Q1 - ASM

Implement the requested linear congruential generator with five parameters and correct unsigned wraparound/modulo behavior.

**Traps:** Load argument 5 from the caller stack using the offset after any prologue; preserve R4-R11 and align SP.

### Q2 - ASM startup

Call the LCG repeatedly from Reset_Handler and maintain the required sequence/state without violating startup or call conventions.

**Traps:** Construct and clean the fifth stacked argument; keep stack eight-byte aligned at public call boundaries.

### Q3 - C

Use Timer0 for a three-second LED sequence and accept only the joystick's first movement for the rhythm-game state transition.

**Traps:** N/A

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.
