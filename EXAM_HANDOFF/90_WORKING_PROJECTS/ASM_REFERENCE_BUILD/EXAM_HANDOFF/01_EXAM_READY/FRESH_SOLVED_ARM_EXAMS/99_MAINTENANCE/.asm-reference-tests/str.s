.syntax unified
.cpu cortex-m3
.thumb
        MOVS R0, #0xAB
        STRB R0, [R1]
