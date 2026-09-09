; Bounded run-length decoding
; uint32_t rle_decode(const uint8_t *pairs, uint32_t pair_count, uint8_t *out, uint32_t capacity)
; Input consists of pair_count (count,value) byte pairs; zero count is invalid. Preflight total length and capacity before writing. Return decoded length or UINT32_MAX on invalid input; input/output must not overlap.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT rle_decode
rle_decode
        cmp r1,#0
        bmi rl_bad
        cmp r1,#0
        beq rl_zero
        cmp r0,#0
        beq rl_bad
        push {r4-r8,lr}
        movs r4,#0
        movs r5,#0
rl_scan
        cmp r4,r1
        bhs rl_check
        lsl r6,r4,#1
        ldrb r7,[r0,r6]
        cmp r7,#0
        beq rl_fail
        adds r5,r5,r7
        bcs rl_fail
        adds r4,#1
        b rl_scan
rl_check
        cmp r5,r3
        bhi rl_fail
        cmp r2,#0
        beq rl_fail
        movs r4,#0
        movs r5,#0
rl_outer
        cmp r4,r1
        bhs rl_done
        lsl r6,r4,#1
        ldrb r7,[r0,r6]
        adds r6,#1
        ldrb r8,[r0,r6]
rl_inner
        strb r8,[r2,r5]
        adds r5,#1
        subs r7,#1
        bne rl_inner
        adds r4,#1
        b rl_outer
rl_done
        mov r0,r5
        pop {r4-r8,pc}
rl_fail
        pop {r4-r8,lr}
rl_bad
        mvn r0,#0
        bx lr
rl_zero
        movs r0,#0
        bx lr

        ALIGN
        END
