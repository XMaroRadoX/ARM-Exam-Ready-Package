# paper-e2025-07-01-a2

Run the Timer1/joystick first-movement rhythm interaction without hidden background ownership.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2025-07-01_ARM2-Q3: main; answer_joystick_sample; answer_timer1; RIT detects first edge; Timer1 advances rounds; 2500 ms

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
