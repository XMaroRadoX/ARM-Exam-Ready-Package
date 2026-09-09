; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; int64_t algorithm_restoring_division_quotient_and_remainder(int64_t dividend, int32_t divisor,
;                                          int32_t *remainder)
; R0:R1=dividend low:high, R2=divisor, R3=remainder pointer.
; R0:R1=quotient low:high. Leaf. Saves R4-R11 (32-byte aligned frame).
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  algorithm_restoring_division_quotient_and_remainder

algorithm_restoring_division_quotient_and_remainder PROC
                CMP     R2, #0
                BNE     wide_div_start
                CMP     R3, #0
                IT      NE
                MOVNE   R12, #0
                IT      NE
                STRNE   R12, [R3]
                MOVS    R0, #0
                MOVS    R1, #0
                BX      LR

wide_div_start
                PUSH    {R4-R11}
                MOV     R4, R0          ; absolute dividend low
                MOV     R5, R1          ; absolute dividend high
                MOV     R6, R2          ; absolute divisor
                MOVS    R7, #0          ; restoring remainder
                MOVS    R8, #0          ; quotient low
                MOVS    R9, #0          ; quotient high
                MOVS    R10, #64        ; fixed loop count
                MOVS    R11, #0         ; bit0=negative quotient, bit1=negative remainder
                SUB     SP, SP, #8
                STR     R3, [SP]

                CMP     R5, #0
                BPL     wide_div_dividend_positive
                ORR     R11, R11, #3
                MVN     R4, R4
                MVN     R5, R5
                ADDS    R4, R4, #1
                MOVS    R3, #0
                ADC     R5, R5, R3
wide_div_dividend_positive
                CMP     R6, #0
                BPL     wide_div_divisor_positive
                EOR     R11, R11, #1
                RSB     R6, R6, #0
wide_div_divisor_positive

wide_div_loop
                LSLS    R4, R4, #1      ; shift dividend, next input bit exits R5
                ADCS    R5, R5, R5
                ADCS    R7, R7, R7      ; remainder = remainder*2 + next bit
                LSLS    R8, R8, #1
                ADC     R9, R9, R9      ; shift 64-bit quotient
                CMP     R7, R6
                BLO     wide_div_no_subtract
                SUB     R7, R7, R6
                ORR     R8, R8, #1
wide_div_no_subtract
                SUBS    R10, R10, #1
                BNE     wide_div_loop

                TST     R11, #1
                BEQ     wide_div_quotient_ready
                MVN     R8, R8
                MVN     R9, R9
                ADDS    R8, R8, #1
                MOVS    R3, #0
                ADC     R9, R9, R3
wide_div_quotient_ready
                TST     R11, #2
                IT      NE
                RSBNE   R7, R7, #0
                LDR     R3, [SP]
                CMP     R3, #0
                IT      NE
                STRNE   R7, [R3]
                MOV     R0, R8
                MOV     R1, R9
                ADD     SP, SP, #8
                POP     {R4-R11}
                BX      LR
                ENDP

                LTORG
                ALIGN   2
                END
