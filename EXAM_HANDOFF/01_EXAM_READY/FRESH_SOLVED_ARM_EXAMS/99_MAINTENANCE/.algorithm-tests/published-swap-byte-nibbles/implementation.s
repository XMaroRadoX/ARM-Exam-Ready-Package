; Swap the two nibbles of a byte
; uint8_t swap_byte_nibbles(uint8_t value)
; Exchange bits 7..4 with bits 3..0 and return the low eight-bit result.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT swap_byte_nibbles
swap_byte_nibbles
        ; R0=value. UXTB keeps only the byte before and after the swap.
        uxtb r0,r0
        lsl r1,r0,#4
        lsr r0,r0,#4
        orr r0,r0,r1
        uxtb r0,r0
        bx lr

        ALIGN
        END
