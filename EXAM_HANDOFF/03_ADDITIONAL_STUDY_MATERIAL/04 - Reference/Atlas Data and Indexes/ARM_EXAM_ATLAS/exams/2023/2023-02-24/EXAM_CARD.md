# E2023-02-24

- Date: `2023-02-24`
- Variant: `ARM`
- Source PDF: `Exams/22-23/20230224 arm.pdf`
- SHA-256: `ebd2df9c75ec7e24bd6f76515a3b06cdfcec78b7e5aea7d33d977761fa0dc0a4`
- Answer collection: `Study Material/03 - Solved Exams/2023-02-24_Kaprekar_SVC`
- Search tags: `abi:callee-saved-registers`, `abi:exception-return`, `abi:non-leaf`, `algorithm:decimal-digits`, `algorithm:kaprekar`, `algorithm:kaprekar-iteration`, `algorithm:recurrence`, `algorithm:sorting`, `data:digit-array`, `data:exception-frame`, `data:scalar`, `event:svc-50`, `integration:c-calls-assembly`, `lang:assembly`, `lang:c`, `risk:msp-vs-psp`, `risk:signedness`, `risk:stack-balance`, `risk:svc-decode`, `risk:termination`, `type:assembly-algorithm`, `type:assembly-exception`
- Patterns: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-DECIMAL-DIGITS-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-SORTING-001`, `PAT-CPU-EXCEPTION-FRAME-001`, `PAT-CPU-SVC-001`, `PAT-FLOW-NESTED-LOOP-001`

## Questions

### Q1 - ASM

Implement the Kaprekar digit transformation, including digit extraction, reordering, subtraction and repeated convergence logic.

- Type: `assembly-algorithm`
- Algorithms: `kaprekar;decimal-digits;sorting;recurrence`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;digit-array;non-leaf;scalar`
- Risks: `signedness;termination;stack-balance`
- Search words: Kaprekar digits ascending descending subtraction convergence
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-DECIMAL-DIGITS-001`, `PAT-ALG-RECURRENCE-001`, `PAT-ALG-SORTING-001`, `PAT-FLOW-NESTED-LOOP-001`

### Q2 - ASM exception

Handle SVC #50, locate the correct exception stack frame, decode the SVC immediate from the instruction before stacked PC, repeatedly call the Kaprekar routine, and return the iteration count in R6.

- Type: `assembly-exception`
- Algorithms: `kaprekar-iteration`
- Peripherals/events/timing: `svc-50`
- Data/ABI: `callee-saved-registers;exception-frame;exception-return;non-leaf`
- Risks: `msp-vs-psp;svc-decode;stack-balance`
- Search words: SVC 50 supervisor immediate stacked PC MSP PSP R6
- Pattern IDs: `PAT-AAPCS-NONLEAF-001`, `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-RECURRENCE-001`, `PAT-CPU-EXCEPTION-FRAME-001`, `PAT-CPU-SVC-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.
