# timer-multiple-matches

Configure four match notifications using explicit PCLK and PR.

## Run and inspect

At core100MHz,divider4,PR24, matches arrive at250us,500us,750us,1000us; MR0 resets the period.

## Resource ownership

- Timer0:four match channels; one handler tests a single snapshot

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
