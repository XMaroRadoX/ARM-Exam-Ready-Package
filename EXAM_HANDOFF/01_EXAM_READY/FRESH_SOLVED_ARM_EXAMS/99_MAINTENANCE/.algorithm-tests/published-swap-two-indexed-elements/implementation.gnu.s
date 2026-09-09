.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_swap_indexes
array_swap_indexes:
        cmp r0,#0
        beq asi_bad
        cmp r2,r1
        bhs asi_bad
        cmp r3,r1
        bhs asi_bad
        ldr r1,[r0,r2,lsl #2]
        ldr r12,[r0,r3,lsl #2]
        str r12,[r0,r2,lsl #2]
        str r1,[r0,r3,lsl #2]
        movs r0,#1
        bx lr
asi_bad:
        movs r0,#0
        bx lr
.balign 4
