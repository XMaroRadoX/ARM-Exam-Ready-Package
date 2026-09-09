# mix-led-timer-rit-systick-adc-dac

Compose a board monitor using LED, Timer, RIT, SysTick, ADC, DAC. ADC sets the value and analog amplitude. LEDs show the low eight bits. Timer1 streams an eight-sample waveform at 8 kHz. Inspect app, output_ticks and supervisor_ticks in the debugger for components without a visible output.

## Run and inspect

Reset: running=1, value=0. For available inputs: INT0 pauses; KEY2 resets; RIGHT increments; ADC 4095 sets value=255 and amplitude=1023. Release inputs between commands.

## Resource ownership

- P2.0–P2.7: board labels LD11–LD4; byte display mask
- Timer0: 10 ms status/control; Timer1: 8 kHz DAC samples when DAC is selected; no capture pins
- 10 ms input sampling; RIT_IRQHandler acknowledges the interrupt
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
