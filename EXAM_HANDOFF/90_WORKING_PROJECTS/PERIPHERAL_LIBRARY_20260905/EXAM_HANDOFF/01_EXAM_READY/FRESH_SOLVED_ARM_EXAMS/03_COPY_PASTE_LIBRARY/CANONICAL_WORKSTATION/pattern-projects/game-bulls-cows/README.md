# game-bulls-cows

Bulls-and-Cows: DOWN, LEFT, RIGHT, UP edit digits0,1,2,3 respectively. SELECT submits, shows, and begins the next guess while retaining the secret; four correct digits finish the game.

## Run and inspect

First SELECT captures Timer1 seed; edit four digits; SELECT evaluates; next SELECT resets guess only. Follow display_guess and increment_digit for the exact mapping.

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
