# Revision review — 2023-05-17_Signed_64_Division

- Source exam: `E2023-05-17`
- Source SHA-256 expected: `94a30856a4f9a56bb908dbab2def2de9fee9973a4471ac5111399a992509bbab`
- Source SHA-256 actual: `94a30856a4f9a56bb908dbab2def2de9fee9973a4471ac5111399a992509bbab`
- Revision status: `REVISION_GATE_PASS`
- Template generation: `TWO_FILE_CALLBACK_V1`

## Requirement trace

- **Q1** — Divide a signed 64-bit dividend by a signed 32-bit divisor without MUL and return a signed 32-bit quotient. Contract: `SDIV64`; arguments: R0 upper dividend, R1 lower dividend, R2 divisor; R0 quotient; constants: 32 quotient iterations. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)
- **Q2** — Extend signed 64/32 division with the requested N, Z, C and V result flags. Contract: `SDIV64S`; arguments: same arguments as SDIV64; R0 quotient and APSR flags; constants: NZCV. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)

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
