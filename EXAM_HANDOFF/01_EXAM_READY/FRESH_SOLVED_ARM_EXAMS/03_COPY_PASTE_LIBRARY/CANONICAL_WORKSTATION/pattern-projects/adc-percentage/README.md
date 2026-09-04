# adc-percentage

Scale a captured ADC sample to rounded percent.

## Run and inspect

ADC0=>0%,2048=>50%,4095=>100%; high8 preview remains unchanged.

## Resource ownership

- Same ownership as adc-button-sequence

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
