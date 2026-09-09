; Calculate a matrix border sum
; int matrix_border_sum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int64_t *sum_out)
; Sum cells in the first or last row or column exactly once. Dimensions must be at most 256. A zero dimension returns zero and permits a null matrix.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_border_sum_i32
matrix_border_sum_i32
        ; R0=matrix,R1=rows,R2=columns,R3=sum_out. Visit row-major and test border coordinates.
        cmp r3,#0
        beq mbs_bad
        cmp r1,#256
        bhi mbs_bad
        cmp r2,#256
        bhi mbs_bad
        cmp r1,#0
        beq mbs_empty
        cmp r2,#0
        beq mbs_empty
        cmp r0,#0
        beq mbs_bad
        push {r4-r10,lr}
        mov r4,r1
        mov r5,r2
        movs r6,#0
        movs r7,#0
        movs r8,#0
mbs_row
        cmp r8,r4
        bhs mbs_done
        movs r9,#0
mbs_column
        cmp r9,r5
        bhs mbs_next_row
        cmp r8,#0
        beq mbs_add
        add r10,r8,#1
        cmp r10,r4
        beq mbs_add
        cmp r9,#0
        beq mbs_add
        add r10,r9,#1
        cmp r10,r5
        bne mbs_next
mbs_add
        mla r10,r8,r5,r9
        ldr r1,[r0,r10,lsl #2]
        asr r2,r1,#31
        adds r6,r6,r1
        adc r7,r7,r2
mbs_next
        adds r9,#1
        b mbs_column
mbs_next_row
        adds r8,#1
        b mbs_row
mbs_done
        str r6,[r3]
        str r7,[r3,#4]
        movs r0,#1
        pop {r4-r10,pc}
mbs_empty
        movs r1,#0
        str r1,[r3]
        str r1,[r3,#4]
        movs r0,#1
        bx lr
mbs_bad
        movs r0,#0
        bx lr

        ALIGN
        END
