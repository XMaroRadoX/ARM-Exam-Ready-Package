; Lexicographically compare two signed arrays
; int32_t arrays_compare_lexicographic(const int32_t *left, uint32_t left_count,
;                                      const int32_t *right, uint32_t right_count)
; Return -1, 0, or 1 using signed element order, then shorter-prefix order. A null pointer is valid only with a zero count; invalid input returns 2.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT arrays_compare_lexicographic
arrays_compare_lexicographic
        ; R0=left, R1=left_count, R2=right, R3=right_count.
        cmp r1,#0
        beq alc_right
        cmp r0,#0
        beq alc_bad
alc_right
        cmp r3,#0
        beq alc_start
        cmp r2,#0
        beq alc_bad
alc_start
        push {r4-r6,lr}
        cmp r1,r3
        bls alc_left_short
        mov r4,r3
        b alc_loop
alc_left_short
        mov r4,r1
alc_loop
        cmp r4,#0
        beq alc_lengths
        ldr r5,[r0],#4
        ldr r6,[r2],#4
        cmp r5,r6
        blt alc_less
        bgt alc_more
        subs r4,#1
        b alc_loop
alc_lengths
        cmp r1,r3
        blt alc_less
        bgt alc_more
        movs r0,#0
        pop {r4-r6,pc}
alc_less
        mvn r0,#0
        pop {r4-r6,pc}
alc_more
        movs r0,#1
        pop {r4-r6,pc}
alc_bad
        movs r0,#2
        bx lr

        ALIGN
        END
