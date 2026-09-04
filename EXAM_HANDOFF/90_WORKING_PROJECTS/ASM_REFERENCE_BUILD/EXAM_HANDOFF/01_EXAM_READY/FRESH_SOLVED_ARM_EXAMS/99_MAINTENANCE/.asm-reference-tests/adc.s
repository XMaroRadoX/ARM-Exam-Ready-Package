.syntax unified
.cpu cortex-m3
.thumb
        LDR R0, =0xFFFFFFFF
        MOVS R1, #0
        MOVS R2, #1
        MOVS R3, #0
        ADDS R0, R0, R2
        ADC R1, R1, R3
