# svc-frame

SVC #7 with MSP/PSP frame selection and a C dispatcher.

## Run and inspect

Debugger: svc_result=7 and returned=8. Assembly owns SVC_Handler; EXAM_ENABLE_SVC_HANDLER stays0.

## Resource ownership

- SVC_Handler selects stacked MSP/PSP frame and tail-calls API decoder

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
