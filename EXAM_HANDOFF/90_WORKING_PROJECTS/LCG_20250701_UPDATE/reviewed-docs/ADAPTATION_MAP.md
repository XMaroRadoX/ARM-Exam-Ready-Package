# Complete answer file placement

Use a working copy of Official Combined Exam API; preserve the original template.

| Answer file | Destination |
|---|---|
| main.c (Q2 or Q3) | Source/sample.c |
| assembly.s | Source/ASM_funct.s |
| IRQ_timer.c (Q2 or Q3) | Source/timer/IRQ_timer.c |
| IRQ_RIT.c (Q3) | Source/RIT/IRQ_RIT.c |

Q1 has a complete standalone assembly answer: its strong Reset_Handler generates the byte array and stops. Keep the original startup file for the vector table and stack.

Q2/Q3 have callable-only assembly and use normal startup to enter C main. Their complete main.c includes the used IRQ handlers. The supplied IRQ replacements prevent duplicates and preserve unused Timer1-3 handlers.

[Q1 guide](Answer%20Source/Q1/README.md) | [Q2 guide](Answer%20Source/Q2/README.md) | [Q3 guide and RIT explanation](Answer%20Source/Q3/README.md)

Replace complete files; do not append a second main or IRQ handler.
