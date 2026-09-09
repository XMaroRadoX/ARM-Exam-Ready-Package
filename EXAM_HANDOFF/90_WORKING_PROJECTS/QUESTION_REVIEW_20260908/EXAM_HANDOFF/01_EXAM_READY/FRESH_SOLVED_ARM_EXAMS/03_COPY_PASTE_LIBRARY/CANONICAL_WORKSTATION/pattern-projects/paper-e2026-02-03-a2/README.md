# paper-e2026-02-03-a2

Continuously display ADC high eight bits; KEY1 runs RLE and displays the low result byte.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2026-02-03_ARM2-Q2: main; ADC_IRQHandler; EINT1_IRQHandler; ADC fresh flag feeds main; debounced KEY1 triggers assembly; 12-bit ADC; high8/low8
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
