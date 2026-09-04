; Distinct sorted intersection
; uint32_t sorted_intersection(const int32_t *a, uint32_t n, const int32_t *b, uint32_t m, int32_t *out, uint32_t capacity)
; Inputs are signed ascending arrays. Require capacity>=n+m without count overflow, and disjoint output. Return output count or UINT32_MAX before writes on invalid input. Output each selected value once.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT sorted_intersection
sorted_intersection
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
sm_bcheck
        cmp r3,#0
        beq sm_start
        cmp r2,#0
        beq sm_bad
sm_start
        movs r6,#0
        movs r7,#0
        movs r8,#0
sm_loop
        cmp r6,r1
        bhs sm_done
        cmp r7,r3
        bhs sm_done
        ldr r9,[r0,r6,lsl #2]
        ldr r10,[r2,r7,lsl #2]
        cmp r9,r10
        blt sm_ia
        bgt sm_ib
        adds r6,#1
        adds r7,#1
        b sm_accept
sm_ia
        adds r6,#1
        b sm_loop
sm_ib
        adds r7,#1
        b sm_loop
sm_accept
        cmp r8,#0
        beq sm_write
        sub r10,r8,#1
        ldr r10,[r4,r10,lsl #2]
        cmp r10,r9
        beq sm_loop
sm_write
        str r9,[r4,r8,lsl #2]
        adds r8,#1
        b sm_loop
sm_done
        mov r0,r8
        pop {r4-r10,pc}
sm_empty
        movs r0,#0
        pop {r4-r10,pc}
sm_bad
        mvn r0,#0
        pop {r4-r10,pc}

        ALIGN
        END
