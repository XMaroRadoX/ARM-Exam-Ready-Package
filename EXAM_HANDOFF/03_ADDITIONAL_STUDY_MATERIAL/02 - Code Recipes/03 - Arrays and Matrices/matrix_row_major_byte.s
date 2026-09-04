; Recommended exam template: read matrix[row][column] from a byte matrix.
; C prototype: uint8_t matrix_get_u8(const uint8_t *base,
;                                   uint32_t row, uint32_t columns,
;                                   uint32_t column);
; Offset = row * columns + column. No bounds check in this low-level pattern.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  matrix_get_u8

matrix_get_u8   PROC
                MUL     R1, R1, R2
                ADDS    R1, R1, R3
                LDRB    R0, [R0, R1]
                BX      LR
                ENDP

                END
