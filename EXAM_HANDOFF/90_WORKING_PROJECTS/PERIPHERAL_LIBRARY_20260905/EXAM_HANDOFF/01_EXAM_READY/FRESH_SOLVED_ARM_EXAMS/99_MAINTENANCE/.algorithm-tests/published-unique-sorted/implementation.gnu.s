.syntax unified
.cpu cortex-m3
.thumb
.text
.global unique_sorted
unique_sorted:
        cmp r0,#0
        beq uq_zero
        push {r4-r6,lr}
        movs r2,#0
        movs r6,#0
uq_loop:
        cmp r6,r1
        bhs uq_done
        ldr r3,[r0,r6,lsl #2]
        cmp r2,#0
        beq uq_write
        sub r4,r2,#1
        ldr r5,[r0,r4,lsl #2]
        cmp r3,r5
        beq uq_next
uq_write:
        str r3,[r0,r2,lsl #2]
        adds r2,#1
uq_next:
        adds r6,#1
        b uq_loop
uq_done:
        mov r0,r2
        pop {r4-r6,pc}
uq_zero:
        movs r0,#0
        bx lr
.balign 4
