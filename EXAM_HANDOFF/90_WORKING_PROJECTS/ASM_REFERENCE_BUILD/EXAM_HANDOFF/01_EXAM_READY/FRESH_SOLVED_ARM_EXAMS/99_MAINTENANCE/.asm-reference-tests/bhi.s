.syntax unified
.cpu cortex-m3
.thumb
        MOVS R0, #7
        CMP R0, #5
        BHI matched
        MOVS R2, #0
        B finished
matched:
        MOVS R2, #1
finished:
