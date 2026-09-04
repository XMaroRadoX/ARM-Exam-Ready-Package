.syntax unified
.cpu cortex-m3
.thumb
.text
.global sorted_union
sorted_union:
        push {r4-r10,lr}
        ldr r4,[sp,#32]
        ldr r5,[sp,#36]
        adds r6,r1,r3
        bcs sm_bad
        cmp r5,r6
        blo sm_bad
        cmp r6,#0
        beq sm_empty
        cmp r4,#0
        beq sm_bad
        cmp r1,#0
        beq sm_bcheck
        cmp r0,#0
        beq sm_bad
sm_bcheck:
        cmp r3,#0
        beq sm_start
        cmp r2,#0
        beq sm_bad
sm_start:
        movs r6,#0
        movs r7,#0
        movs r8,#0
sm_loop:
        cmp r6,r1
        bhs sm_from_b
        cmp r7,r3
        bhs sm_from_a
        ldr r9,[r0,r6,lsl #2]
        ldr r10,[r2,r7,lsl #2]
        cmp r9,r10
        ble sm_from_a
sm_from_b:
        cmp r7,r3
        bhs sm_done
        ldr r9,[r2,r7,lsl #2]
        adds r7,#1
        b sm_accept
sm_from_a:
        ldr r9,[r0,r6,lsl #2]
        adds r6,#1
sm_accept:
        cmp r8,#0
        beq sm_write
        sub r10,r8,#1
        ldr r10,[r4,r10,lsl #2]
        cmp r10,r9
        beq sm_loop
sm_write:
        str r9,[r4,r8,lsl #2]
        adds r8,#1
        b sm_loop
sm_done:
        mov r0,r8
        pop {r4-r10,pc}
sm_empty:
        movs r0,#0
        pop {r4-r10,pc}
sm_bad:
        mvn r0,#0
        pop {r4-r10,pc}
.balign 4
