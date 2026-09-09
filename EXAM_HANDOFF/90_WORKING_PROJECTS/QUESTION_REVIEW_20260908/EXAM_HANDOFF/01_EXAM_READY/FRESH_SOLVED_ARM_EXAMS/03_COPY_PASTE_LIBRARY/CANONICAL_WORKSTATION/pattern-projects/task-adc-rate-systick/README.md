# task-adc-rate-systick

Map ADC to a bounded 50–1000 ms interval; retain elapsed progress when the setting changes.

## Run and inspect

ADC 0 selects five ticks; fifth tick toggles. ADC 4095 selects 100 ticks.

## Resource ownership

- P2.0–P2.7: board labels LD11–LD4; byte display mask
- 10 ms if primary clock; otherwise 100 ms supervisor counter; no peripheral acknowledgement
- P1.31 / AD0.5 potentiometer; 0–4095; one conversion at a time
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
