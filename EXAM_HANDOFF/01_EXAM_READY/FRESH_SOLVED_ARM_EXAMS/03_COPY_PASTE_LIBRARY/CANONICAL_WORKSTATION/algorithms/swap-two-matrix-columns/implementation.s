; Swap two matrix columns
; int matrix_swap_columns_i32(int32_t *matrix, uint32_t rows, uint32_t columns,
;                       uint32_t first, uint32_t second)
; Swap two complete columns. Require dimensions 1..256 and both indexes below columns. Equal indexes are a successful no-op. Invalid input writes nothing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_swap_columns_i32
matrix_swap_columns_i32
        ; R0=matrix,R1=rows,R2=columns,R3=first; second is at entry SP.
        ldr r12,[sp]
        cmp r0,#0
        beq msa_bad
        cmp r1,#1
        blo msa_bad
        cmp r2,#1
        blo msa_bad
        cmp r1,#256
        bhi msa_bad
        cmp r2,#256
        bhi msa_bad
        cmp r3,r2
        bhs msa_bad
        cmp r12,r2
        bhs msa_bad
        push {r4-r10,lr}
        mov r4,r12
        movs r5,#0
msa_loop
        cmp r5,r1
        bhs msa_done
        mla r6,r5,r2,r3
        mla r7,r5,r2,r4
        ldr r8,[r0,r6,lsl #2]
        ldr r9,[r0,r7,lsl #2]
        str r9,[r0,r6,lsl #2]
        str r8,[r0,r7,lsl #2]
        adds r5,#1
        b msa_loop
msa_done
        movs r0,#1
        pop {r4-r10,pc}
msa_bad
        movs r0,#0
        bx lr

        ALIGN
        END
