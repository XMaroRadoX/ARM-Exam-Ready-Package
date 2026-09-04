.syntax unified
.cpu cortex-m3
.thumb
        MOVS R0, #0
        CBZ R0, empty
        MOVS R1, #99
empty:
