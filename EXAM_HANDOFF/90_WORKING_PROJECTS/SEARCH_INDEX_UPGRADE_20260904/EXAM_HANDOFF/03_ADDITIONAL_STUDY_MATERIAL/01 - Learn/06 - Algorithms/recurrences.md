# Recurrences

A recurrence answer has four parts: seeds, current state, next-term formula, and stopping rule.

```asm
; R0=output words, R1=count; example Fibonacci-like sequence
CMP     R1, #0
BEQ     rec_done
MOVS    R2, #0
STR     R2, [R0]
CMP     R1, #1
BEQ     rec_done
MOVS    R3, #1
STR     R3, [R0, #4]
MOVS    R4, #2
rec_loop
CMP     R4, R1
BHS     rec_done
ADD     R12, R2, R3
STR     R12, [R0, R4, LSL #2]
MOV     R2, R3
MOV     R3, R12
ADDS    R4, R4, #1
B       rec_loop
rec_done
BX      LR
```

Adapt seeds and the next-term policy, not the loop structure. Historical variants include affine/LCG sequences, Look-and-Say, run-length generation, Recamán, digit recurrences, and sociable-number iteration.

