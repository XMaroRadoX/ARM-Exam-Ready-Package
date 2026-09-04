# E2023-05-17

- Date: `2023-05-17`
- Variant: `ARM`
- Source PDF: `Exams/22-23/20230517 arm.pdf`
- SHA-256: `94a30856a4f9a56bb908dbab2def2de9fee9973a4471ac5111399a992509bbab`
- Answer collection: `Study Material/03 - Solved Exams/2023-05-17_Signed_64_Division`
- Search tags: `abi:callee-saved-registers`, `abi:flags-return-contract`, `abi:two-register-wide-input`, `algorithm:condition-flag-result`, `algorithm:signed-restoring-division`, `data:apsr-flags`, `data:signed-32-bit`, `data:signed-64-bit`, `data:two-word-value`, `lang:assembly`, `risk:divide-by-zero`, `risk:nzcv-semantics`, `risk:overflow`, `risk:sign-normalization`, `risk:stack-balance`, `type:assembly-algorithm`, `type:assembly-flags`
- Patterns: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-WIDE-DIVISION-001`, `PAT-CPU-FLAGS-001`

## Questions

### Q1 - ASM

Divide a signed 64-bit dividend by a signed 32-bit divisor without MUL, using sign normalization, a 64-bit shift/subtract loop, and quotient-bit construction.

- Type: `assembly-algorithm`
- Algorithms: `signed-restoring-division`
- Peripherals/events/timing: `none`
- Data/ABI: `callee-saved-registers;signed-32-bit;signed-64-bit;two-register-wide-input;two-word-value`
- Risks: `divide-by-zero;sign-normalization;overflow;stack-balance`
- Search words: 64 by 32 signed division restoring shift subtract no MUL quotient remainder
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-ALG-WIDE-DIVISION-001`, `PAT-CPU-FLAGS-001`

### Q2 - ASM flags

Set or report the required N, Z, C and V status according to the division outcome using program-status-register operations.

- Type: `assembly-flags`
- Algorithms: `condition-flag-result`
- Peripherals/events/timing: `none`
- Data/ABI: `apsr-flags;flags-return-contract`
- Risks: `nzcv-semantics`
- Search words: APSR CPSR N Z C V flags overflow carry
- Pattern IDs: `PAT-AAPCS-STACK-SAFETY-001`, `PAT-CPU-FLAGS-001`

## Verification

- Assembly/simulator label: `COMPILE_ONLY`
- Hardware-build label: `COMPILE_ONLY`
- Physical board: `PHYSICAL_BOARD_NOT_TESTED`

## What usually changes

Sizes, constants, recurrence rules, timer periods, pins, state transitions and
result encoding. Start with the solved answer's `ADAPTATION_MAP.md` and keep
the question's exact width, signedness, ownership and AAPCS contract.
