; Recommended exam template: get one bit from an 8x8 packed bit matrix.
; C prototype: uint32_t packed_get(const uint8_t rows[8],
;                                 uint32_t row, uint32_t column);
; Bit 7 is column 0 and bit 0 is column 7. Returns 0 or 1.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  packed_get

packed_get      PROC
                LDRB    R3, [R0, R1]
                MOVS    R0, #0x80
                LSRS    R0, R0, R2
                TST     R3, R0
                ITE     NE
                MOVNE   R0, #1
                MOVEQ   R0, #0
                BX      LR
                ENDP

                END
