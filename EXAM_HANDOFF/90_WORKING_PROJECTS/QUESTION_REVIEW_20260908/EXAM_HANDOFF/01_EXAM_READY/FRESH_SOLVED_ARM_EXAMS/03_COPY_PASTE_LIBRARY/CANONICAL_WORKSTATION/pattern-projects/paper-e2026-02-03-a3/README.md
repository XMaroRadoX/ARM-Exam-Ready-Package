# paper-e2026-02-03-a3

Use ADC high eight bits as Recaman length on KEY2, then show elements every two seconds.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2026-02-03_ARM3-Q2: main; answer_timer0; ADC supplies length; KEY2 builds; Timer0 displays; 2000 ms; 255 words
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
