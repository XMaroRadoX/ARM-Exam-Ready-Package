# dac-button-once

A raw press starts one complete table traversal; busy presses are ignored.

## Run and inspect

INT0 then8 sample matches gives completed=1 and stopped Timer0. A later INT0 restarts at index0.

## Resource ownership

- EINT0: trigger
- Timer0:1263 ticks/sample, stops after8 samples

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
