; Test whether a matrix is lower triangular
; int matrix_is_lower_triangular_i32(const int32_t *matrix, uint32_t size)
; Return 1 when every cell on the forbidden side of the main diagonal is zero. size must be at most 256. The empty matrix passes; null nonempty input fails.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_is_lower_triangular_i32
matrix_is_lower_triangular_i32
        ; R0=matrix,R1=size. R2=row,R3=column.
        cmp r1,#256
        bhi mtt_no
        cmp r1,#0
        beq mtt_yes
        cmp r0,#0
        beq mtt_no
        push {r4,r5}
        movs r2,#0
mtt_row
        cmp r2,r1
        bhs mtt_done
        movs r3,#0
mtt_column
        cmp r3,r1
        bhs mtt_next_row
        cmp r3,r2
        bls mtt_next
        mla r4,r2,r1,r3
        ldr r5,[r0,r4,lsl #2]
        cmp r5,#0
        bne mtt_fail
mtt_next
        adds r3,#1
        b mtt_column
mtt_next_row
        adds r2,#1
        b mtt_row
mtt_done
        pop {r4,r5}
mtt_yes
        movs r0,#1
        bx lr
mtt_fail
        pop {r4,r5}
mtt_no
        movs r0,#0
        bx lr

        ALIGN
        END
