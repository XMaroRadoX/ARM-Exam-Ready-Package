.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_fill
array_fill:
        cmp r1,#0
        beq afl_yes
        cmp r0,#0
        beq afl_bad
afl_loop:
        str r2,[r0],#4
        subs r1,#1
        bne afl_loop
afl_yes:
        movs r0,#1
        bx lr
afl_bad:
        movs r0,#0
        bx lr
.balign 4
