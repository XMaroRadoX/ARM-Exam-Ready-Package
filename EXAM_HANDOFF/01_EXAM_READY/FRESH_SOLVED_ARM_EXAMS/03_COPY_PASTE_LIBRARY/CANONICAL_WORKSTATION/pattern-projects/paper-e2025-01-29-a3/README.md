# paper-e2025-01-29-a3

Capture A and B with Timer2 and verify transpose distributes over XOR.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2025-01-29_ARM3-Q2: main; events fill matrices then compare both sides of identity; (A xor B)^T

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
