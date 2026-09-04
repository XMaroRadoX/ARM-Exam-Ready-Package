.syntax unified
.cpu cortex-m3
.thumb
.text
.global q15_multiply
q15_multiply:
                SMULL   R2, R3, R0, R1
                LSRS    R2, R2, #15
                ORR     R0, R2, R3, LSL #17
                BX      LR
