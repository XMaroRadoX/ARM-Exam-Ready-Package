# July 1, 2025: seed-1 LCG paper

The attached [20250701.pdf](../../../02_ORIGINAL_MATERIALS/Exams/ARM%20questions/20250701.pdf) says A2. The library keeps its historical ID E2025-07-01-A1 because that entry matches the recurrence: seed 1, a=131, c=7, XOR iteration n, m=255. The separate seed-6/multiplier-157 variant is unchanged.

| Question | Actual requirement | Complete answer |
|---|---|---|
| Q1 | Implement nextElementLCG; fill a DIM-byte array from Reset_Handler. | [Q1 files and explanation](Answer%20Source/Q1/README.md) |
| Q2 | Timer0 every 3 seconds; only ten LCG calls; exactly one LED8-11 selected by modulo 4. | [Q2 files and explanation](Answer%20Source/Q2/README.md) |
| Q3 | First joystick movement only; correct/wrong score; full last response window; LED4 wins, LED5 loses. | [Q3 files and RIT explanation](Answer%20Source/Q3/README.md) |

The previous mapping incorrectly treated the reset-array test as Q2. It belongs to Q1. Q1's immediate test and Q2/Q3's timed application are separate complete builds.

