# Search, sort, and frequency tables

## Frequency table

Use this only when values have a small known range. Clear the table, then increment `frequency[value]`.

```asm
; R0=byte input, R1=count, R2=word frequency table
MOVS    R3, #0
freq_test
CMP     R3, R1
BHS     freq_done
LDRB    R12, [R0, R3]
LDR     R4, [R2, R12, LSL #2]
ADDS    R4, R4, #1
STR     R4, [R2, R12, LSL #2]
ADDS    R3, R3, #1
B       freq_test
freq_done
```

Validate or prove the value range before using it as an index. Bulls-and-Cows uses two frequency tables and counts exact matches separately so duplicate symbols are not over-counted.

## Selection-style sort

For each position `i`, scan `j=i+1..n-1` for the best candidate, then swap once. This is usually easier to verify in assembly than clever sorting code.

## Early search exit

Keep a “found” result or return immediately only when the ABI and cleanup allow it. A function with a stack frame must branch to a shared epilogue, not bypass the POP.

