; Unpack a 32-bit word into four bytes
; int unpack_four_bytes_be(uint32_t value, uint8_t *output, uint32_t capacity)
; Write bits 31..24, 23..16, 15..8, and 7..0 into output[0..3]. Require capacity>=4 and a valid output; failure writes nothing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT unpack_four_bytes_be
unpack_four_bytes_be
        ; R0=value,R1=output,R2=capacity. Validate before four STRB operations.
        cmp r1,#0
        beq ufb_bad
        cmp r2,#4
        blo ufb_bad
        lsr r3,r0,#24
        strb r3,[r1]
        lsr r3,r0,#16
        strb r3,[r1,#1]
        lsr r3,r0,#8
        strb r3,[r1,#2]
        strb r0,[r1,#3]
        movs r0,#1
        bx lr
ufb_bad
        movs r0,#0
        bx lr

        ALIGN
        END
