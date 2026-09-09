.syntax unified
.cpu cortex-m3
.thumb
.text
.global integer_is_odd
integer_is_odd:
        and r0,r0,#1
        bx lr
.balign 4
