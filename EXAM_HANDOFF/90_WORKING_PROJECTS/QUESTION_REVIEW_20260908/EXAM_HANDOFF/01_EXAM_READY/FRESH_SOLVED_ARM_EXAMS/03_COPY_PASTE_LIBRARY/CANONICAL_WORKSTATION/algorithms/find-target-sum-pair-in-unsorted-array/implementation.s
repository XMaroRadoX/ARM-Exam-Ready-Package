; Find a target-sum pair in a unsorted array
; int array_pair_sum_unsorted(const int32_t *values, uint32_t count, int32_t target,
;                     uint32_t *first_out, uint32_t *second_out)
; Find two distinct indexes whose exact 64-bit sum equals target. Output pointers must be valid and distinct; failure writes nothing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_pair_sum_unsorted
array_pair_sum_unsorted
        ; R0=values, R1=count, R2=target, R3=first_out; second_out is at entry SP.
        ldr r12,[sp]
        cmp r0,#0
        beq aps_bad
        cmp r3,#0
        beq aps_bad
        cmp r12,#0
        beq aps_bad
        cmp r3,r12
        beq aps_bad
        cmp r1,#2
        blo aps_bad
        push {r4-r10,lr}
        mov r4,r12
        movs r5,#0
aps_outer
        cmp r5,r1
        bhs aps_fail
        add r6,r5,#1
aps_loop
        cmp r6,r1
        bhs aps_next_first
        ldr r7,[r0,r5,lsl #2]
        ldr r8,[r0,r6,lsl #2]
        asr r9,r7,#31
        asr r10,r8,#31
        adds r7,r7,r8
        adc r9,r9,r10
        asr r8,r2,#31
        cmp r9,r8
        bne aps_next_second
        cmp r7,r2
        beq aps_found
aps_next_second
        adds r6,#1
        b aps_loop
aps_next_first
        adds r5,#1
        b aps_outer
aps_found
        str r5,[r3]
        str r6,[r4]
        movs r0,#1
        pop {r4-r10,pc}
aps_fail
        movs r0,#0
        pop {r4-r10,pc}
aps_bad
        movs r0,#0
        bx lr

        ALIGN
        END
