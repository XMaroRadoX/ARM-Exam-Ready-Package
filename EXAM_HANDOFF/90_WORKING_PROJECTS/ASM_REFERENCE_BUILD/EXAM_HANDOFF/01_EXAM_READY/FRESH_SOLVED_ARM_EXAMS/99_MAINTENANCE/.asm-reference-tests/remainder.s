.syntax unified
.cpu cortex-m3
.thumb
        UDIV R2, R0, R1
        MLS R0, R2, R1, R0
