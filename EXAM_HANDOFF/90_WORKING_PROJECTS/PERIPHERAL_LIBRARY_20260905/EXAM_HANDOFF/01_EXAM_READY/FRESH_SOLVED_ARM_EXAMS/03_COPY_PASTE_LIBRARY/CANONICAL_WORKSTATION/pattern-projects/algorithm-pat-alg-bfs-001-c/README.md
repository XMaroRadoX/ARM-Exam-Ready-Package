# algorithm-pat-alg-bfs-001-c

pat-alg-bfs-001: complete c implementation and executable cases.

## Run and inspect

Run once: pattern_result=0 and LED mask0x01 means all included cases passed; otherwise pattern_result identifies the failed fixture line and LEDs show0xFF. Inspect test_main for exact inputs and results.

## Resource ownership

- No periodic interrupts; main calls test_main once
- Algorithm uses only the explicitly declared inputs and scratch storage

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
- Source/reference.c

Add Source/reference.c to the project target when adapting manually.
