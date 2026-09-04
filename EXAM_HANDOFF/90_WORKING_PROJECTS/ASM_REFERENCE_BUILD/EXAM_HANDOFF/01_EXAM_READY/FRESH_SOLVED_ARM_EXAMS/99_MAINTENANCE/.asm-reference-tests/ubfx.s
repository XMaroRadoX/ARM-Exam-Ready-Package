.syntax unified
.cpu cortex-m3
.thumb
        MOVS R1, #0x70
        UBFX R0, R1, #4, #3
        SBFX R2, R1, #4, #3
