; Upper bound and equal range
; size_t upper_bound_i32(const int *a, size_t n, int key)
; Ascending signed input; return the first index with value>key, or n. Null returns zero. This entry supplies upper bound; combine with the existing lower-bound routine for an equal range.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT upper_bound_i32
upper_bound_i32
        cmp r0,#0
        beq ub_zero
        push {r4,r5}
        movs r3,#0
ub_loop
        cmp r3,r1
        bhs ub_done
        sub r12,r1,r3
        lsr r12,r12,#1
        add r12,r3
        ldr r4,[r0,r12,lsl #2]
        cmp r4,r2
        bgt ub_left
        add r3,r12,#1
        b ub_loop
ub_left
        mov r1,r12
        b ub_loop
ub_done
        mov r0,r3
        pop {r4,r5}
        bx lr
ub_zero
        movs r0,#0
        bx lr

        ALIGN
        END
