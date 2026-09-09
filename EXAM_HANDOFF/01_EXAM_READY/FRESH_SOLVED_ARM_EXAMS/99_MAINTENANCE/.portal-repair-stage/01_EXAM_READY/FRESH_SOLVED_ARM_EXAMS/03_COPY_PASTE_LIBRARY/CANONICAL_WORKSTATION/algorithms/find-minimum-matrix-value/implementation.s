; Find the minimum matrix value
; int matrix_minimum_i32(const int32_t *matrix, uint32_t rows, uint32_t columns, int32_t *value_out)
; Return the signed matrix extremum. Require dimensions 1..256 and valid pointers. Invalid or empty input returns 0 without writing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_minimum_i32
matrix_minimum_i32
        ; R0=matrix,R1=rows,R2=columns,R3=value_out.
        cmp r0,#0
        beq mex_bad
        cmp r3,#0
        beq mex_bad
        cmp r1,#1
        blo mex_bad
        cmp r2,#1
        blo mex_bad
        cmp r1,#256
        bhi mex_bad
        cmp r2,#256
        bhi mex_bad
        mul r1,r1,r2
        push {r4,lr}
        ldr r2,[r0],#4
        subs r1,#1
mex_loop
        cmp r1,#0
        beq mex_done
        ldr r4,[r0],#4
        cmp r4,r2
        bge mex_next
        mov r2,r4
mex_next
        subs r1,#1
        b mex_loop
mex_done
        str r2,[r3]
        movs r0,#1
        pop {r4,pc}
mex_bad
        movs r0,#0
        bx lr

        ALIGN
        END
