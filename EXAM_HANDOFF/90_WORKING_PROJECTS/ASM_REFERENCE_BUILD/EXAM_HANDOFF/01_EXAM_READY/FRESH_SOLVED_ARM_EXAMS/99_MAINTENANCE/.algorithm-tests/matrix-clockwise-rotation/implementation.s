; Clockwise square-matrix rotation
; int matrix_rotate_clockwise(const int32_t *a, uint32_t n, int32_t *out, uint32_t capacity)
; Rotate a signed-word square matrix 90 degrees clockwise into separate storage. Require n<=256 and capacity>=n*n. Empty matrix succeeds; exact aliasing is rejected, other overlap is prohibited.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_rotate_clockwise
matrix_rotate_clockwise
        cmp r1,#256
        bhi rt_bad
        mul r12,r1,r1
        cmp r3,r12
        blo rt_bad
        cmp r1,#0
        beq rt_yes
        cmp r0,#0
        beq rt_bad
        cmp r2,#0
        beq rt_bad
        cmp r0,r2
        beq rt_bad
        push {r4-r8,lr}
        movs r3,#0
rt_outer
        cmp r3,r1
        bhs rt_done
        movs r4,#0
rt_inner
        cmp r4,r1
        bhs rt_next
        mla r5,r3,r1,r4
        mul r6,r4,r1
        add r6,r1
        subs r6,#1
        sub r6,r3
        ldr r7,[r0,r5,lsl #2]
        str r7,[r2,r6,lsl #2]
        adds r4,#1
        b rt_inner
rt_next
        adds r3,#1
        b rt_outer
rt_done
        pop {r4-r8,lr}
rt_yes
        movs r0,#1
        bx lr
rt_bad
        movs r0,#0
        bx lr

        ALIGN
        END
