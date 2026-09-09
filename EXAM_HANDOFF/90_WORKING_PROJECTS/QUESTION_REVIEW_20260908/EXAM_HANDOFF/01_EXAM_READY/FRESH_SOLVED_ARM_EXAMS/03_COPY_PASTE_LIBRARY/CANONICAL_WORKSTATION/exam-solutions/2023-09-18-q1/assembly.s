                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  digitSum
                EXPORT  digitaddition

; uint32_t digitSum(uint32_t a)
digitSum        PROC
                MOVS    R1, #0
                MOVS    R2, #10
ds_loop         CMP     R0, #0
                BEQ     ds_done
                UDIV    R3, R0, R2
                MLS     R12, R3, R2, R0
                ADD     R1, R1, R12
                MOV     R0, R3
                B       ds_loop
ds_done         MOV     R0, R1
                BX      LR
                ENDP

; uint32_t digitaddition(uint32_t *area, uint32_t count)
digitaddition   PROC
                PUSH    {R4-R8, LR}     ; 24-byte aligned non-leaf frame
                CMP     R1, #0
                BEQ     da_zero
                MOV     R4, R0
                MOV     R5, R1
                LDR     R6, [R4]        ; current term
                MOV     R0, R6
                BL      digitSum
                MOV     R7, R0          ; sum of all digits
                MOVS    R8, #1
da_loop         CMP     R8, R5
                BHS     da_done
                MOV     R0, R6
                BL      digitSum
                ADDS    R6, R6, R0
                BCS     da_zero
                STR     R6, [R4, R8, LSL #2]
                MOV     R0, R6
                BL      digitSum       ; count the NEW term, not its predecessor
                ADD     R7, R7, R0
                ADDS    R8, R8, #1
                B       da_loop
da_done         MOV     R0, R7
                POP     {R4-R8, PC}
da_zero         MOVS    R0, #0
                POP     {R4-R8, PC}
                ENDP

                AREA    DIGIT_SERIES, DATA, READWRITE, NOINIT
review_series   SPACE   200             ; 50 words, as requested
                AREA    |.text|, CODE, READONLY
                EXPORT  Reset_Handler
Reset_Handler   PROC
                LDR     R0, =review_series
                MOVS    R2, #47
                STR     R2, [R0]
                MOVS    R1, #50
                BL      digitaddition
review_finished B       review_finished
                ENDP
                LTORG
                END

