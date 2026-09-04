.syntax unified
.cpu cortex-m3
.thumb
sum_words:
        MOVS R2, #0
        CBZ R1, sum_done
sum_loop:
        LDR R3, [R0], #4
        ADD R2, R2, R3
        SUBS R1, R1, #1
        BNE sum_loop
sum_done:
        MOV R0, R2
        BX LR
