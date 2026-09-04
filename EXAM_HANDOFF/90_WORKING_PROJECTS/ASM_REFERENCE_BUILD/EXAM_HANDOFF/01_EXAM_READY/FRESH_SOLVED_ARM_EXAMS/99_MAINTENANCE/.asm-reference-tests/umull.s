.syntax unified
.cpu cortex-m3
.thumb
        LDR R2, =0xFFFFFFFF
        MOVS R3, #2
        UMULL R0, R1, R2, R3
