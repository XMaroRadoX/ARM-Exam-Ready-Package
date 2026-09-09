# paper-e2026-02-18-a1

Map Hofstadter Q values to note pitch and duration with three timers and stream SinTable to the DAC.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2026-02-18_ARM1-Q2: answer_timer0; answer_timer1; answer_timer2; Timer0=A 50ms, Timer1=B pitch, Timer2=C duration; Pmax/Pmin 5351/1062 and 40000000/625000; k 1/5

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
