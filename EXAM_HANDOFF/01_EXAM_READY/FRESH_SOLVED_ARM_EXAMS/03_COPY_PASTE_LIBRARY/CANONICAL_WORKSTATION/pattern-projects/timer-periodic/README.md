# timer-periodic

Count and display every half-second match.

## Run and inspect

After reset count=0; after two matches count=2 and display=0x02.

## Resource ownership

- Timer0: 500 ms; TIMER0_IRQHandler updates count; foreground idle

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
