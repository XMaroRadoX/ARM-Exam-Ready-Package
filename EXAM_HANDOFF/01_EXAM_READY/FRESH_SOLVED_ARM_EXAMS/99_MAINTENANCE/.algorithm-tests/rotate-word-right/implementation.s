; Rotate a 32-bit word right
; uint32_t rotate_right_u32(uint32_t value, uint32_t amount)
; Normalize amount modulo 32 and rotate without losing bits. A zero or multiple-of-32 amount returns the original word.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT rotate_right_u32
rotate_right_u32
        ; R0=value,R1=amount. Register-controlled ROR uses the low five count bits.
        and r1,r1,#31
        ror r0,r0,r1
        bx lr

        ALIGN
        END
