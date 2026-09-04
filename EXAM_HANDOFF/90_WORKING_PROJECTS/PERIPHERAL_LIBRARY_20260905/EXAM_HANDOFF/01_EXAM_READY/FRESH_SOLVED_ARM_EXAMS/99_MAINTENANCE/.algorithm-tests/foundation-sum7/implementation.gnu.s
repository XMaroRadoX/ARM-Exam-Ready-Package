.syntax unified
.cpu cortex-m3
.thumb
.text
.global sum7
sum7:
                MOV     R12, SP
                PUSH    {R4-R9, R12, LR}
                LDR     R4, [R12, #0]
                LDR     R5, [R12, #4]
                LDR     R6, [R12, #8]
                ADDS    R0, R0, R1
                ADDS    R0, R0, R2
                ADDS    R0, R0, R3
                ADDS    R0, R0, R4
                ADDS    R0, R0, R5
                ADDS    R0, R0, R6
                POP     {R4-R9, R12, PC}
