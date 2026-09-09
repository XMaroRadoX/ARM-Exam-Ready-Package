# adc-button-sequence

Preview ADC, capture the latest completed sample on a raw press, show four paced values.

## Run and inspect

ADC4095 previews255; INT0 captures4095, displays255,0,1,2 at500ms steps, then stops. Pot changes do not change the captured sequence.

## Resource ownership

- ADC: one conversion at a time; ADC_IRQHandler consumes then starts next
- EINT0: capture and start sequence
- Timer0: 500 ms; same priority as ADC and EINT0

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
