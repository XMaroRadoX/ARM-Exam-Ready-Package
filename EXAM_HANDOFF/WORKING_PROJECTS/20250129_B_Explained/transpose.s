                AREA    TRANSPOSE_CODE, CODE, READONLY
                THUMB
                PRESERVE8
                EXPORT  transpose

; void transpose(const uint8_t *A, uint8_t *AT)
; R0 = address of A; R1 = address of AT. Buffers must not overlap.
transpose       PROC
                PUSH    {R4-R8, LR}      ; 6 registers = 24 bytes
                MOVS    R2, #0
                MOVS    R3, #0
clear_loop
                STRB    R3, [R1, R2]    ; AT[index] = 0
                ADDS    R2, R2, #1
                CMP     R2, #8
                BLO     clear_loop

                MOVS    R2, #0          ; i = source row
row_loop
                LDRB    R4, [R0, R2]    ; x = A[i]
                MOVS    R3, #0          ; j = source column
bit_loop
                MOVS    R5, #0x80
                LSR     R5, R5, R3      ; source mask = 0x80 >> j
                TST     R4, R5
                BEQ     next_bit        ; zero bit: destination stays zero
                MOVS    R6, #0x80
                LSR     R6, R6, R2      ; destination mask = 0x80 >> i
                LDRB    R7, [R1, R3]    ; read AT[j]
                ORR     R7, R7, R6      ; set its column i
                STRB    R7, [R1, R3]
next_bit
                ADDS    R3, R3, #1
                CMP     R3, #8
                BLO     bit_loop
                ADDS    R2, R2, #1
                CMP     R2, #8
                BLO     row_loop
                POP     {R4-R8, PC}
                ENDP

; Question 1 example data. The routine also accepts the C arrays in Q2.
                AREA    MATRIX_INPUT, DATA, READONLY
                EXPORT  matrix
matrix          DCB     0xF8, 0x7C, 0x3E, 0x1F, 0x8F, 0xC7, 0xE3, 0xF1

                AREA    MATRIX_OUTPUT, DATA, READWRITE
                EXPORT  matrix_T
matrix_T        SPACE   8
                END
