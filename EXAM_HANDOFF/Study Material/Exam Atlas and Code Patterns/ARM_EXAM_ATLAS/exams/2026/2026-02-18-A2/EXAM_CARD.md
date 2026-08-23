# E2026-02-18-A2

- Date: `2026-02-18`
- Variant: `ARM2`
- Source PDF: `Exams/Exam 18.02.2026/20260218_ARM_2.pdf`
- SHA-256: `4dfecf2ee5556c9aa2b55184743e35fad063e50c0960233a80f5404312d458ea`
- Answer collection: `Study Material/Solved Exams/2026-02-18_ARM1_Three_Timers`
- Tags: `abi:nonleaf`, `alg:frequency-count`, `alg:recurrence`, `board:adc`, `board:dac`, `board:timer`, `cpu:flags`, `mem:matrix-row-major`, `mem:word-array`, `risk:irq-shared-state`, `risk:stack-alignment`, `state:event-loop`, `timing:free-running`, `timing:periodic`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ADC-SAMPLE-001`, `PAT-ALG-FREQUENCY-COUNT-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-FLAGS-001`, `PAT-DAC-STREAM-001`, `PAT-MEM-MATRIX-ROW-MAJOR-001`, `PAT-MEM-WORD-ARRAY-001`, `PAT-STATE-EVENT-LOOP-001`, `PAT-STATE-IRQ-HANDOFF-001`, `PAT-TIMER-FREE-RUNNING-001`, `PAT-TIMER-OWNERSHIP-001`, `PAT-TIMER-PERIODIC-001`
- Related exams: `E2026-02-18-A1`, `E2026-06-25-B1`, `E2026-02-03-A3`, `E2025-02-12-A1`, `E2026-06-25-B2`

## Questions

### Q1 - ASM

Generate the Hofstadter-Conway variant iteratively in a word array with correct seeds, recurrence-derived indexes and requested aggregate/result.

**Traps:** Define array/length/result and protect derived indexes from underflow/out-of-range access.

### Q2 - C + ASM call

Implement the three-timer, DAC and 50 ms scheduling variant, including frequency/duration calculations and explicit running/stopped states.

**Traps:** Separate ISR flags from main processing and keep every timer/vector owner unique.

## Verification

- Assembly: `COMPILE_ONLY`
- Peripheral model: `COMPILE_ONLY`
- Hardware build: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, and result encoding. Start with the project `ADAPTATION_MAP.md`.
