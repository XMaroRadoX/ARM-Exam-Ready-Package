.syntax unified
.cpu cortex-m3
.thumb
        LDR R0, =0xFFFFFFFF
        MOVS R1, #1
        CMP R0, R1
