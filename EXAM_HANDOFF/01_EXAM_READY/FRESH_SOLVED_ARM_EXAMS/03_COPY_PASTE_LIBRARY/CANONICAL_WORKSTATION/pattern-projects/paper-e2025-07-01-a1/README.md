# paper-e2025-07-01-a1

Generate one LCG value in each of the first ten Timer0 interrupts, every three seconds; use value modulo 4 to light exactly one LED8-11. Accept only the first joystick movement per three-second LED round; score ten rounds and show LED4 for victory or LED5 otherwise.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2025-07-01_ARM1-Q2: main; TIMER0_IRQHandler; nextElementLCG; R0 previous, R1 a, R2 c, R3 n; fifth argument m on stack; return R0; seed=1; a=131; c=7; n=0..9; m=255; 10 elements
- 2025-07-01_ARM1-Q3: main; TIMER0_IRQHandler; RIT_IRQHandler; game_next_round; game_poll_joystick; nextElementLCG; Timer0 opens rounds; RIT polls new direction edges; waiting_for_move accepts one response.; seed=1; a=131; c=7; n=0..9; m=255; 10 elements; Timer0=3000ms; RIT=10ms; final score at 33s

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
