; Classify an integer as even or odd
; uint32_t integer_is_odd(int32_t value)
; Return 0 for even and 1 for odd. Testing the low bit works for positive, zero, and negative two-complement values.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT integer_is_odd
integer_is_odd
        ; R0=value. Bit zero is the complete result.
        and r0,r0,#1
        bx lr

        ALIGN
        END
