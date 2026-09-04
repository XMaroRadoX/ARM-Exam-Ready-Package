; Decimal digit product
; uint32_t decimal_digit_product(uint32_t n)
; Unsigned decimal input. Zero has one digit; return the count or product named by the routine.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT decimal_digit_product
decimal_digit_product
        movs r1,#1
        movs r2,#10
dd_loop
        udiv r12,r0,r2
        mls r3,r12,r2,r0
        mul r1,r3,r1
        mov r0,r12
        cmp r0,#0
        bne dd_loop
        mov r0,r1
        bx lr

        ALIGN
        END
