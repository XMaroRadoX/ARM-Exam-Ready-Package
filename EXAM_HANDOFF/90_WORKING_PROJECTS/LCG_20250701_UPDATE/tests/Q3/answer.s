.syntax unified
.cpu cortex-m3
.thumb
.text
.global nextElementLCG
.thumb_func
nextElementLCG:
                PUSH    {R4, LR}
                LDR     R4, [SP, #8]
                MUL     R0, R1, R0
                ADD     R0, R0, R2
                EOR     R0, R0, R3
                UDIV    R1, R0, R4
                MUL     R1, R1, R4
                SUB     R0, R0, R1
                POP     {R4, PC}
