# Arrays and loops

## Sum, count, minimum, and transform

All four use the same safe loop. Only the body and initialization change.

```asm
; R0=word array, R1=count
MOVS    R2, #0                  ; index
MOVS    R3, #0                  ; accumulator
scan_test
CMP     R2, R1
BHS     scan_done
LDR     R12, [R0, R2, LSL #2]
; BODY: add, compare, count, or transform R12
ADDS    R2, R2, #1
B       scan_test
scan_done
```

For a minimum, handle `n==0` according to the question, initialize the minimum from element zero, then start at index one. Do not initialize a signed minimum to zero unless zero is a valid mathematical sentinel.

## Copy with independent source and destination widths

```asm
; sign-extend int8 source into int32 destination
LDRSB   R3, [R0, R2]
STR     R3, [R1, R2, LSL #2]
```

Exam traps: testing after the body, wrong scale, signed load mismatch, and using a sentinel that may occur in the input.

