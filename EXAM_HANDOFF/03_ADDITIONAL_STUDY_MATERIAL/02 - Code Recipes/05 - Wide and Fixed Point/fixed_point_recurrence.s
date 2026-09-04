; Recommended exam template: signed Q15 multiplication with a 64-bit product.
; C prototype: int32_t q15_multiply(int32_t a, int32_t b);
; Returns the low 32 bits of (a*b)>>15. SMULL avoids a 32-bit overflow.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  q15_multiply

q15_multiply    PROC
                SMULL   R2, R3, R0, R1
                LSRS    R2, R2, #15
                ORR     R0, R2, R3, LSL #17
                BX      LR
                ENDP

                END
