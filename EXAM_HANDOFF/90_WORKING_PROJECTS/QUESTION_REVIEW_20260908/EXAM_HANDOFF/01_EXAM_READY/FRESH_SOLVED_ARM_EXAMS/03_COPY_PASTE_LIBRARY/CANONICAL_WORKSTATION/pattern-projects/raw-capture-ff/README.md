# raw-capture-ff

Capture the modulo counter immediately on a raw button IRQ.

## Run and inspect

Set Timer1 TC=37 in debugger; INT0 saves and displays37. Counter resets at0xFF. Bounce intentionally produces raw IRQs.

## Resource ownership

- Timer1: MR0=0xFF, reset without IRQ
- EINT0: capture before acknowledgement

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
