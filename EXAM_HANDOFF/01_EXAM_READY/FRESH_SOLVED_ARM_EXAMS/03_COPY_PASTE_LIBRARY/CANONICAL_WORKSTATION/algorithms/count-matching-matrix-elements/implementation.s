; Count matching matrix elements
; uint32_t matrix_count_matches_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int32_t target)
; Count cells equal to target in a matrix with dimensions at most 256. A zero dimension returns zero and permits a null matrix pointer. Other invalid input returns zero.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_count_matches_i32
matrix_count_matches_i32
        ; R0=matrix,R1=rows,R2=columns,R3=target. R4 is match count.
        cmp r1,#256
        bhi mcm_zero
        cmp r2,#256
        bhi mcm_zero
        mul r1,r1,r2
        cmp r1,#0
        beq mcm_zero
        cmp r0,#0
        beq mcm_zero
        push {r4,r5}
        movs r4,#0
mcm_loop
        ldr r5,[r0],#4
        cmp r5,r3
        bne mcm_next
        adds r4,#1
mcm_next
        subs r1,#1
        bne mcm_loop
        mov r0,r4
        pop {r4,r5}
        bx lr
mcm_zero
        movs r0,#0
        bx lr

        ALIGN
        END
