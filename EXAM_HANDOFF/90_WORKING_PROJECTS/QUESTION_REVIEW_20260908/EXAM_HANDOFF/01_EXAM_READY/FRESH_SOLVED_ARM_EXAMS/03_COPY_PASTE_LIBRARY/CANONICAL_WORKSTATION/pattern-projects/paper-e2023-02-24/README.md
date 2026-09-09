# paper-e2023-02-24

Handle SVC number 50, read the stacked argument, run Kaprekar, and return the count through the exception frame.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2023-02-24-Q2: SVC_Handler; stacked R0 input; stacked R0 output; SVC immediate 50; SVC #50

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
