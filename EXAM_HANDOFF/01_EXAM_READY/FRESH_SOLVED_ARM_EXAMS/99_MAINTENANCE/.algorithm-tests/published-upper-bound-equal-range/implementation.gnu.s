.syntax unified
.cpu cortex-m3
.thumb
.text
.global upper_bound_i32
upper_bound_i32:
        cmp r0,#0
        beq ub_zero
        push {r4,r5}
        movs r3,#0
ub_loop:
        cmp r3,r1
        bhs ub_done
        sub r12,r1,r3
        lsr r12,r12,#1
        add r12,r3
        ldr r4,[r0,r12,lsl #2]
        cmp r4,r2
        bgt ub_left
        add r3,r12,#1
        b ub_loop
ub_left:
        mov r1,r12
        b ub_loop
ub_done:
        mov r0,r3
        pop {r4,r5}
        bx lr
ub_zero:
        movs r0,#0
        bx lr
.balign 4
