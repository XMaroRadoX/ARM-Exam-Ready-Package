.syntax unified
.cpu cortex-m3
.thumb
        PUSH {R4,LR}
        BL helper
        POP {R4,PC}
helper:
        ADDS R0, R0, #1
        BX LR
