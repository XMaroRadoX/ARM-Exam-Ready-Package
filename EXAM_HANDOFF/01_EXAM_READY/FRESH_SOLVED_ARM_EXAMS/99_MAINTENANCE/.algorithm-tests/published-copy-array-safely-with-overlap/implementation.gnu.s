.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_copy_overlap
array_copy_overlap:
        cmp r1,r3
        blo aco_bad
        cmp r3,#0
        beq aco_yes
        cmp r0,#0
        beq aco_bad
        cmp r2,#0
        beq aco_bad
        cmp r0,r2
        beq aco_yes
        blo aco_forward
        sub r12,r0,r2
        cmp r12,r3,lsl #2
        bhs aco_forward
        add r0,r0,r3,lsl #2
        add r2,r2,r3,lsl #2
aco_backward:
        ldr r12,[r2,#-4]!
        str r12,[r0,#-4]!
        subs r3,#1
        bne aco_backward
        b aco_yes
aco_forward:
        ldr r12,[r2],#4
        str r12,[r0],#4
        subs r3,#1
        bne aco_forward
aco_yes:
        movs r0,#1
        bx lr
aco_bad:
        movs r0,#0
        bx lr
.balign 4
