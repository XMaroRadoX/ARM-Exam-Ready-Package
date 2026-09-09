# task-audio-sequence-systick

Play 200 ms, silence 100 ms, then advance through three sample-divider settings.

## Run and inspect

At tick 20 output stops; at tick 30 next note starts; phase wraps after three notes.

## Resource ownership

- P2.0–P2.7: board labels LD11–LD4; byte display mask
- Timer0: 10 ms status/control; Timer1: 8 kHz DAC samples when DAC is selected; no capture pins
- 10 ms if primary clock; otherwise 100 ms supervisor counter; no peripheral acknowledgement
- P0.26 / AOUT speaker; 0–1023; timed waveform with Timer1, static voltage otherwise
- Foreground: sole controller state owner; bounded FIFO of 31 usable snapshots; loss counter on overflow

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
