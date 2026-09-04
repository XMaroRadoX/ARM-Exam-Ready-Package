# Fixed-point and wide arithmetic

Fixed-point stores a real value as an integer with an implied scale. For Qm.n, one represents `1 << n`.

```asm
; Q16.16 multiply: ((int64)a*b) >> 16
SMULL   R2, R3, R0, R1         ; signed 64-bit product R3:R2
LSRS    R2, R2, #16
ORR     R0, R2, R3, LSL #16
BX      LR
```

Use `UMULL` for unsigned values and `SMULL` for signed values. Rounding, saturation, and overflow behavior must follow the question; they are not interchangeable defaults.

For 64-bit addition use `ADDS` on low words and `ADC` on high words. For subtraction use `SUBS` and `SBC`.

