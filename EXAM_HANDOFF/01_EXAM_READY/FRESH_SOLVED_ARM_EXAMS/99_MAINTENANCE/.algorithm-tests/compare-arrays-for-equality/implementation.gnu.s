.syntax unified
.cpu cortex-m3
.thumb
.text
.global arrays_equal
arrays_equal:
        cmp r2,#0
        beq aeq_yes
        cmp r0,#0
        beq aeq_no
        cmp r1,#0
        beq aeq_no
aeq_loop:
        ldr r3,[r0],#4
        ldr r12,[r1],#4
        cmp r3,r12
        bne aeq_no
        subs r2,#1
        bne aeq_loop
aeq_yes:
        movs r0,#1
        bx lr
aeq_no:
        movs r0,#0
        bx lr
.balign 4
