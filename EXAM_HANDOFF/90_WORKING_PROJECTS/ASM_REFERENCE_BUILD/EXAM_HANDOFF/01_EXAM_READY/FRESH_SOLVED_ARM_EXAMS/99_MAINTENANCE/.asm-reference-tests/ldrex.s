.syntax unified
.cpu cortex-m3
.thumb
retry:
        LDREX R1, [R0]
        ADD R1, R1, #1
        STREX R2, R1, [R0]
        CMP R2, #0
        BNE retry
