# paper-e2024-07-09

Choose a valid neighbor, including a SysTick-based randomized selection helper. Run randomized depth-first maze traversal with stack backtracking and a strong Reset_Handler that starts SysTick.

## Run and inspect

Follow the exact input sequence and expected result in the linked original question and reviewed mapping.

## Resource ownership

- 2024-07-09-Q1: chooseNeighbor; chooseRandomNeighbor; R0-R3 neighbor states; R0 direction 0..4; directions 1..4
- 2024-07-09-Q2: depthFirstSearch; Reset_Handler; R0 maze, R1 rows, R2 columns, R3 start; SysTick LOAD 0xFFFFFF
- SysTick counter-only use: Source/idle_systick.c owns a returning handler.

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
- Source/idle_systick.c
