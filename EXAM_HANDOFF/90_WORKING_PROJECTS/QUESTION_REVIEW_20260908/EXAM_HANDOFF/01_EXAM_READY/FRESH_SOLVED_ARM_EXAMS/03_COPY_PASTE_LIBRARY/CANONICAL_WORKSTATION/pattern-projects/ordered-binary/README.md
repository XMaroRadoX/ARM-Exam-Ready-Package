# ordered-binary

Process raw button commands without losing identity to merged bits.

## Run and inspect

KEY2,KEY1,KEY1,KEY2,KEY2,KEY1 then INT0 produces binary100110=38. At32 bits further digit commands are ignored.

## Resource ownership

- EINT1=append0; EINT2=append1; EINT0=submit
- Equal NVIC priority; foreground idle

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
