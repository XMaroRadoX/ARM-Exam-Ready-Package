.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =values
        LDR R0, [R1, #4]
        B after_values
.balign 4
values:
.word 11,22
after_values:
