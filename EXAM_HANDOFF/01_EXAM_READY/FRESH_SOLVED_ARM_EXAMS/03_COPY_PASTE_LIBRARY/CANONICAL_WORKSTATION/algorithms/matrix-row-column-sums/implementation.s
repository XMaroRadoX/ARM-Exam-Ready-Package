; Matrix row and column sums
; int matrix_sums(const int16_t *a, uint32_t rows, uint32_t cols, int64_t *out, uint32_t capacity)
; For a row-major signed-halfword matrix, write rows row sums followed by cols column sums. Require dimensions 1..256, capacity>=rows+cols and disjoint output; return 0 before writes on invalid input, otherwise 1.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_sums
matrix_sums
        cmp r0,#0
        beq mx_bad
        cmp r3,#0
        beq mx_bad
        cmp r1,#1
        blo mx_bad
        cmp r2,#1
        blo mx_bad
        cmp r1,#256
        bhi mx_bad
        cmp r2,#256
        bhi mx_bad
        ldr r12,[sp]
        push {r4-r11,lr}
        sub sp,sp,#4
        add r4,r1,r2
        cmp r12,r4
        blo mx_fail
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        movs r8,#0
mx_row
        cmp r8,r5
        bhs mx_columns
        movs r9,#0
        movs r10,#0
mx_ri
        cmp r9,r6
        bhs mx_rs
        mla r11,r8,r6,r9
        lsl r11,r11,#1
        ldrsh r0,[r4,r11]
        add r10,r0
        adds r9,#1
        b mx_ri
mx_rs
        str r10,[r7],#4
        asr r0,r10,#31
        str r0,[r7],#4
        adds r8,#1
        b mx_row
mx_columns
        movs r8,#0
mx_col
        cmp r8,r6
        bhs mx_done
        movs r9,#0
        movs r10,#0
mx_ci
        cmp r9,r5
        bhs mx_cs
        mla r11,r9,r6,r8
        lsl r11,r11,#1
        ldrsh r0,[r4,r11]
        add r10,r0
        adds r9,#1
        b mx_ci
mx_cs
        str r10,[r7],#4
        asr r0,r10,#31
        str r0,[r7],#4
        adds r8,#1
        b mx_col
mx_done
        movs r0,#1
        b mx_return
mx_fail
        movs r0,#0
mx_return
        add sp,sp,#4
        pop {r4-r11,pc}
mx_bad
        movs r0,#0
        bx lr

        ALIGN
        END
