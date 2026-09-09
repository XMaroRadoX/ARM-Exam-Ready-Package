                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  bitwiseAffineTransformation

; uint32_t bitwiseAffineTransformation(const uint8_t *A, uint32_t b,
;                                       uint32_t c)
bitwiseAffineTransformation PROC
                PUSH    {R4-R10, LR}
                MOV     R4, R0          ; Matrix address.
                UXTB    R5, R1          ; Eight-bit vector b.
                UXTB    R6, R2          ; Result starts with vector c.
                MOVS    R7, #0          ; Matrix row.

affine_row
                CMP     R7, #8
                BHS     affine_done

                LDRB    R8, [R4, R7]
                ANDS    R8, R8, R5
                MOVS    R9, #0          ; Parity.
                MOVS    R10, #8

affine_parity
                AND     R12, R8, #1
                EORS    R9, R9, R12
                LSRS    R8, R8, #1
                SUBS    R10, R10, #1
                BNE     affine_parity

                CMP     R9, #0
                BEQ     affine_next_row
                MOVS    R8, #1
                MOVS    R10, #7
                SUBS    R10, R10, R7
                LSL     R8, R8, R10
                EORS    R6, R6, R8

affine_next_row
                ADDS    R7, R7, #1
                B       affine_row

affine_done
                UXTB    R0, R6
                POP     {R4-R10, PC}
                ENDP

                LTORG
                ALIGN   4
                END
