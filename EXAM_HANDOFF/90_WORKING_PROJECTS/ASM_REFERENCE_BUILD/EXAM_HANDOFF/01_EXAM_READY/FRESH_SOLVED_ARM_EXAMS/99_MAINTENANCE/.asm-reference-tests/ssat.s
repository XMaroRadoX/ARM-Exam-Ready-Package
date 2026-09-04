.syntax unified
.cpu cortex-m3
.thumb
        MOVW R1, #300
        USAT R0, #8, R1
