; Add signed integers with overflow detection
; int checked_add_i32(int32_t left, int32_t right, int32_t *result_out)
; Return 1 and the exact signed 32-bit result. Return 0 without writing when result_out is null or the mathematical result is outside INT32_MIN..INT32_MAX.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT checked_add_i32
checked_add_i32
        ; R0=left,R1=right,R2=result_out. Store only after overflow is ruled out.
        cmp r2,#0
        beq cbo_bad
        adds r3,r0,r1
        bvs cbo_bad
        str r3,[r2]
        movs r0,#1
        bx lr
cbo_bad
        movs r0,#0
        bx lr

        ALIGN
        END
