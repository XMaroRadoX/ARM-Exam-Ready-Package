# task-adc-capture-rit

INT0 freezes the newest completed sample. Later pot changes update acquisition but not the captured result.

## Run and inspect

Sample 2048 then INT0 => result 2048; sample 4095 alone leaves result 2048.

## Resource ownership

- P2.0–P2.7: board labels LD11–LD4; byte display mask
- P2.10 INT0, P2.11 KEY1, P2.12 KEY2; active low
- 10 ms input sampling; RIT_IRQHandler acknowledges the interrupt
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
