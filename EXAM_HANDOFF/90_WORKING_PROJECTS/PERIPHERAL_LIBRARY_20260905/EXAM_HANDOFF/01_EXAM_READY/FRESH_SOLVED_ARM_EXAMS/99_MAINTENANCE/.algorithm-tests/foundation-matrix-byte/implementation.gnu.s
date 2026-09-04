.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_get_u8
matrix_get_u8:
                MUL     R1, R1, R2
                ADDS    R1, R1, R3
                LDRB    R0, [R0, R1]
                BX      LR
