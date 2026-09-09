# ordered-parameters

Two raw commands choose increment and offset.

## Run and inspect

KEY1 then KEY2 selects increment3,offset2; teaching computation3*10+2 displays32. This is a parameter-flow demonstration, not the complete Kruskal paper.

## Resource ownership

- EINT0..2 equal priority; command updates one phase per IRQ

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
