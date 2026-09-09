.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_insert_at
array_insert_at:
        cmp r0,#0
        beq ains_bad
        cmp r1,#0
        beq ains_bad
        ldr r12,[r1]
        cmp r12,r2
        bhs ains_bad
        cmp r3,r12
        bhi ains_bad
        push {r4,lr}
        ldr r4,[sp,#8]
        mov r2,r12
ains_shift:
        cmp r2,r3
        beq ains_place
        sub r12,r2,#1
        ldr r12,[r0,r12,lsl #2]
        str r12,[r0,r2,lsl #2]
        subs r2,#1
        b ains_shift
ains_place:
        str r4,[r0,r3,lsl #2]
        ldr r2,[r1]
        adds r2,#1
        str r2,[r1]
        movs r0,#1
        pop {r4,pc}
ains_bad:
        movs r0,#0
        bx lr
.balign 4
