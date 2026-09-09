                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  LCGsequence

; uint32_t LCGsequence(previous, a, c, shift, modulus)
LCGsequence     PROC
                LDR     R12, [SP]       ; Fifth argument: modulus.
                LSR     R3, R0, R3      ; previous >> shift.
                MUL     R0, R0, R1
                ADDS    R0, R0, R2
                EORS    R0, R0, R3
                UDIV    R1, R0, R12
                MLS     R0, R1, R12, R0
                BX      LR
                ENDP

                LTORG
                ALIGN   4
                END
