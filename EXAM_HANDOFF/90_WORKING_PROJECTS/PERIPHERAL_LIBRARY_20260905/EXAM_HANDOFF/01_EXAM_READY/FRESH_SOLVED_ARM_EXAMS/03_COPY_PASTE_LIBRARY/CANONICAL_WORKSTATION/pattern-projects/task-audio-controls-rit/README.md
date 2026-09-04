# task-audio-controls-rit

INT0 pauses/resumes; RIGHT cycles sine, square, ramp; KEY2 resets application state.

## Run and inspect

RIGHT advances shape once; held RIGHT does not repeat. Paused output is zero.

## Resource ownership

- P2.10 INT0, P2.11 KEY1, P2.12 KEY2; active low
- P1.25 SELECT, P1.26 DOWN, P1.27 LEFT, P1.28 RIGHT, P1.29 UP; active low
- Timer0: 10 ms status/control; Timer1: 8 kHz DAC samples when DAC is selected; no capture pins
- 10 ms input sampling; RIT_IRQHandler acknowledges the interrupt
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
