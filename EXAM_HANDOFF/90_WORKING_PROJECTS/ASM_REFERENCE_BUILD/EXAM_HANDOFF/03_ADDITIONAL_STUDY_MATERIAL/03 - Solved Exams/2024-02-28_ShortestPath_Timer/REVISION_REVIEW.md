# Revision review — 2024-02-28_ShortestPath_Timer

- Source exam: `E2024-02-28`
- Source SHA-256 expected: `772f6c10718ce63a360fd71027fbfce97bacac7b86829e48cf4bd3763d966783`
- Source SHA-256 actual: `772f6c10718ce63a360fd71027fbfce97bacac7b86829e48cf4bd3763d966783`
- Revision status: `REVISION_GATE_PASS`
- Template generation: `TWO_FILE_CALLBACK_V1`

## Requirement trace

- **Q1** — Compute shortest-path distances from the exit through an encoded maze. Contract: `shortestPath`; arguments: R0 rows, R1 columns, R2 maze address; R0 start distance; constants: 0 wall, 1 start, 2 exit. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)
- **Q2** — Use Timer0 to display each path direction for 0.5 s followed by 0.5 s off. Contract: `main; answer_timer0`; arguments: Timer0 IRQ alternates direction and blank phases; constants: 500 ms phases. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)

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
