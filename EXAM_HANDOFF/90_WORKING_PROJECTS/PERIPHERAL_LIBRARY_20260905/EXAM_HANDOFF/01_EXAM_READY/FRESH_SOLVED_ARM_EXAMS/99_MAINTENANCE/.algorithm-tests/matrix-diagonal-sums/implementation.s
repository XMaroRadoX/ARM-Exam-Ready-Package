; Main and secondary diagonal sums
; int diagonal_sums(const int16_t *a, uint32_t n, int64_t *out, uint32_t capacity)
; Square row-major matrix with n<=256. Write main and secondary sums into two 64-bit outputs. Empty matrix yields two zeros. Require capacity>=2 and valid output; nonempty input must be valid and disjoint.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT diagonal_sums
diagonal_sums
        cmp r2,#0
        beq dg_bad
        cmp r3,#2
        blo dg_bad
        cmp r1,#256
        bhi dg_bad
        cmp r1,#0
        beq dg_start
        cmp r0,#0
        beq dg_bad
dg_start
        push {r4-r8,lr}
        movs r4,#0
        movs r5,#0
        movs r6,#0
dg_loop
        cmp r6,r1
        bhs dg_done
        mla r7,r6,r1,r6
        lsl r7,r7,#1
        ldrsh r8,[r0,r7]
        add r4,r8
        mul r7,r6,r1
        add r7,r1
        subs r7,#1
        sub r7,r6
        lsl r7,r7,#1
        ldrsh r8,[r0,r7]
        add r5,r8
        adds r6,#1
        b dg_loop
dg_done
        str r4,[r2]
        asr r4,r4,#31
        str r4,[r2,#4]
        str r5,[r2,#8]
        asr r5,r5,#31
        str r5,[r2,#12]
        movs r0,#1
        pop {r4-r8,pc}
dg_bad
        movs r0,#0
        bx lr

        ALIGN
        END
