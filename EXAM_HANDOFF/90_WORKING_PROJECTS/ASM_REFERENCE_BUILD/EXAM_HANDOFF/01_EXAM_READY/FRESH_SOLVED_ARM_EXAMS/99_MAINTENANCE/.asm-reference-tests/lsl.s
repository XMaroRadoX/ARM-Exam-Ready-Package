.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =0xFFFFFFFC
        LSR R0, R1, #1
        ASR R2, R1, #1
