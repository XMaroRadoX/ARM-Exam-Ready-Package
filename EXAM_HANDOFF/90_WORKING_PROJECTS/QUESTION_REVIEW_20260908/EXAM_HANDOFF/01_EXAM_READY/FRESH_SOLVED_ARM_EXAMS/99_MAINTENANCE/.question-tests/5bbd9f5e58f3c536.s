.syntax unified
.cpu cortex-m3
.thumb
.text
.global bitwiseAffineTransformation
bitwiseAffineTransformation:
                PUSH    {R4-R10, LR}
                MOV     R4, R0
                UXTB    R5, R1
                UXTB    R6, R2
                MOVS    R7, #0
affine_row:
                CMP     R7, #8
                BHS     affine_done
                LDRB    R8, [R4, R7]
                ANDS    R8, R8, R5
                MOVS    R9, #0
                MOVS    R10, #8
affine_parity:
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
affine_next_row:
                ADDS    R7, R7, #1
                B       affine_row
affine_done:
                UXTB    R0, R6
                POP     {R4-R10, PC}
.ltorg
.balign 4
