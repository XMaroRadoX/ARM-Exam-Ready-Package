; Array length: fixed count or bounded sentinel
; int bounded_word_length(const uint32_t *a, uint32_t capacity, uint32_t sentinel, uint32_t *length)
; For a fixed C array, use sizeof array / sizeof array[0] at the caller. A pointer has no length. This routine handles only an explicit sentinel-terminated word array: return 1 and the number of words before the first sentinel within capacity, or return 0 without writing when no sentinel is found or a required pointer is null.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT bounded_word_length
bounded_word_length
        cmp r0,#0
        beq al_bad
        cmp r3,#0
        beq al_bad
        push {r4,lr}
        movs r4,#0
al_loop
        cmp r4,r1
        bhs al_missing
        ldr r12,[r0,r4,lsl #2]
        cmp r12,r2
        beq al_found
        adds r4,#1
        b al_loop
al_found
        str r4,[r3]
        movs r0,#1
        pop {r4,pc}
al_missing
        movs r0,#0
        pop {r4,pc}
al_bad
        movs r0,#0
        bx lr

        ALIGN
        END
