# paper-e2026-06-25-b1

Implement the full joystick Bulls-and-Cows game, preserving one timer-derived secret across guesses.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2026-06-25_ARM1-Q2: main; answer_joystick_sample; Timer0 TC creates secret; RIT polls joystick edges; four digits 0..3

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
