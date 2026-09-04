.syntax unified
.cpu cortex-m3
.thumb
        PUSH {R4,LR}
        MOVS R4, #3
        MOV R0, R4
        POP {R4,PC}
