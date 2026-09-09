.syntax unified
.cpu cortex-m3
.thumb
.text
.global LCGsequence
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
