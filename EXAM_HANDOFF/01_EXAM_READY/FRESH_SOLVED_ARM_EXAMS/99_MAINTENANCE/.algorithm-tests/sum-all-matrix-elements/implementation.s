; Sum all matrix elements
; int matrix_total_sum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int64_t *sum_out)
; Sum a contiguous row-major int32_t matrix into int64_t. rows and columns must each be at most 256. A zero dimension produces zero and permits a null matrix pointer. Invalid input returns 0 without writing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_total_sum_i32
matrix_total_sum_i32
        ; R0=matrix,R1=rows,R2=columns,R3=sum_out. R4:R5 is the 64-bit sum.
        cmp r3,#0
        beq mts_bad
        cmp r1,#256
        bhi mts_bad
        cmp r2,#256
        bhi mts_bad
        mul r1,r1,r2
        cmp r1,#0
        beq mts_empty
        cmp r0,#0
        beq mts_bad
        push {r4-r7,lr}
        movs r4,#0
        movs r5,#0
mts_loop
        ldr r6,[r0],#4
        asr r7,r6,#31
        adds r4,r4,r6
        adc r5,r5,r7
        subs r1,#1
        bne mts_loop
        str r4,[r3]
        str r5,[r3,#4]
        movs r0,#1
        pop {r4-r7,pc}
mts_empty
        movs r1,#0
        str r1,[r3]
        str r1,[r3,#4]
        movs r0,#1
        bx lr
mts_bad
        movs r0,#0
        bx lr

        ALIGN
        END
