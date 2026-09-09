# paper-e2023-09-18

Raw button interrupts compose binary K; INT0 builds the series and checks the stated identity on LEDs4/5.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2023-09-18-Q2: main; EINT0_IRQHandler; EINT1_IRQHandler; EINT2_IRQHandler; EINT1 appends0; EINT2 appends1; EINT0 runs the computation; K up to 50

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
