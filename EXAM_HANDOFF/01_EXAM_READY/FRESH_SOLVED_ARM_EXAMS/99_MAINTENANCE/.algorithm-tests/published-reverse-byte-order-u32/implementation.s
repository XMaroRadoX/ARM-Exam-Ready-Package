; Reverse the byte order of a 32-bit word
; uint32_t reverse_byte_order_u32(uint32_t value)
; Return the same four bytes in reverse order. This changes logical byte positions and does not access memory.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT reverse_byte_order_u32
reverse_byte_order_u32
        ; Cortex-M3 REV reverses all four byte lanes in R0.
        rev r0,r0
        bx lr

        ALIGN
        END
