# Revision review — 2026-06-25_ARM1_BullsAndCows

- Source exam: `E2026-06-25-B1`
- Source SHA-256 expected: `a3f7eaca07f96a281382237948255abc1fadcfd2a3502d2e4d604921128fa2a8`
- Source SHA-256 actual: `a3f7eaca07f96a281382237948255abc1fadcfd2a3502d2e4d604921128fa2a8`
- Revision status: `REVISION_GATE_PASS`
- Template generation: `TWO_FILE_CALLBACK_V1`

## Requirement trace

- **Q1** — Compute bulls and cows using per-digit frequency arrays and pack the score. Contract: `BullsAndCows`; arguments: R0 guess, R1 secret, R2 guessFrequency, R3 secretFrequency; constants: (2*bulls-1)<<4 plus (2*cows-1). [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)
- **Q2** — Implement the full joystick Bulls-and-Cows game, preserving one timer-derived secret across guesses. Contract: `main; answer_joystick_sample`; arguments: Timer0 TC creates secret; RIT polls joystick edges; constants: four digits 0..3. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)

## Evidence

- source_paper_sha256: `PASS`
- question_trace: `PASS`
- main_c_present: `PASS`
- assembly_s_present: `PASS`
- mapping_present: `PASS`
- adaptation_present: `PASS`
- host_reference: `HOST_REFERENCE_PASS`
- peripheral_model: `SIMULATED_PERIPHERAL_MODEL_PASS`
- arm_compile_link: `ARM_COMPILE_LINK_PASS`
- arm_instruction_execution: `COMPILE_ONLY`
- physical_board: `PHYSICAL_BOARD_NOT_TESTED`

This review does not claim physical-board execution. A compile/link pass is not instruction-level execution.
