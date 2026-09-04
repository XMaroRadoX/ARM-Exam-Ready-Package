.syntax unified
.cpu cortex-m3
.thumb
        LDR R0, =0x7FFFFFFF
        ADDS R0, R0, #1
        BVS matched
        MOVS R2, #0
        B finished
matched:
        MOVS R2, #1
finished:
