                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  SDIV64
                EXPORT  SDIV64S

; int32_t SDIV64(int32_t upper, uint32_t lower, int32_t divisor)
SDIV64          PROC
                PUSH    {R4-R8, LR}
                EOR     R4, R0, R2      ; sign of quotient
                CMP     R0, #0
                BGE     div_abs_d
                MVN     R1, R1
                MVN     R0, R0
                ADDS    R1, R1, #1
                MOVS    R8, #0
                ADCS    R0, R0, R8
div_abs_d       CMP     R2, #0
                IT      LT
                RSBLT   R2, R2, #0
                MOVS    R3, #0          ; quotient
                MOVS    R5, #32
div_loop        LSLS    R1, R1, #1
                ADC     R0, R0, R0      ; shift U:L left as one 64-bit value
                LSLS    R3, R3, #1
                CMP     R0, R2
                BLO     div_next
                SUB     R0, R0, R2
                ORR     R3, R3, #1
div_next        SUBS    R5, R5, #1
                BNE     div_loop
                CMP     R4, #0
                IT      MI
                RSBMI   R3, R3, #0
                MOV     R0, R3
                POP     {R4-R8, PC}
                ENDP

; Same quotient, with N/Z from the result, C=0 and V from the paper's test.
SDIV64S         PROC
                PUSH    {R4-R8, LR}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                CMP     R4, #0
                BGE     divs_abs_d
                RSB     R4, R4, #0      ; paper test uses absolute upper word
divs_abs_d      CMP     R6, #0
                IT      LT
                RSBLT   R6, R6, #0
                LSRS    R6, R6, #1
                CMP     R6, R4
                ITE     HI
                MOVHI   R7, #0
                MOVLS   R7, #1          ; overflow flag
                BL      SDIV64
                MRS     R4, APSR
                BIC     R4, R4, #0xF0000000
                CMP     R0, #0
                IT      MI
                ORRMI   R4, R4, #0x80000000
                IT      EQ
                ORREQ   R4, R4, #0x40000000
                CMP     R7, #0
                IT      NE
                ORRNE   R4, R4, #0x10000000
                MSR     APSR_nzcvq, R4
                POP     {R4-R8, PC}
                ENDP
                END
