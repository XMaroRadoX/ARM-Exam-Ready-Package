.syntax unified
.cpu cortex-m3
.thumb
.text
.global add_square
add_square:
                PUSH    {R4, LR}
                MOV     R4, R1
                BL      square_value
                ADDS    R0, R0, R4
                POP     {R4, PC}
square_value:
                MUL     R0, R0, R0
                BX      LR
