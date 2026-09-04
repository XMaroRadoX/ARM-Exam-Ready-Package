# timer-exact-ticks

Preserve exact ticks rather than reinterpret them as milliseconds.

## Run and inspect

Each1263 peripheral-clock ticks increments count.

## Resource ownership

- Timer0:PR0,MR0=1263

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
