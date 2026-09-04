# rhythm-first-movement

First movement per interval; later movements deliberately ignored.

## Run and inspect

Keep the source timer threshold and IRQ algorithm call. The first movement consumes the active interval; do not replay ignored movements.

## Resource ownership

- Timer0:3000ms; TIMER0_IRQHandler calls nextElementLCG and opens one movement window
- RIT:10ms; RIT_IRQHandler handles first movement immediately

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
