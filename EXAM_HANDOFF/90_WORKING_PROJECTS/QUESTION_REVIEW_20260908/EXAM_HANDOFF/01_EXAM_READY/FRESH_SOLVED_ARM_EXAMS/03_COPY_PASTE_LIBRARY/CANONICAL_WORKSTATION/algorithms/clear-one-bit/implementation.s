; Clear one bit
; int clear_bit_u32(uint32_t value, uint32_t index, uint32_t *result_out)
; Accept bit indexes 0..31. Return 1 and the requested result, or return 0 without writing for an invalid index or null output.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT clear_bit_u32
clear_bit_u32
        ; R0=value,R1=index,R2=result_out. Invalid input performs no store.
        cmp r1,#32
        bhs beo_bad
        cmp r2,#0
        beq beo_bad
        movs r3,#1
        lsl r3,r3,r1
        bic r0,r0,r3
        str r0,[r2]
        movs r0,#1
        bx lr
beo_bad
        movs r0,#0
        bx lr

        ALIGN
        END
