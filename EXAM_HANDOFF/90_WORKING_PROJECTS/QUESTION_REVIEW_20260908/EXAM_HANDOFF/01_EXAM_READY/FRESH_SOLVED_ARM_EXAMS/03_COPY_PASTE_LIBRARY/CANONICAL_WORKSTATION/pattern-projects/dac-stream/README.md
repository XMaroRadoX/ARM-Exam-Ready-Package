# dac-stream

Explicit table playback with eight samples per waveform cycle.

## Run and inspect

Each Timer0 match writes the next table value; after8 matches index wraps and completed=1. Sample frequency=PCLK/1263; waveform frequency=sample frequency/8.

## Resource ownership

- Timer0: exact1263 ticks; TIMER0_IRQHandler writes one sample

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
