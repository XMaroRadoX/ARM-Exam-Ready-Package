# paper-e2024-09-16

Two successive raw button interrupts select increment and offset, then call Kruskal immediately on the second choice.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2024-09-16-Q2: main; EINT1_IRQHandler; EINT2_IRQHandler; First raw IRQ selects increment; second selects offset and calls the algorithm; choices 2,3,4

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
