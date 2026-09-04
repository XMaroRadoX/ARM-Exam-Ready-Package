.syntax unified
.cpu cortex-m3
.thumb
        CMP R0, #0
        ITE EQ
        MOVEQ R1, #1
        MOVNE R1, #0
