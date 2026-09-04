# timer-pause-resume

Pause/resume differs from clearing and starting a fresh interval.

## Run and inspect

INT0 pauses current TC; KEY1 continues it; KEY2 clears TC/PC and starts a full500ms interval.

## Resource ownership

- Timer0:500ms; raw EINT0/1/2 controls

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
