; Floyd-Warshall all-pairs paths
; int floyd_warshall(int *distance, size_t n, int infinity)
; In-place distance matrix, n<=256, positive infinity sentinel. Finite distances must be less than infinity; initialize diagonal to zero. Candidates at or above infinity remain unrepresentable. Return 0 on invalid input, signed overflow or negative cycle, possibly after partial updates.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT floyd_warshall
floyd_warshall
        cmp r0,#0
        beq fw_bad
        cmp r1,#256
        bhi fw_bad
        cmp r2,#0
        ble fw_bad
        push {r4-r10,lr}
        movs r4,#0
fw_k
        cmp r4,r1
        bhs fw_diag_start
        movs r5,#0
fw_i
        cmp r5,r1
        bhs fw_kn
        movs r6,#0
fw_j
        cmp r6,r1
        bhs fw_in
        mla r7,r5,r1,r4
        ldr r8,[r0,r7,lsl #2]
        cmp r8,r2
        beq fw_jn
        mla r7,r4,r1,r6
        ldr r9,[r0,r7,lsl #2]
        cmp r9,r2
        beq fw_jn
        adds r8,r8,r9
        bvs fw_fail
        mla r7,r5,r1,r6
        ldr r10,[r0,r7,lsl #2]
        cmp r8,r10
        bge fw_jn
        str r8,[r0,r7,lsl #2]
fw_jn
        adds r6,#1
        b fw_j
fw_in
        adds r5,#1
        b fw_i
fw_kn
        adds r4,#1
        b fw_k
fw_diag_start
        movs r4,#0
fw_diag
        cmp r4,r1
        bhs fw_ok
        mla r5,r4,r1,r4
        ldr r6,[r0,r5,lsl #2]
        cmp r6,#0
        blt fw_fail
        adds r4,#1
        b fw_diag
fw_ok
        movs r0,#1
        pop {r4-r10,pc}
fw_fail
        pop {r4-r10,lr}
fw_bad
        movs r0,#0
        bx lr

        ALIGN
        END
