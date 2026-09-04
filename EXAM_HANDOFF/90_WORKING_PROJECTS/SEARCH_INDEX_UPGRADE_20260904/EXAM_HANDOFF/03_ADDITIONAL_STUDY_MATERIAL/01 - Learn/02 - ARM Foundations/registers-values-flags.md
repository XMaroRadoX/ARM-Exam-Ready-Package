# Registers, values, and flags

## Registers you must know

| Register | Exam meaning |
|---|---|
| R0-R3 | first four arguments, scratch values, and return values; a called function may destroy them |
| R4-R11 | preserved registers; save and restore any that the function changes |
| R12 | scratch register; useful for temporary addresses or values |
| R13/SP | stack pointer; every subtraction must be undone exactly |
| R14/LR | return address; a nested `BL` overwrites it, so a non-leaf function must save it |
| R15/PC | current instruction address; exception frames save a return PC |

## Flags

`N` is the sign bit, `Z` says zero/equal, `C` is unsigned carry/no-borrow, and `V` is signed overflow. `CMP a,b` behaves like `a-b` without storing the result.

| Meaning | Branch |
|---|---|
| equal / not equal | `BEQ` / `BNE` |
| unsigned lower / higher-or-same | `BLO` / `BHS` |
| unsigned higher / lower-or-same | `BHI` / `BLS` |
| signed less / greater-or-equal | `BLT` / `BGE` |
| signed greater / less-or-equal | `BGT` / `BLE` |

Never select a branch by English appearance alone. Decide whether the compared values are signed.

## Common combinations

```asm
; if (x == 0)
CMP     R0, #0
BEQ     zero_case

; unsigned: if (i >= n) stop
CMP     R2, R1
BHS     done

; signed: if (value < 0)
CMP     R0, #0
BLT     negative

; uint64 result = a + b, pairs are low/high
ADDS    R0, R0, R2
ADC     R1, R1, R3

; absolute value, except INT_MIN cannot be represented as positive int32
CMP     R0, #0
IT      LT
RSBLT   R0, R0, #0
```

