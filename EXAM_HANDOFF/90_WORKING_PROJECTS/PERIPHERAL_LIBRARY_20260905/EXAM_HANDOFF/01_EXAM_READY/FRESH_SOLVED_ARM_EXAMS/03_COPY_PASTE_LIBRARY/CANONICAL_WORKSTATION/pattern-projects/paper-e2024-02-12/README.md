# paper-e2024-02-12

Seed an LCG from Timer0, generate the maze on KEY2, then call the assembly solver.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2024-02-12-Q2: main; next_random; EINT2_IRQHandler; Timer0 TC seeds LCG; KEY2 event starts generation; modulus 101; threshold 18
- Unused enabled button vectors: acknowledge only in Source/unused_buttons.c; preserve the paper answer files.

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
- Source/unused_buttons.c
