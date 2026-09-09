; Test whether an integer is a power of two
; int is_power_of_two_u32(uint32_t value)
; Return 1 only for positive unsigned values containing exactly one set bit. Zero is not a power of two.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT is_power_of_two_u32
is_power_of_two_u32
        ; R0=value. R1 receives value-1.
        cmp r0,#0
        beq ipt_no
        sub r1,r0,#1
        tst r0,r1
        bne ipt_no
        movs r0,#1
        bx lr
ipt_no
        movs r0,#0
        bx lr

        ALIGN
        END
