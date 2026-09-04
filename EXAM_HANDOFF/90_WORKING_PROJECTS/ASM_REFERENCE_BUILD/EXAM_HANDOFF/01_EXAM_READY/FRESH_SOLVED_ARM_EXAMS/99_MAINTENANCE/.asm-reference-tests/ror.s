.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =0x12345678
        ROR R0, R1, #8
