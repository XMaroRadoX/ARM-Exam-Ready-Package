# dac-three-timer-notes

Three-timer note sequencing with exact paper thresholds.

## Run and inspect

Timer A skips its tick while B or C runs; B writes one DAC sample; C stops B. Source constants and argument order are retained.

## Resource ownership

- Timer0 A:50ms; TIMER0_IRQHandler starts a note only when B and C stopped
- Timer1 B:periodic waveform threshold from5351..1062; TIMER1_IRQHandler advances45-sample table
- Timer2 C:one-shot duration threshold from(40000000..625000)/5; TIMER2_IRQHandler stops B

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
