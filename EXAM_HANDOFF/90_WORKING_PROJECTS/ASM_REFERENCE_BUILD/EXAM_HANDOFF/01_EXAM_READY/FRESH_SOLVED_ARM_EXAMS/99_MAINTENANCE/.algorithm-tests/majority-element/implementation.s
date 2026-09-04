; Majority element with verification
; int majority_element(const int32_t *a, uint32_t n, int32_t *out)
; Return 1 and a value appearing more than n/2 times, or 0 without writing. A candidate must pass a second counting scan.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT majority_element
majority_element
        cmp r0,#0
        beq mj_bad
        cmp r1,#0
        beq mj_bad
        cmp r2,#0
        beq mj_bad
        push {r4-r8,lr}
        movs r3,#0
        movs r4,#0
        movs r5,#0
mj_loop
        cmp r5,r1
        bhs mj_verify
        ldr r6,[r0,r5,lsl #2]
        cmp r3,#0
        beq mj_choose
        cmp r4,r6
        beq mj_inc
        subs r3,#1
        b mj_next
mj_choose
        mov r4,r6
mj_inc
        adds r3,#1
mj_next
        adds r5,#1
        b mj_loop
mj_verify
        movs r5,#0
        movs r7,#0
mj_count
        cmp r5,r1
        bhs mj_check
        ldr r6,[r0,r5,lsl #2]
        cmp r6,r4
        bne mj_cn
        adds r7,#1
mj_cn
        adds r5,#1
        b mj_count
mj_check
        lsrs r1,#1
        cmp r7,r1
        bls mj_fail
        str r4,[r2]
        movs r0,#1
        pop {r4-r8,pc}
mj_fail
        movs r0,#0
        pop {r4-r8,pc}
mj_bad
        movs r0,#0
        bx lr

        ALIGN
        END
