.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =0xFFFFFFFF
        ADDS R0, R1, #1
