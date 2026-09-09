# game-mastermind

Mastermind mapping and persistent game state.

## Run and inspect

UP, RIGHT, DOWN, LEFT edit digits0,1,2,3 respectively. First SELECT captures the secret; later SELECT submits. After a losing result, SELECT clears the guess while retaining the secret.

## Resource ownership

- Timer1:MR0=UINT32_MAX,PR0,no match IRQ; seed on first SELECT
- RIT:10ms input sampling; RIT_IRQHandler publishes edges; main owns rounds

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
