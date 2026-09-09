.syntax unified
.cpu cortex-m3
.thumb
.text
.global LCGsequence
.equ DIM,10
.section .data
lcg_test_values:
.space DIM
.text
.global Reset_Handler
Reset_Handler:
                SUB     SP, SP, #8
                MOV     R4, #256
                STR     R4, [SP]
                LDR     R4, =lcg_test_values
                MOVS    R0, #6
                MOVS    R5, #0
lcg_reset_loop:
                MOVS    R1, #157
                MOVS    R2, #3
                MOVS    R3, #3
                BL      LCGsequence
                STRB    R0, [R4, R5]
                ADDS    R5, R5, #1
                CMP     R5, #DIM
                BLO     lcg_reset_loop
                ADD     SP, SP, #8
                B       lcg_finished
lcg_finished:
B       lcg_finished
LCGsequence:
                LDR     R12, [SP]
                LSR     R3, R0, R3
                MUL     R0, R0, R1
                ADDS    R0, R0, R2
                EORS    R0, R0, R3
                UDIV    R1, R0, R12
                MLS     R0, R1, R12, R0
                BX      LR
.ltorg
.balign 4
