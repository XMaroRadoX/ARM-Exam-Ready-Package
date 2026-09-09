# joystick-release

Raw press, hold and release masks with periodic sampling.

## Run and inspect

Start with SELECT released; press lights LD11; hold leaves it on; release clears it. High bits never appear.

## Resource ownership

- RIT:10ms; RIT_IRQHandler owns joystick previous/current state

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
