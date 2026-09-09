.syntax unified
.cpu cortex-m3
.thumb
.text
.global checked_multiply_i32
checked_multiply_i32:
        cmp r2,#0
        beq cbo_bad
        smull r3,r12,r0,r1
        asr r1,r3,#31
        cmp r12,r1
        bne cbo_bad
        str r3,[r2]
        movs r0,#1
        bx lr
cbo_bad:
        movs r0,#0
        bx lr
.balign 4
