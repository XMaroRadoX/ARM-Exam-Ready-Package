.syntax unified
.cpu cortex-m3
.thumb
fifth:
        PUSH {R4,LR}
        LDR R0, [SP, #8]
        POP {R4,PC}
