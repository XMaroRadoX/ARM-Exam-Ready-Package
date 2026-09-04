.syntax unified
.cpu cortex-m3
.thumb
        MOVS R0, #15
        BIC R0, R0, #8
        EOR R0, R0, #1
