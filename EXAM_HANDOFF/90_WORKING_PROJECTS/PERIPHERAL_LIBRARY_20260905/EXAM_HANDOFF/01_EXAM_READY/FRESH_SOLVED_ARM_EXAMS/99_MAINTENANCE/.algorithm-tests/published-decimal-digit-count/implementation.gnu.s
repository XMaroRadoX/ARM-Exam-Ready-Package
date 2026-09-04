.syntax unified
.cpu cortex-m3
.thumb
.text
.global decimal_digit_count
decimal_digit_count:
        movs r1,#0
        movs r2,#10
dd_loop:
        udiv r12,r0,r2
        mls r3,r12,r2,r0
        adds r1,#1
        mov r0,r12
        cmp r0,#0
        bne dd_loop
        mov r0,r1
        bx lr
.balign 4
