.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_subtract_i32
matrix_subtract_i32:
        ldr r12,[sp]
        push {r4-r9,lr}
        sub sp,sp,#4
        ldr r4,[sp,#36]
        cmp r2,#256
        bhi mbo_fail
        cmp r3,#256
        bhi mbo_fail
        mul r5,r2,r3
        cmp r4,r5
        blo mbo_fail
        cmp r5,#0
        beq mbo_yes
        cmp r0,#0
        beq mbo_fail
        cmp r1,#0
        beq mbo_fail
        cmp r12,#0
        beq mbo_fail
        movs r6,#0
mbo_check:
        cmp r6,r5
        bhs mbo_write_start
        ldr r7,[r0,r6,lsl #2]
        ldr r8,[r1,r6,lsl #2]
        subs r9,r7,r8
        bvs mbo_fail
        adds r6,#1
        b mbo_check
mbo_write_start:
        movs r6,#0
mbo_write:
        cmp r6,r5
        bhs mbo_yes
        ldr r7,[r0,r6,lsl #2]
        ldr r8,[r1,r6,lsl #2]
        subs r9,r7,r8
        str r9,[r12,r6,lsl #2]
        adds r6,#1
        b mbo_write
mbo_yes:
        movs r0,#1
        b mbo_return
mbo_fail:
        movs r0,#0
mbo_return:
        add sp,sp,#4
        pop {r4-r9,pc}
.balign 4
