; Kruskal minimum spanning tree
; typedef struct{size_t u,v;unsigned w;}MstEdge;
; unsigned kruskal_mst(const MstEdge *edges, size_t m, size_t n, size_t *parent)
; Supply edges sorted by nondecreasing weight, n=1..256, valid endpoints and n parent words. Return MST weight or UINT_MAX for invalid ordering/endpoints, disconnection or total overflow. This generic MST differs from the supplied maze-generation exam.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT kruskal_mst
kruskal_mst
        cmp r3,#0
        beq kr_bad
        cmp r2,#1
        blo kr_bad
        cmp r2,#256
        bhi kr_bad
        cmp r1,#0
        beq kr_setup
        cmp r0,#0
        beq kr_bad
kr_setup
        push {r4-r11,lr}
        sub sp,sp,#12
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        ldr r0,=357913941
        cmp r5,r0
        bhi kr_fail
        movs r8,#0
        movs r9,#0
kr_validate
        cmp r8,r5
        bhs kr_initialize
        add r11,r8,r8,lsl #1
        add r11,r4,r11,lsl #2
        ldr r0,[r11]
        cmp r0,r6
        bhs kr_fail
        ldr r0,[r11,#4]
        cmp r0,r6
        bhs kr_fail
        ldr r0,[r11,#8]
        cmp r0,r9
        blo kr_fail
        mov r9,r0
        adds r8,#1
        b kr_validate
kr_initialize
        movs r8,#0
kr_init
        cmp r8,r6
        bhs kr_start
        str r8,[r7,r8,lsl #2]
        adds r8,#1
        b kr_init
kr_start
        movs r8,#0
        movs r9,#0
        movs r10,#0
kr_loop
        add r0,r9,#1
        cmp r0,r6
        beq kr_done
        cmp r8,r5
        bhs kr_fail
        add r11,r8,r8,lsl #1
        add r11,r4,r11,lsl #2
        mov r0,r7
        ldr r1,[r11]
        bl kr_root
        str r0,[sp]
        mov r0,r7
        ldr r1,[r11,#4]
        bl kr_root
        ldr r1,[sp]
        cmp r0,r1
        beq kr_next
        ldr r2,[r11,#8]
        adds r10,r10,r2
        bcs kr_fail
        cmn r10,#1
        beq kr_fail
        str r1,[r7,r0,lsl #2]
        adds r9,#1
kr_next
        adds r8,#1
        b kr_loop
kr_done
        mov r0,r10
        b kr_return
kr_fail
        mvn r0,#0
kr_return
        add sp,sp,#12
        pop {r4-r11,pc}
kr_bad
        mvn r0,#0
        bx lr
kr_root
        ldr r2,[r0,r1,lsl #2]
        cmp r2,r1
        beq kr_root_done
        ldr r3,[r0,r2,lsl #2]
        str r3,[r0,r1,lsl #2]
        mov r1,r3
        b kr_root
kr_root_done
        mov r0,r1
        bx lr
        ALIGN
        END
