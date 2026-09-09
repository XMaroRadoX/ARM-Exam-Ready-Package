; Scale an integer between ranges
; int scale_i32_between_ranges(int32_t value, int32_t input_min,
;                              int32_t input_max, int32_t output_min,
;                              int32_t output_max, int32_t *result_out)
; Clamp value to input_min..input_max, then linearly map it to output_min..output_max. Input span must be positive and fit int32_t; output span must fit int32_t. Use a signed 64-bit product and truncate division toward zero. Invalid input writes nothing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT scale_i32_between_ranges
scale_i32_between_ranges
        ; R0=value,R1=input_min,R2=input_max,R3=output_min. output_max and result_out are on entry stack.
        ldr r12,[sp,#4]
        cmp r12,#0
        beq sir_bad
        push {r4-r10,lr}
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        ldr r8,[sp,#32]
        ldr r9,[sp,#36]
        subs r10,r6,r5
        bvs sir_fail
        cmp r10,#0
        ble sir_fail
        subs r6,r8,r7
        bvs sir_fail
        cmp r4,r5
        bge sir_high
        mov r4,r5
sir_high
        cmp r4,r2
        ble sir_product
        mov r4,r2
sir_product
        sub r4,r4,r5
        smull r0,r1,r4,r6
        mov r2,r10
        movs r3,#0
        bl __aeabi_ldivmod
        adds r0,r0,r7
        bvs sir_fail
        str r0,[r9]
        movs r0,#1
        pop {r4-r10,pc}
sir_fail
        movs r0,#0
        pop {r4-r10,pc}
sir_bad
        movs r0,#0
        bx lr
        IMPORT __aeabi_ldivmod
        ALIGN
        END
