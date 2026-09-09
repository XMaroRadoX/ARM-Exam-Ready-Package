; Find the minimum value in a selected row
; int matrix_row_minimum_i32(const int32_t *matrix, uint32_t rows,
;                        uint32_t columns, uint32_t row_index,
;                        int32_t *value_out)
; Return the signed minimum in one row. Require dimensions 1..256, a valid selected index, and valid pointers. Invalid input writes nothing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_row_minimum_i32
matrix_row_minimum_i32
        ; R0=matrix,R1=rows,R2=columns,R3=selected index; value_out is at entry SP.
        ldr r12,[sp]
        cmp r0,#0
        beq mse_bad
        cmp r12,#0
        beq mse_bad
        cmp r1,#1
        blo mse_bad
        cmp r2,#1
        blo mse_bad
        cmp r1,#256
        bhi mse_bad
        cmp r2,#256
        bhi mse_bad
        cmp r3,r1
        bhs mse_bad
        push {r4-r6,lr}
        mov r4,r3
        mul r1,r4,r2
        add r0,r0,r1,lsl #2
        mov r1,r2
        ldr r3,[r0]
        subs r1,#1
mse_loop
        cmp r1,#0
        beq mse_done
        add r0,r0,#4
        ldr r5,[r0]
        cmp r5,r3
        bge mse_next
        mov r3,r5
mse_next
        subs r1,#1
        b mse_loop
mse_done
        str r3,[r12]
        movs r0,#1
        pop {r4-r6,pc}
mse_bad
        movs r0,#0
        bx lr

        ALIGN
        END
