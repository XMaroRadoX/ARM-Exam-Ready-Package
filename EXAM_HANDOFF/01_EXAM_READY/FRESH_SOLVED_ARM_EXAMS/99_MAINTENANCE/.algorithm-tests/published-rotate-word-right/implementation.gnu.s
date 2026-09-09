.syntax unified
.cpu cortex-m3
.thumb
.text
.global rotate_right_u32
rotate_right_u32:
        and r1,r1,#31
        ror r0,r0,r1
        bx lr
.balign 4
