; Find the first matching matrix coordinate
; int matrix_find_first_i32(const int32_t *matrix, uint32_t rows,
;                           uint32_t columns, int32_t target,
;                           uint32_t *row_out, uint32_t *column_out)
; Find the first row-major cell equal to target. Require dimensions 1..256 and distinct valid output pointers. Failure or invalid input leaves both outputs unchanged.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_find_first_i32
matrix_find_first_i32
        ; R0=matrix,R1=rows,R2=columns,R3=target. row_out and column_out are on entry stack.
        ldr r12,[sp]
        cmp r12,#0
        beq mff_bad
        push {r4-r8,lr}
        ldr r4,[sp,#28]
        cmp r0,#0
        beq mff_fail
        cmp r4,#0
        beq mff_fail
        cmp r12,r4
        beq mff_fail
        cmp r1,#1
        blo mff_fail
        cmp r2,#1
        blo mff_fail
        cmp r1,#256
        bhi mff_fail
        cmp r2,#256
        bhi mff_fail
        mul r5,r1,r2
        movs r6,#0
mff_loop
        cmp r6,r5
        bhs mff_fail
        ldr r7,[r0,r6,lsl #2]
        cmp r7,r3
        beq mff_found
        adds r6,#1
        b mff_loop
mff_found
        udiv r7,r6,r2
        mls r8,r7,r2,r6
        str r7,[r12]
        str r8,[r4]
        movs r0,#1
        pop {r4-r8,pc}
mff_fail
        movs r0,#0
        pop {r4-r8,pc}
mff_bad
        movs r0,#0
        bx lr

        ALIGN
        END
