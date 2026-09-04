# task-adjustable-waveform-systick

Potentiometer controls amplitude; INT0 pauses; KEY1/SELECT changes waveform; joystick LEFT/RIGHT adjusts display.

## Run and inspect

ADC 0 silences amplitude; 4095 reaches 1023; pause writes zero; reset clears application state.

## Resource ownership

- P2.0–P2.7: board labels LD11–LD4; byte display mask
- P2.10 INT0, P2.11 KEY1, P2.12 KEY2; active low
- P1.25 SELECT, P1.26 DOWN, P1.27 LEFT, P1.28 RIGHT, P1.29 UP; active low
- Timer0: 10 ms status/control; Timer1: 8 kHz DAC samples when DAC is selected; no capture pins
- 10 ms if primary clock; otherwise 100 ms supervisor counter; no peripheral acknowledgement
- P1.31 / AD0.5 potentiometer; 0–4095; one conversion at a time
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
