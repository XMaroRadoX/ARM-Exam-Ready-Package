# Revision review — 2024-02-12_Maze_LCG_Timer

- Source exam: `E2024-02-12`
- Source SHA-256 expected: `857211aa08989b7cd8e4630443c80fe33a4ad8e94d34a17636626deac8230ede`
- Source SHA-256 actual: `857211aa08989b7cd8e4630443c80fe33a4ad8e94d34a17636626deac8230ede`
- Revision status: `REVISION_GATE_PASS`
- Template generation: `TWO_FILE_CALLBACK_V1`

## Requirement trace

- **Q1** — Propagate maze direction letters from the exit until no additional cells can be labelled. Contract: `mazeSolver`; arguments: R0 rows, R1 columns, R2 flat maze address; constants: walls # and exit E. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)
- **Q2** — Seed an LCG from Timer0, generate the maze on KEY2, then call the assembly solver. Contract: `main; next_random; EINT2_IRQHandler`; arguments: Timer0 TC seeds LCG; KEY2 event starts generation; constants: modulus 101; threshold 18. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)

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
