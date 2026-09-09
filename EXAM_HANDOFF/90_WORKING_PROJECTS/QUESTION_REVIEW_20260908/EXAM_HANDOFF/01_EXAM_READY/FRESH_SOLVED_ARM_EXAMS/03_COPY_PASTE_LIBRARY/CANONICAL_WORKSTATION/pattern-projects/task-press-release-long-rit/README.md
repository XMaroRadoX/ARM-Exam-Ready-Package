# task-press-release-long-rit

INT0 press toggles bit 0; release toggles bit 1; 1 second hold toggles bit 2 once.

## Run and inspect

Hold INT0 for 150 steps: value 5. Release: 7. No repeated long action.

## Resource ownership

- P2.0–P2.7: board labels LD11–LD4; byte display mask
- P2.10 INT0, P2.11 KEY1, P2.12 KEY2; active low
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
