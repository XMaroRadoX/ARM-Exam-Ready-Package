# task-code-entry-rit

RIGHT, LEFT, RIGHT, LEFT encodes 0x66; SELECT checks and clears the input.

## Run and inspect

Correct four-command sequence then SELECT: 255; short or wrong sequence: 0.

## Resource ownership

- P2.0–P2.7: board labels LD11–LD4; byte display mask
- P1.25 SELECT, P1.26 DOWN, P1.27 LEFT, P1.28 RIGHT, P1.29 UP; active low
- 10 ms input sampling; RIT_IRQHandler acknowledges the interrupt
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
