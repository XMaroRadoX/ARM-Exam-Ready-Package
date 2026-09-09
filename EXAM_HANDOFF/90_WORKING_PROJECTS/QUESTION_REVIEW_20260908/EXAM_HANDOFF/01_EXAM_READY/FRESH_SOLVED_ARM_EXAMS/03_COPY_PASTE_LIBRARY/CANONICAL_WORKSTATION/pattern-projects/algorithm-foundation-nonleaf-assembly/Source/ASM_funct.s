; Recommended exam template: function that calls another function
; C prototype: uint32_t add_square(uint32_t a, uint32_t b);
; R4 is callee-saved. BL overwrites LR, so both are saved.
; PUSH/POP cover two registers (8 bytes), preserving public-call alignment.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  add_square

add_square      PROC
                PUSH    {R4, LR}
                MOV     R4, R1
                BL      square_value
                ADDS    R0, R0, R4
                POP     {R4, PC}
                ENDP

square_value    PROC
                MUL     R0, R0, R0
                BX      LR
                ENDP

                END
