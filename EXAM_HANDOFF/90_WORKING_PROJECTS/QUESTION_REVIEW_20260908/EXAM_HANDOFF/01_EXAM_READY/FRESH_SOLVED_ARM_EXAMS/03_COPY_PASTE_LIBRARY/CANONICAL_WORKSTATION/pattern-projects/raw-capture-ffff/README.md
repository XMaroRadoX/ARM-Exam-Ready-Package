# raw-capture-ffff

Raw capture with the 16-bit match limit.

## Run and inspect

Timer1 resets at0xFFFF; INT0 captures TC immediately.

## Resource ownership

- Timer1:MR0=0xFFFF; EINT0 raw capture

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
