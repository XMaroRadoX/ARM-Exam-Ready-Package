.syntax unified
.cpu cortex-m3
.thumb
.text
.global digital_root
digital_root:
        movs r3,#10
dr_outer:
        cmp r0,#10
        blo dr_done
        movs r1,#0
dr_inner:
        udiv r12,r0,r3
        mls r2,r12,r3,r0
        adds r1,r2
        mov r0,r12
        cmp r0,#0
        bne dr_inner
        mov r0,r1
        b dr_outer
dr_done:
        bx lr
.balign 4
