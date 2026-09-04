; Handwritten Cortex-M3 Thumb exam reference.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT pat_alg_dfs_stack_001
pat_alg_dfs_stack_001
        ldr r12,[sp]
        cmp r0,#0
        beq df_bad
        cmp r3,#0
        beq df_bad
        cmp r12,#0
        beq df_bad
        cmp r2,r1
        bhs df_bad
        push {r4-r10,lr}
        ldr r4,=65535
        cmp r1,r4
        bhi df_fail
        ldrb r4,[r3,r2]
        cmp r4,#0
        bne df_fail
        mov r4,r0
        mov r5,r1
        mov r6,r3
        mov r7,r12
        movs r8,#1
        movs r9,#0
        str r2,[r7]
        strb r8,[r6,r2]
df_outer
        cmp r8,#0
        beq df_done
        subs r8,#1
        ldr r10,[r7,r8,lsl #2]
        adds r9,#1
        mov r2,r5
df_neighbor
        cmp r2,#0
        beq df_outer
        subs r2,#1
        mla r0,r10,r5,r2
        ldrb r1,[r4,r0]
        cmp r1,#0
        beq df_neighbor
        ldrb r1,[r6,r2]
        cmp r1,#0
        bne df_neighbor
        movs r1,#1
        strb r1,[r6,r2]
        str r2,[r7,r8,lsl #2]
        adds r8,#1
        b df_neighbor
df_done
        mov r0,r9
        pop {r4-r10,pc}
df_fail
        pop {r4-r10,lr}
df_bad
        movs r0,#0
        bx lr
        LTORG
        ALIGN
        END
