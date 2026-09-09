                PRESERVE8
                THUMB

                AREA    asm_functions, CODE, READONLY
                EXPORT  nextElementLCG

; Inputs: R0=previous, R1=a, R2=c, R3=n, [SP]=m.
; Output: R0=((a * previous + c) XOR n) mod m.
; Parameters in this paper are unsigned and m=255 is nonzero.
nextElementLCG  PROC
                ; Preserve the caller's R4 and the return address: 8 bytes.
                PUSH    {R4, LR}

                ; The fifth argument was at [SP] on entry.
                ; The push moved SP down 8 bytes, so now read [SP + 8].
                LDR     R4, [SP, #8]

                MUL     R0, R1, R0      ; a * previous
                ADD     R0, R0, R2      ; Add c
                EOR     R0, R0, R3      ; XOR with iteration n

                ; Modulo = value - (integer quotient * modulus).
                ; R1's original multiplier is no longer needed.
                UDIV    R1, R0, R4
                MUL     R1, R1, R4
                SUB     R0, R0, R1      ; Leave the remainder in R0

                ; Restore R4 and return by loading the saved LR into PC.
                ; Do not restore R0: that would overwrite our answer.
                POP     {R4, PC}
                ENDP
                END
