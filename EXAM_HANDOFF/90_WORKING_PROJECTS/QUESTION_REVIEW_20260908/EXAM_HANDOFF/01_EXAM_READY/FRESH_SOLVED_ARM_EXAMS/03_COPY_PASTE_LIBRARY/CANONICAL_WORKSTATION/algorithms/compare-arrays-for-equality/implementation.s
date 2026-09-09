; Compare two arrays for equality
; int arrays_equal(const int32_t *left, const int32_t *right, uint32_t count)
; Return 1 when all count signed words are equal. Empty arrays are equal even with null pointers. A null pointer with a nonzero count returns 0.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT arrays_equal
arrays_equal
        ; R0=left, R1=right, R2=count.
        cmp r2,#0
        beq aeq_yes
        cmp r0,#0
        beq aeq_no
        cmp r1,#0
        beq aeq_no
aeq_loop
        ldr r3,[r0],#4
        ldr r12,[r1],#4
        cmp r3,r12
        bne aeq_no
        subs r2,#1
        bne aeq_loop
aeq_yes
        movs r0,#1
        bx lr
aeq_no
        movs r0,#0
        bx lr

        ALIGN
        END
