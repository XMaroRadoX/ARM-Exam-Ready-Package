.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_restoring_division_quotient_and_remainder
algorithm_restoring_division_quotient_and_remainder:
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
wide_div_start:
                PUSH    {R4-R11}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOVS    R7, #0
                MOVS    R8, #0
                MOVS    R9, #0
                MOVS    R10, #64
                MOVS    R11, #0
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
wide_div_dividend_positive:
                CMP     R6, #0
                BPL     wide_div_divisor_positive
                EOR     R11, R11, #1
                RSB     R6, R6, #0
wide_div_divisor_positive:
wide_div_loop:
                LSLS    R4, R4, #1
                ADCS    R5, R5, R5
                ADCS    R7, R7, R7
                LSLS    R8, R8, #1
                ADC     R9, R9, R9
                CMP     R7, R6
                BLO     wide_div_no_subtract
                SUB     R7, R7, R6
                ORR     R8, R8, #1
wide_div_no_subtract:
                SUBS    R10, R10, #1
                BNE     wide_div_loop
                TST     R11, #1
                BEQ     wide_div_quotient_ready
                MVN     R8, R8
                MVN     R9, R9
                ADDS    R8, R8, #1
                MOVS    R3, #0
                ADC     R9, R9, R3
wide_div_quotient_ready:
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
.ltorg
.balign 4
