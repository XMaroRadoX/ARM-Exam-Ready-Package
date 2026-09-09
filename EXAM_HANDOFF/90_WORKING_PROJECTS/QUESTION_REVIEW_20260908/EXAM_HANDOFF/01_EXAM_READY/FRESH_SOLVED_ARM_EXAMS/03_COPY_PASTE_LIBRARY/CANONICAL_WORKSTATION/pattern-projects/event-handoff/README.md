# event-handoff

A pending-work bit consumed in foreground.

## Run and inspect

One or more IRQs before take produce one request. Three delayed identical events are not a count of3. Use direct command handling when every identity matters.

## Resource ownership

- Timer0:500ms producer
- main: atomic take and foreground display

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
