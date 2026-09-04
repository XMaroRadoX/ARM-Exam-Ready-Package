# dac-duration

Waveform timer plus independent duration timer.

## Run and inspect

Timer0 streams; after100ms Timer1 stops Timer0 and writes midpoint512. No queued playback resumes afterward.

## Resource ownership

- Timer0:1263 ticks/sample
- Timer1:100ms one-shot stops Timer0

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
