# paper-e2025-07-01-a1

Run the Timer0/joystick rhythm interaction with explicit edge handling and LED feedback.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2025-07-01_ARM1-Q3: main; answer_joystick_sample; answer_timer0; RIT polls edges; Timer0 advances rounds; 3000 ms

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
