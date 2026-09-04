; Reverse all 32 bits
; uint32_t reverse_bits(uint32_t value)
; Reverse all 32 positions, including leading zeros.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT reverse_bits
reverse_bits
        movs r1,#0
        movs r2,#32
rb_loop
        lsrs r0,#1
        adc r1,r1,r1
        subs r2,#1
        bne rb_loop
        mov r0,r1
        bx lr

        ALIGN
        END
