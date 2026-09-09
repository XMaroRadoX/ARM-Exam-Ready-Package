; Multiply a matrix by a scalar with overflow detection
; int matrix_scalar_multiply_i32(const int32_t *matrix, uint32_t rows,
;                                uint32_t columns, int32_t scalar,
;                                int32_t *output, uint32_t capacity)
; Multiply every cell by scalar in signed int32_t. Require dimensions at most 256, enough disjoint output, and no overflow. A full preflight prevents partial writes.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_scalar_multiply_i32
matrix_scalar_multiply_i32
        ; R0=matrix,R1=rows,R2=columns,R3=scalar. output and capacity are on entry stack.
        ldr r12,[sp]
        push {r4-r9,lr}
        sub sp,sp,#4
        ldr r4,[sp,#36]
        cmp r1,#256
        bhi msm_fail
        cmp r2,#256
        bhi msm_fail
        mul r5,r1,r2
        cmp r4,r5
        blo msm_fail
        cmp r5,#0
        beq msm_yes
        cmp r0,#0
        beq msm_fail
        cmp r12,#0
        beq msm_fail
        movs r6,#0
msm_check
        cmp r6,r5
        bhs msm_write_start
        ldr r7,[r0,r6,lsl #2]
        smull r8,r9,r7,r3
        asr r7,r8,#31
        cmp r9,r7
        bne msm_fail
        adds r6,#1
        b msm_check
msm_write_start
        movs r6,#0
msm_write
        cmp r6,r5
        bhs msm_yes
        ldr r7,[r0,r6,lsl #2]
        mul r7,r3,r7
        str r7,[r12,r6,lsl #2]
        adds r6,#1
        b msm_write
msm_yes
        movs r0,#1
        b msm_return
msm_fail
        movs r0,#0
msm_return
        add sp,sp,#4
        pop {r4-r9,pc}

        ALIGN
        END
