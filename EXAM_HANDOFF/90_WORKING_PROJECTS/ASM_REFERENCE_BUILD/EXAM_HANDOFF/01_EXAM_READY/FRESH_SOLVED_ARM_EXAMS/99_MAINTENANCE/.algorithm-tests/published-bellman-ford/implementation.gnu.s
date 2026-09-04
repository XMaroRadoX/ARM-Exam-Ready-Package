.syntax unified
.cpu cortex-m3
.thumb
.text
.global bellman_ford
bellman_ford:
        cmp r3,r2
        bhs bf_bad
        cmp r2,#256
        bhi bf_bad
        cmp r1,#0
        beq bf_setup
        cmp r0,#0
        beq bf_bad
bf_setup:
        push {r4-r11,lr}
        sub sp,sp,#20
        str r3,[sp]
        mov r4,r0
        mov r5,r1
        mov r6,r2
        ldr r7,[sp,#56]
        cmp r7,#0
        beq bf_fail
        ldr r0,=357913941
        cmp r5,r0
        bhi bf_fail
        movs r9,#0
        ldr r11,=2147483647
bf_validate:
        cmp r9,r5
        bhs bf_initialize
        add r0,r9,r9,lsl #1
        add r0,r4,r0,lsl #2
        ldr r1,[r0]
        ldr r2,[r0,#4]
        cmp r1,r6
        bhs bf_fail
        cmp r2,r6
        bhs bf_fail
        adds r9,#1
        b bf_validate
bf_initialize:
        movs r9,#0
bf_init:
        cmp r9,r6
        bhs bf_start
        str r11,[r7,r9,lsl #2]
        adds r9,#1
        b bf_init
bf_start:
        ldr r0,[sp]
        movs r1,#0
        str r1,[r7,r0,lsl #2]
        movs r8,#1
bf_pass:
        movs r9,#0
        movs r10,#0
bf_edge:
        cmp r9,r5
        bhs bf_nextpass
        add r0,r9,r9,lsl #1
        add r0,r4,r0,lsl #2
        ldr r1,[r0]
        ldr r2,[r0,#4]
        ldr r3,[r0,#8]
        ldr r1,[r7,r1,lsl #2]
        cmp r1,r11
        beq bf_nextedge
        adds r1,r1,r3
        bvs bf_fail
        cmp r1,r11
        beq bf_fail
        ldr r3,[r7,r2,lsl #2]
        cmp r1,r3
        bge bf_nextedge
        cmp r8,r6
        beq bf_fail
        str r1,[r7,r2,lsl #2]
        movs r10,#1
bf_nextedge:
        adds r9,#1
        b bf_edge
bf_nextpass:
        cmp r10,#0
        beq bf_good
        adds r8,#1
        b bf_pass
bf_good:
        movs r0,#1
        b bf_return
bf_fail:
        movs r0,#0
bf_return:
        add sp,sp,#20
        pop {r4-r11,pc}
bf_bad:
        movs r0,#0
        bx lr
.balign 4
