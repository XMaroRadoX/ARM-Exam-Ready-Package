# paper-e2025-02-12-a1

Generate a 45-sample sine waveform through the DAC at the required Timer0 threshold.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2025-02-12_ARM1-Q2: main; answer_timer0; Timer0 IRQ writes one DAC sample and wraps index; 45 samples; k=1263
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
