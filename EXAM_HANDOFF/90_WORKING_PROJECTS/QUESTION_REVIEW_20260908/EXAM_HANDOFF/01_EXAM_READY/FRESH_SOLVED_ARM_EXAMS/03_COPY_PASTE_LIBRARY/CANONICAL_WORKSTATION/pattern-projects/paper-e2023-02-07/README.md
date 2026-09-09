# paper-e2023-02-07

Capture characters with INT0 using Timer1 and alternate LEDs 6/7; KEY1 sorts and lights LED11.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2023-02-07-Q2: main; EINT0_IRQHandler; EINT1_IRQHandler; INT0 reads Timer1 TC immediately; KEY1 calls insertionSort inside EINT1_IRQHandler; Timer1 MR0=0xFF; reset without match IRQ
- Unused enabled button vectors: acknowledge only in Source/unused_buttons.c; preserve the paper answer files.

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
- Source/unused_buttons.c
