# E2026-02-18-A1

- Date: `2026-02-18`
- Variant: `ARM1`
- Source PDF: `Material 2026\Exams\20260218_ARM_1.pdf`
- SHA-256: `0ef4f9295c4d1d486e29a037ebdd0f159208e131d2fa26ce3723b223b0887fa2`
- Project: `C:\Personal\College\CA 2026\CA\ARM_Exam_Ready_Package\deliverables\solved_exam_examples\2026-02-18_ARM1_Three_Timers`
- Tags: `abi:nonleaf`, `alg:frequency-count`, `alg:recurrence`, `board:adc`, `board:dac`, `board:gpio`, `board:timer`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `risk:vector-ownership`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-DAC-STREAM-001`, `PAT-GPIO-EVENT-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`, `PAT-TIMER-VECTOR-OWNERSHIP-001`
- Related exams: `E2026-02-18-A2`, `E2026-06-25-B1`, `E2026-02-03-A3`, `E2026-06-25-B2`, `E2025-02-12-A2`

## Questions

### Q1 - ASM

Generate the iterative Hofstadter Q sequence in a word array and return or track the required maximum while handling early indices safely.

**Traps:** Array pointer/length and max return value; validate recurrence-derived indexes before loads.

### Q2 - C + ASM call

Coordinate three timers for A/B/C states, stream SinTable[45] through the DAC, use a 50 ms scheduler tick, compute frequency/duration values, and track whether each timer is running.

**Traps:** Generated/control data must be stable before timers consume it; avoid conflicting ownership of timers and vectors.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.
