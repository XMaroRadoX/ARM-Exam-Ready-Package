.syntax unified
.cpu cortex-m3
.thumb
        MOVS R1, #4
        MOVS R2, #10
        MOVS R3, #47
        MLS R0, R1, R2, R3
