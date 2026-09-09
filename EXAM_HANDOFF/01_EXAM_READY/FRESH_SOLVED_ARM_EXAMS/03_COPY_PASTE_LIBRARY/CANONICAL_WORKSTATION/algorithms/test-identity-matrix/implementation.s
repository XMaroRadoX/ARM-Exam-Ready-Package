; Test whether a matrix is an identity matrix
; int matrix_is_identity_i32(const int32_t *matrix, uint32_t size)
; Return 1 when diagonal cells are one and every other cell is zero. size must be at most 256. The empty 0x0 matrix is accepted; a null nonempty matrix is invalid and returns 0.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_is_identity_i32
matrix_is_identity_i32
        ; R0=matrix,R1=size. R2=row,R3=column,R4=expected value.
        cmp r1,#256
        bhi mid_no
        cmp r1,#0
        beq mid_yes
        cmp r0,#0
        beq mid_no
        push {r4-r6,lr}
        movs r2,#0
mid_row
        cmp r2,r1
        bhs mid_done
        movs r3,#0
mid_column
        cmp r3,r1
        bhs mid_next_row
        movs r4,#0
        cmp r2,r3
        bne mid_load
        movs r4,#1
mid_load
        mla r5,r2,r1,r3
        ldr r6,[r0,r5,lsl #2]
        cmp r6,r4
        bne mid_fail
        adds r3,#1
        b mid_column
mid_next_row
        adds r2,#1
        b mid_row
mid_done
        pop {r4-r6,lr}
mid_yes
        movs r0,#1
        bx lr
mid_fail
        pop {r4-r6,lr}
mid_no
        movs r0,#0
        bx lr

        ALIGN
        END
