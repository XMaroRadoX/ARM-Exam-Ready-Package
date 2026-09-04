.syntax unified
.cpu cortex-m3
.thumb
        STMFD SP!, {R4,LR}
        MOVS R4, #9
        LDMFD SP!, {R4,PC}
