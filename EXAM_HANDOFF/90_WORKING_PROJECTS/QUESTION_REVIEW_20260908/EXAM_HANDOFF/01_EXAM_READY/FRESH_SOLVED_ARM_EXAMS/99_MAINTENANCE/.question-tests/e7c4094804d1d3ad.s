.syntax unified
.cpu cortex-m3
.thumb
.text
.global transpose
.global transposition
transposition:
transpose:
                PUSH    {R4-R10, LR}
                MOV     R4, R0
                MOV     R5, R1
                MOVS    R6, #0
transpose_clear:
                CMP     R6, #8
                BHS     transpose_rows
                MOVS    R7, #0
                STRB    R7, [R5, R6]
                ADDS    R6, R6, #1
                B       transpose_clear
transpose_rows:
                MOVS    R6, #0
transpose_row_loop:
                CMP     R6, #8
                BHS     transpose_done
                LDRB    R7, [R4, R6]
                MOVS    R8, #0
transpose_bit_loop:
                CMP     R8, #8
                BHS     transpose_next_row
                MOVS    R9, #0x80
                LSR     R9, R9, R8
                TST     R7, R9
                BEQ     transpose_next_bit
                LDRB    R10, [R5, R8]
                MOVS    R9, #0x80
                LSR     R9, R9, R6
                ORRS    R10, R10, R9
                STRB    R10, [R5, R8]
transpose_next_bit:
                ADDS    R8, R8, #1
                B       transpose_bit_loop
transpose_next_row:
                ADDS    R6, R6, #1
                B       transpose_row_loop
transpose_done:
                POP     {R4-R10, PC}
.ltorg
.balign 4
