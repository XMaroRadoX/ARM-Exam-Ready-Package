.syntax unified
.cpu cortex-m3
.thumb
.text
.global checked_add_i32
checked_add_i32:
        cmp r2,#0
        beq cbo_bad
        adds r3,r0,r1
        bvs cbo_bad
        str r3,[r2]
        movs r0,#1
        bx lr
cbo_bad:
        movs r0,#0
        bx lr
.balign 4
