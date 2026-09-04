# buttons-systick-timer

Confirmed inputs and display timer with separate owners.

## Run and inspect

INT0 increases count once after 5 sampled lows; KEY1 pauses display; KEY2 resets and starts its interval. Release then press for another action.

## Resource ownership

- SysTick:10ms; starts during config
- Timer0:500ms; EINT0..2 begin debounce

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
