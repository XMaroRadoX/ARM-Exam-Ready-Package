.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_consume_once_duplicate_safe_matching
algorithm_consume_once_duplicate_safe_matching:
                CMP     R0, #0
                BEQ     match_invalid
                CMP     R1, #0
                BEQ     match_invalid
                CMP     R3, #0
                BEQ     match_invalid
                CMP     R2, #32
                BHI     match_invalid
                PUSH    {R4-R11}
                SUB     SP, SP, #64
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOV     R7, R3
                MOVS    R8, #0
                MOVS    R9, #0
                MOVS    R10, #0
match_clear:
                CMP     R10, R6
                BHS     match_exact_start
                MOVS    R0, #0
                STRB    R0, [SP, R10]
                ADD     R1, SP, #32
                STRB    R0, [R1, R10]
                ADDS    R10, R10, #1
                B       match_clear
match_exact_start:
                MOVS    R10, #0
match_exact:
                CMP     R10, R6
                BHS     match_cows_start
                LDRB    R0, [R4, R10]
                LDRB    R1, [R5, R10]
                CMP     R0, R1
                BNE     match_exact_next
                MOVS    R0, #1
                STRB    R0, [SP, R10]
                ADD     R1, SP, #32
                STRB    R0, [R1, R10]
                ADDS    R8, R8, #1
match_exact_next:
                ADDS    R10, R10, #1
                B       match_exact
match_cows_start:
                MOVS    R10, #0
match_guess:
                CMP     R10, R6
                BHS     match_done
                ADD     R0, SP, #32
                LDRB    R1, [R0, R10]
                CMP     R1, #0
                BNE     match_next_guess
                MOVS    R11, #0
match_secret:
                CMP     R11, R6
                BHS     match_next_guess
                LDRB    R1, [SP, R11]
                CMP     R1, #0
                BNE     match_next_secret
                LDRB    R1, [R5, R10]
                LDRB    R2, [R4, R11]
                CMP     R1, R2
                BNE     match_next_secret
                MOVS    R1, #1
                STRB    R1, [SP, R11]
                STRB    R1, [R0, R10]
                ADDS    R9, R9, #1
                B       match_next_guess
match_next_secret:
                ADDS    R11, R11, #1
                B       match_secret
match_next_guess:
                ADDS    R10, R10, #1
                B       match_guess
match_done:
                STR     R9, [R7]
                MOV     R0, R8
                ADD     SP, SP, #64
                POP     {R4-R11}
                BX      LR
match_invalid:
                CMP     R3, #0
                IT      NE
                MOVNE   R0, #0
                IT      NE
                STRNE   R0, [R3]
                MOVS    R0, #0
                BX      LR
.ltorg
.balign 4
