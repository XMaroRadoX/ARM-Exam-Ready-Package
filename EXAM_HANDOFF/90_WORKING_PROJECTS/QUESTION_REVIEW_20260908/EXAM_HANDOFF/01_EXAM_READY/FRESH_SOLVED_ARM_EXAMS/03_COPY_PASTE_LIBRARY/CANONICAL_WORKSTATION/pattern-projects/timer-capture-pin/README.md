# timer-capture-pin

Configure a real CAP0.0 input and interpret its saved flag.

## Run and inspect

Provide rising edges at P1.26; each saves TC in CR0 and updates last_capture. This owns P1.26, so do not initialize joystick in this project.

## Resource ownership

- P1.26: CAP0.0, CCR rising edge+interrupt
- Timer0: PR0; no match actions; TIMER0_IRQHandler reads CR0

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
