# paper-e2024-02-28

Use Timer0 to display each path direction for 0.5 s followed by 0.5 s off.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2024-02-28-Q2: main; answer_timer0; Timer0 IRQ alternates direction and blank phases; 500 ms phases

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
