# Revision review — 2024-09-16_Kruskal_Buttons

- Source exam: `E2024-09-16`
- Source SHA-256 expected: `bbadd5254928052d8fdf6f824af902ed80a57c58adbb8028e7ec666d2935e3c1`
- Source SHA-256 actual: `bbadd5254928052d8fdf6f824af902ed80a57c58adbb8028e7ec666d2935e3c1`
- Revision status: `REVISION_GATE_PASS`
- Template generation: `TWO_FILE_CALLBACK_V1`

## Requirement trace

- **Q1** — Apply Kruskal-style wall removal using seven ABI arguments and merge component labels. Contract: `kruskal`; arguments: R0-R3 first four args; remaining three on caller stack; constants: horizontal/vertical wall arrays. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)
- **Q2** — Use two debounced button choices to select increment and offset values 2, 3 or 4 before calling Kruskal. Contract: `main; EINT1_IRQHandler; EINT2_IRQHandler`; arguments: first two events select parameters; later event runs algorithm; constants: choices 2,3,4. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)

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
