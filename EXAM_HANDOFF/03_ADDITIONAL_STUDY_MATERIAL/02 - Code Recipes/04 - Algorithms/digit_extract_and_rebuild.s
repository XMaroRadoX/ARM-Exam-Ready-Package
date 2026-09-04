; Recommended exam template: reverse the decimal digits of an unsigned word.
; C prototype: uint32_t reverse_decimal(uint32_t value);
; UDIV gives the quotient; MLS reconstructs remainder = value - quotient*10.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  reverse_decimal

reverse_decimal PROC
                PUSH    {R4-R6, LR}
                MOV     R4, R0
                MOVS    R5, #0
                MOVS    R6, #10
digit_loop      CMP     R4, #0
                BEQ     digit_done
                UDIV    R1, R4, R6
                MLS     R2, R1, R6, R4
                MUL     R5, R5, R6
                ADDS    R5, R5, R2
                MOV     R4, R1
                B       digit_loop
digit_done      MOV     R0, R5
                POP     {R4-R6, PC}
                ENDP

                END
