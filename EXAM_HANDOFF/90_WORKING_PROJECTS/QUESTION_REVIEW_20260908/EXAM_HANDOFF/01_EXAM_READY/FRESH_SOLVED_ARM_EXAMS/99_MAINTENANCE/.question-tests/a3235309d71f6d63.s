.syntax unified
.cpu cortex-m3
.thumb
.equ DIM,10
.section .data
sequence:
.space DIM
.text
.global Reset_Handler
Reset_Handler:
                MOV     R4, #1
                MOV     R5, #0
                LDR     R6, =sequence
generate_loop:
                MOV     R0, R4
                MOV     R1, #131
                MOV     R2, #7
                MOV     R3, R5
                SUB     SP, SP, #8
                MOV     R12, #255
                STR     R12, [SP]
                BL      nextElementLCG
                ADD     SP, SP, #8
                STRB    R0, [R6, R5]
                MOV     R4, R0
                ADD     R5, R5, #1
                CMP     R5, #DIM
                BLO     generate_loop
finished:
                B       finished
.ltorg
.text
.global nextElementLCG
nextElementLCG:
                PUSH    {R4, LR}
                LDR     R4, [SP, #8]
                MUL     R0, R1, R0
                ADD     R0, R0, R2
                EOR     R0, R0, R3
                UDIV    R1, R0, R4
                MUL     R1, R1, R4
                SUB     R0, R0, R1
                POP     {R4, PC}
