.syntax unified
.cpu cortex-m3
.thumb
        MOVS R1, #47
        MOVS R2, #10
        UDIV R0, R1, R2
        MLS R3, R0, R2, R1
