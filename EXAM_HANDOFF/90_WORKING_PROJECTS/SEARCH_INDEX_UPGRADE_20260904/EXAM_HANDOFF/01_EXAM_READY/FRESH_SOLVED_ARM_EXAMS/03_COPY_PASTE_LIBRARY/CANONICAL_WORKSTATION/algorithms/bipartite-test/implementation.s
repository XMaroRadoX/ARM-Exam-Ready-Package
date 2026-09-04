; Bipartite graph test
; int graph_is_bipartite(const uint8_t *a, size_t n, int8_t *color, size_t *queue)
; Undirected byte adjacency matrix, n<=256. Supply n color bytes and n queue words. Return 1 for a two-coloring across all components, or 0 on conflict or invalid input.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT graph_is_bipartite
graph_is_bipartite
        cmp r0,#0
        beq bi_bad
        cmp r2,#0
        beq bi_bad
        cmp r3,#0
        beq bi_bad
        cmp r1,#256
        bhi bi_bad
        push {r4-r10,lr}
        movs r4,#0
        movs r5,#255
bi_init
        cmp r4,r1
        bhs bi_start
        strb r5,[r2,r4]
        adds r4,#1
        b bi_init
bi_start
        movs r4,#0
bi_component
        cmp r4,r1
        bhs bi_ok
        ldrsb r5,[r2,r4]
        cmp r5,#0
        bge bi_next_component
        movs r5,#0
        strb r5,[r2,r4]
        str r4,[r3]
        movs r6,#1
bi_queue
        cmp r5,r6
        bhs bi_next_component
        ldr r7,[r3,r5,lsl #2]
        adds r5,#1
        movs r8,#0
bi_edge
        cmp r8,r1
        bhs bi_queue
        mla r10,r7,r1,r8
        ldrb r9,[r0,r10]
        cmp r9,#0
        beq bi_next_edge
        ldrsb r9,[r2,r8]
        ldrb r10,[r2,r7]
        cmp r9,#0
        bge bi_compare
        eor r10,r10,#1
        strb r10,[r2,r8]
        str r8,[r3,r6,lsl #2]
        adds r6,#1
        b bi_next_edge
bi_compare
        cmp r9,r10
        beq bi_fail
bi_next_edge
        adds r8,#1
        b bi_edge
bi_next_component
        adds r4,#1
        b bi_component
bi_ok
        movs r0,#1
        pop {r4-r10,pc}
bi_fail
        pop {r4-r10,lr}
bi_bad
        movs r0,#0
        bx lr

        ALIGN
        END
