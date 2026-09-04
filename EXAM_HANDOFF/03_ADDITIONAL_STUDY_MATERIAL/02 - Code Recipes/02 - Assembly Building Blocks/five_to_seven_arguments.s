; Recommended exam template: access arguments 5-7 safely
; C prototype:
; uint32_t sum7(uint32_t a, uint32_t b, uint32_t c, uint32_t d,
;               uint32_t e, uint32_t f, uint32_t g);
; Arguments 1-4 are R0-R3. Arguments 5-7 are at the caller's original SP.
; Capture original SP before PUSH. Eight saved registers keep SP aligned.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  sum7

sum7            PROC
                MOV     R12, SP
                PUSH    {R4-R9, R12, LR}
                LDR     R4, [R12, #0]
                LDR     R5, [R12, #4]
                LDR     R6, [R12, #8]
                ADDS    R0, R0, R1
                ADDS    R0, R0, R2
                ADDS    R0, R0, R3
                ADDS    R0, R0, R4
                ADDS    R0, R0, R5
                ADDS    R0, R0, R6
                POP     {R4-R9, R12, PC}
                ENDP

                END
