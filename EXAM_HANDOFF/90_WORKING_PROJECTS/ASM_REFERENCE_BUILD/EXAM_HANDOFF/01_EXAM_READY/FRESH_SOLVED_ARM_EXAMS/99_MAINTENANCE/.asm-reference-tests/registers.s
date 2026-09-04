.syntax unified
.cpu cortex-m3
.thumb
        PUSH {R4,LR}
        MOV R4, R0
        BL helper
        ADD R0, R0, R4
        POP {R4,PC}

helper:
 bx lr
