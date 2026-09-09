.syntax unified
.cpu cortex-m3
.thumb
.text
.global bitwiseAffineTransformation
bitwiseAffineTransformation:
        PUSH    {R4-R7}
        MOVS    R3, #0
        MOVS    R4, #8
row_loop:
        LDRB    R5, [R0], #1
        AND     R5, R5, R1
        MOVS    R6, #0
        MOVS    R7, #8
bit_loop:
        AND     R12, R5, #1
        EOR     R6, R6, R12
        LSRS    R5, R5, #1
        SUBS    R7, R7, #1
        BNE     bit_loop
        LSLS    R3, R3, #1
        ORR     R3, R3, R6
        SUBS    R4, R4, #1
        BNE     row_loop
        EOR     R0, R3, R2
        UXTB    R0, R0
        POP     {R4-R7}
        BX      LR
