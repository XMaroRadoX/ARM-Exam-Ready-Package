.syntax unified
.cpu cortex-m3
.thumb
.text
.global prim_mst
prim_mst:
        cmp r0,#0
        beq pr_bad
        cmp r3,#0
        beq pr_bad
        cmp r2,r1
        bhs pr_bad
        cmp r1,#256
        bhi pr_bad
        push {r4-r11,lr}
        sub sp,sp,#4
        ldr r4,[sp,#40]
        cmp r4,#0
        beq pr_fail
        movs r9,#0
        mvn r10,#0
        movs r11,#0
pr_init:
        cmp r9,r1
        bhs pr_start
        str r10,[r3,r9,lsl #2]
        strb r11,[r4,r9]
        adds r9,#1
        b pr_init
pr_start:
        str r11,[r3,r2,lsl #2]
        movs r5,#0
        movs r6,#0
pr_outer:
        cmp r6,r1
        bhs pr_done
        mov r7,r1
        mvn r8,#0
        movs r9,#0
pr_select:
        cmp r9,r1
        bhs pr_accept
        ldrb r10,[r4,r9]
        cmp r10,#0
        bne pr_sn
        ldr r10,[r3,r9,lsl #2]
        cmp r10,r8
        bhs pr_sn
        mov r8,r10
        mov r7,r9
pr_sn:
        adds r9,#1
        b pr_select
pr_accept:
        cmp r7,r1
        beq pr_fail
        adds r5,r5,r8
        bcs pr_fail
        cmn r5,#1
        beq pr_fail
        movs r10,#1
        strb r10,[r4,r7]
        movs r9,#0
pr_edges:
        cmp r9,r1
        bhs pr_next
        ldrb r10,[r4,r9]
        cmp r10,#0
        bne pr_en
        mla r12,r7,r1,r9
        ldr r10,[r0,r12,lsl #2]
        cmp r10,#0
        beq pr_en
        ldr r11,[r3,r9,lsl #2]
        cmp r10,r11
        bhs pr_en
        str r10,[r3,r9,lsl #2]
pr_en:
        adds r9,#1
        b pr_edges
pr_next:
        adds r6,#1
        b pr_outer
pr_done:
        mov r0,r5
        b pr_return
pr_fail:
        mvn r0,#0
pr_return:
        add sp,sp,#4
        pop {r4-r11,pc}
pr_bad:
        mvn r0,#0
        bx lr
.balign 4
