.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =0x12345678
        REV R0, R1
        MOVS R2, #16
        CLZ R3, R2
