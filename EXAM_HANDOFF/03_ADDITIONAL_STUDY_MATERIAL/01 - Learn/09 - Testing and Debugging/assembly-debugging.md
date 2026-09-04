# Assembly debugging

## Before running

- Confirm the exported symbol spelling and C prototype.
- Confirm Thumb mode and `PRESERVE8`.
- Mark each register as argument, base, length, index, accumulator, or temporary.
- Check each load/store width and scale.
- Pair the prologue and epilogue and calculate frame size.

## In Keil

1. Break at the assembly symbol.
2. Record SP and R4-R11.
3. Step through one iteration while watching pointers, indexes, flags, and memory.
4. Run to the return, then verify SP is identical and R4-R11 are preserved.
5. Inspect guard words around output arrays.
6. Repeat with zero/minimum size, maximum size, duplicates, and signed extremes.

## Symptom to likely cause

| Symptom | First check |
|---|---|
| loop never ends | wrong update register or signed/unsigned branch |
| first element works, later values fail | missing/incorrect index scale |
| caller crashes after return | LR or SP restoration |
| works until helper call | live value left in R0-R3/R12 |
| negatives look huge | `LDRB` used instead of `LDRSB` |
| matrix row is shifted | wrong stride or element size |

