; Pack four bytes into a 32-bit word
; uint32_t pack_four_bytes_be(uint8_t first, uint8_t second,
;                             uint8_t third, uint8_t fourth)
; Pack first into bits 31..24, second into 23..16, third into 15..8, and fourth into 7..0. The name describes this logical big-endian display order; no memory access occurs.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT pack_four_bytes_be
pack_four_bytes_be
        ; R0-R3 contain the four bytes. Mask before shifting and combining.
        uxtb r0,r0
        uxtb r1,r1
        uxtb r2,r2
        uxtb r3,r3
        lsl r0,r0,#24
        orr r0,r0,r1,lsl #16
        orr r0,r0,r2,lsl #8
        orr r0,r0,r3
        bx lr

        ALIGN
        END
