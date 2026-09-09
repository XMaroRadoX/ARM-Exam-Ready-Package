; Checked array product
; int checked_array_product(const int32_t *values, uint32_t count, int32_t *product_out)
; Multiply signed words into an int32_t result. The empty product is one. Return 0 without writing if an input is invalid or any multiplication leaves the signed 32-bit range.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT checked_array_product
checked_array_product
        ; R0=values, R1=count, R2=product_out. R3 holds the tentative product.
        cmp r2,#0
        beq cap_bad
        cmp r1,#0
        beq cap_empty
        cmp r0,#0
        beq cap_bad
        push {r4-r7,lr}
        movs r3,#1
cap_loop
        ldr r4,[r0],#4
        smull r5,r6,r3,r4
        asr r7,r5,#31
        cmp r6,r7
        bne cap_fail
        mov r3,r5
        subs r1,#1
        bne cap_loop
        str r3,[r2]
        movs r0,#1
        pop {r4-r7,pc}
cap_fail
        movs r0,#0
        pop {r4-r7,pc}
cap_empty
        movs r3,#1
        str r3,[r2]
        movs r0,#1
        bx lr
cap_bad
        movs r0,#0
        bx lr

        ALIGN
        END
