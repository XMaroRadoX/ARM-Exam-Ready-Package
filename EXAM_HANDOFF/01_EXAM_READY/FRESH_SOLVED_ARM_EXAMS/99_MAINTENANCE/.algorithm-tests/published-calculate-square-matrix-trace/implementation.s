; Calculate a square matrix trace
; int matrix_trace_i32(const int32_t *matrix, uint32_t size, int64_t *trace_out)
; Sum the main diagonal of a contiguous square int32_t matrix. size must be at most 256. A 0x0 matrix has trace zero and may be null.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_trace_i32
matrix_trace_i32
        ; R0=matrix,R1=size,R2=trace_out. R3 is the diagonal index.
        cmp r2,#0
        beq mtr_bad
        cmp r1,#256
        bhi mtr_bad
        cmp r1,#0
        beq mtr_empty
        cmp r0,#0
        beq mtr_bad
        push {r4-r7,lr}
        movs r3,#0
        movs r4,#0
        movs r5,#0
        add r7,r1,#1
mtr_loop
        ldr r6,[r0,r3,lsl #2]
        asr r12,r6,#31
        adds r4,r4,r6
        adc r5,r5,r12
        add r3,r3,r7
        subs r1,#1
        bne mtr_loop
        str r4,[r2]
        str r5,[r2,#4]
        movs r0,#1
        pop {r4-r7,pc}
mtr_empty
        movs r3,#0
        str r3,[r2]
        str r3,[r2,#4]
        movs r0,#1
        bx lr
mtr_bad
        movs r0,#0
        bx lr

        ALIGN
        END
