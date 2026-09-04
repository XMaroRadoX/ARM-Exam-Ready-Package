.syntax unified
.cpu cortex-m3
.thumb
        MOVS R1, #0xFE
        SXTB R0, R1
        UXTB R2, R1
