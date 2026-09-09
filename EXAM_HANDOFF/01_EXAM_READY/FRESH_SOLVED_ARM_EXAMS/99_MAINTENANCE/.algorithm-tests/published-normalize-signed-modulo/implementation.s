; Normalize signed modulo into a nonnegative result
; int normalized_modulo_i32(int32_t value, int32_t modulus, int32_t *result_out)
; Require modulus>0. Return the unique result in 0..modulus-1 that is congruent to value. Invalid input returns 0 without writing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT normalized_modulo_i32
normalized_modulo_i32
        ; R0=value,R1=positive modulus,R2=result_out. R3 is quotient, R12 remainder.
        cmp r2,#0
        beq nmi_bad
        cmp r1,#0
        ble nmi_bad
        sdiv r3,r0,r1
        mls r12,r3,r1,r0
        cmp r12,#0
        bge nmi_store
        add r12,r12,r1
nmi_store
        str r12,[r2]
        movs r0,#1
        bx lr
nmi_bad
        movs r0,#0
        bx lr

        ALIGN
        END
