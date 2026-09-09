                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  isSociable

; uint32_t isSociable(uint32_t number)
isSociable      PROC
                PUSH    {R4-R6, LR}
                MOV     R4, R0          ; Original number.
                MOV     R5, R0          ; Current sequence value.
                MOVS    R6, #0          ; Number of computed terms.

sociable_loop
                MOV     R0, R5
                BL      aliquotSum
                ADDS    R6, R6, #1

                CMP     R0, R4
                BEQ     sociable_found
                CMP     R0, #1
                BEQ     sociable_not_found
                CMP     R6, #8
                BEQ     sociable_not_found

                MOV     R5, R0
                B       sociable_loop

sociable_found
                MOV     R0, R6
                POP     {R4-R6, PC}

sociable_not_found
                MOVS    R0, #0
                POP     {R4-R6, PC}
                ENDP

; R0 = n. Return the aliquot sum in R0.
aliquotSum      PROC
                CMP     R0, #1
                BHI     aliquot_nontrivial
                MOVS    R0, #0
                BX      LR
aliquot_nontrivial
                MOVS    R1, #1          ; sum = 1.
                MOVS    R2, #2          ; a = 2.

divisor_loop
                UDIV    R3, R0, R2      ; b = n / a.
                MLS     R12, R3, R2, R0 ; remainder = n - b*a.
                CMP     R12, #0
                BNE     next_divisor

                CMP     R2, R3
                BLO     add_divisor_pair
                BEQ     add_square_root

                MOV     R0, R1
                BX      LR

add_divisor_pair
                ADDS    R1, R1, R2
                ADDS    R1, R1, R3
                B       next_divisor

add_square_root
                ADDS    R1, R1, R2
                MOV     R0, R1
                BX      LR

next_divisor
                ADDS    R2, R2, #1
                B       divisor_loop
                ENDP

                LTORG
                ALIGN   4
                END
