; Topological sort
; size_t topological_sort(const uint8_t *a, size_t n, size_t *degree, size_t *queue, size_t *out)
; Byte adjacency matrix, n<=256. degree, queue and out each hold n words and do not overlap. Return n for a complete order; return 0 on a cycle or invalid input. A cycle may leave a valid partial order.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT topological_sort
topological_sort
        cmp r0,#0
        beq tp_bad
        cmp r2,#0
        beq tp_bad
        cmp r3,#0
        beq tp_bad
        cmp r1,#256
        bhi tp_bad
        push {r4-r11,lr}
        sub sp,sp,#4
        ldr r4,[sp,#40]
        cmp r4,#0
        beq tp_fail
        movs r5,#0
        movs r8,#0
tp_init
        cmp r5,r1
        bhs tp_begin
        movs r6,#0
        movs r10,#0
tp_degree
        cmp r6,r1
        bhs tp_ds
        mla r11,r6,r1,r5
        ldrb r9,[r0,r11]
        cmp r9,#0
        beq tp_dn
        adds r10,#1
tp_dn
        adds r6,#1
        b tp_degree
tp_ds
        str r10,[r2,r5,lsl #2]
        cmp r10,#0
        bne tp_in
        str r5,[r3,r8,lsl #2]
        adds r8,#1
tp_in
        adds r5,#1
        b tp_init
tp_begin
        movs r7,#0
tp_loop
        cmp r7,r8
        bhs tp_check
        ldr r9,[r3,r7,lsl #2]
        str r9,[r4,r7,lsl #2]
        adds r7,#1
        movs r6,#0
tp_edges
        cmp r6,r1
        bhs tp_loop
        mla r11,r9,r1,r6
        ldrb r10,[r0,r11]
        cmp r10,#0
        beq tp_en
        ldr r10,[r2,r6,lsl #2]
        subs r10,#1
        str r10,[r2,r6,lsl #2]
        bne tp_en
        str r6,[r3,r8,lsl #2]
        adds r8,#1
tp_en
        adds r6,#1
        b tp_edges
tp_check
        cmp r7,r1
        bne tp_fail
        mov r0,r7
        b tp_return
tp_fail
        movs r0,#0
tp_return
        add sp,sp,#4
        pop {r4-r11,pc}
tp_bad
        movs r0,#0
        bx lr

        ALIGN
        END
