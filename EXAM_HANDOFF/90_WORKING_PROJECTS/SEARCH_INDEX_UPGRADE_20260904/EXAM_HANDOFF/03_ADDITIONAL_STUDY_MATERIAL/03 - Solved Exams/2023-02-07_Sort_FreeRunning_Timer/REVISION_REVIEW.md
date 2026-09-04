# Revision review — 2023-02-07_Sort_FreeRunning_Timer

- Source exam: `E2023-02-07`
- Source SHA-256 expected: `77929b413afda671274838630078b32bbebe1e643e1102a00412a7209879ce26`
- Source SHA-256 actual: `77929b413afda671274838630078b32bbebe1e643e1102a00412a7209879ce26`
- Revision status: `REVISION_GATE_PASS`
- Template generation: `TWO_FILE_CALLBACK_V1`

## Requirement trace

- **Q1** — Copy signed bytes into word storage, then sort ascending with insertion sort. Contract: `copyData; insertionSort`; arguments: R0 source, R1 destination, R2 length; then R0 array, R1 length; constants: signed byte to signed word. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)
- **Q2** — Capture characters with INT0 using Timer1 and alternate LEDs 6/7; KEY1 sorts and lights LED11. Contract: `main; EINT0_IRQHandler; EINT1_IRQHandler`; arguments: Timer1 TC supplies captured value; event bits transfer debounced presses; constants: Timer1 modulo 0x100. [Current C solution](Answer%20Source/main.c) · [Current ASM solution](Answer%20Source/assembly.s)

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
