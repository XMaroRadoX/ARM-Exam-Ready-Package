                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  bitMatrixMultiplication

; void bitMatrixMultiplication(const uint8_t *A, const uint8_t *B, uint8_t *C)
bitMatrixMultiplication PROC
                PUSH    {R4-R11, R12, LR}
                MOV     R4, R0          ; A.
                MOV     R5, R1          ; B.
                MOV     R6, R2          ; C.
                MOVS    R7, #0          ; Row i.

matrix_row
                CMP     R7, #8
                BHS     matrix_done
                LDRB    R8, [R4, R7]
                MOVS    R9, #0          ; Result row.
                MOVS    R10, #0         ; Column j.

matrix_column
                CMP     R10, #8
                BHS     matrix_store_row
                MOVS    R12, #0         ; XOR sum for c(i,j).
                MOVS    R11, #0         ; k.

matrix_product
                CMP     R11, #8
                BHS     matrix_store_bit

                MOVS    R0, #0x80
                LSR     R0, R0, R11
                TST     R8, R0
                BEQ     matrix_next_k

                LDRB    R1, [R5, R11]
                MOVS    R2, #0x80
                LSR     R2, R2, R10
                TST     R1, R2
                BEQ     matrix_next_k

                MOVS    R0, #1
                EORS    R12, R12, R0

matrix_next_k
                ADDS    R11, R11, #1
                B       matrix_product

matrix_store_bit
                CMP     R12, #0
                BEQ     matrix_next_column
                MOVS    R0, #0x80
                LSR     R0, R0, R10
                ORRS    R9, R9, R0

matrix_next_column
                ADDS    R10, R10, #1
                B       matrix_column

matrix_store_row
                STRB    R9, [R6, R7]
                ADDS    R7, R7, #1
                B       matrix_row

matrix_done
                MOV     R0, R6
                POP     {R4-R11, R12, PC}
                ENDP

                LTORG
                ALIGN   4
                END
