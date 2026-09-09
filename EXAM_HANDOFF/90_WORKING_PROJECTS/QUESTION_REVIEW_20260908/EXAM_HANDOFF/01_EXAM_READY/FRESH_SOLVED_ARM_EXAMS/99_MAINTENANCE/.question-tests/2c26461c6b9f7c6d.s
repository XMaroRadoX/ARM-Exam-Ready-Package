.syntax unified
.cpu cortex-m3
.thumb
.text
.global Maclaurin_cos
Maclaurin_cos:
                PUSH    {R4-R9, LR}
                SUB     SP, SP, #4
                MOV     R4, R0
                MOV     R5, R1
                MOVS    R6, #100
                MOV     R7, R6
                MOVS    R8, #1
sin_term_loop:
                CMP     R8, R5
                BHI     sin_done
                MUL     R0, R4, R4
                MUL     R0, R6, R0
                RSBS    R0, R0, #0
                LSLS    R2, R8, #1
                SUBS    R1, R2, #1
                MUL     R1, R1, R2
                MOVS    R2, #100
                MUL     R1, R1, R2
                SDIV    R6, R0, R1
                ADDS    R7, R7, R6
                ADDS    R8, R8, #1
                B       sin_term_loop
sin_done:
                MOV     R0, R7
                ADD     SP, SP, #4
                POP     {R4-R9, PC}
.ltorg
.balign 4
