; Checked array sum
; int checked_array_sum(const int32_t *values, uint32_t count,
;                       int64_t *sum_out)
; Sum signed words into a 64-bit result. count must not exceed INT32_MAX, which guarantees that every possible int32_t input sum fits int64_t. A zero-length array sums to zero and may have a null data pointer. Return 0 without writing for an invalid pointer or count.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT checked_array_sum
checked_array_sum
        ; R0=values, R1=count, R2=sum_out. R3:R4 is the 64-bit sum.
        cmp r2,#0
        beq cas_bad
        cmp r1,#0
        bmi cas_bad
        cmp r1,#0
        beq cas_empty
        cmp r0,#0
        beq cas_bad
        push {r4-r7,lr}
        movs r3,#0
        movs r4,#0
cas_loop
        ldr r5,[r0],#4
        asr r6,r5,#31
        adds r3,r3,r5
        adc r4,r4,r6
        subs r1,#1
        bne cas_loop
        str r3,[r2]
        str r4,[r2,#4]
        movs r0,#1
        pop {r4-r7,pc}
cas_empty
        movs r3,#0
        str r3,[r2]
        str r3,[r2,#4]
        movs r0,#1
        bx lr
cas_bad
        movs r0,#0
        bx lr

        ALIGN
        END
