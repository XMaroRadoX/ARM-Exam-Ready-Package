                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  copyData
                EXPORT  insertionSortUnsigned

; void copyData(const int8_t *source, int8_t *destination, uint32_t length)
copyData        PROC
                CMP     R2, #0
                BEQ     copy_done
copy_loop
                LDRB    R3, [R0], #1
                STRB    R3, [R1], #1
                SUBS    R2, R2, #1
                BNE     copy_loop
copy_done
                BX      LR
                ENDP

; void insertionSortUnsigned(int8_t *values, uint32_t length)
; Signed byte loads make negative values sort correctly.
insertionSortUnsigned   PROC
                PUSH    {R4-R8, LR}
                MOV     R4, R0          ; Base address.
                MOV     R5, R1          ; Array length.
                CMP     R5, #1
                BLS     sort_done

                MOVS    R6, #1          ; i = 1.
sort_outer
                CMP     R6, R5
                BHS     sort_done

                LDRB   R7, [R4, R6]    ; x = A[i].
                SUBS    R8, R6, #1      ; j = i - 1.

sort_inner
                CMP     R8, #0
                BLT     sort_insert
                LDRB   R0, [R4, R8]
                CMP     R0, R7
                BLS     sort_insert

                ADDS    R1, R8, #1
                STRB    R0, [R4, R1]
                SUBS    R8, R8, #1
                B       sort_inner

sort_insert
                ADDS    R8, R8, #1
                STRB    R7, [R4, R8]
                ADDS    R6, R6, #1
                B       sort_outer

sort_done
                POP     {R4-R8, PC}
                ENDP

                LTORG
                ALIGN   4
                END
