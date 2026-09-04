.syntax unified
.cpu cortex-m3
.thumb
.text
.global pat_alg_run_length_001
pat_alg_run_length_001:
                LDR     R12, [SP]
                CMP     R0, #0
                BEQ     rle_invalid
                CMP     R2, #0
                BEQ     rle_invalid
                CMP     R3, #0
                BEQ     rle_invalid
                PUSH    {R4-R11}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOV     R7, R3
                MOV     R8, R12
                MOVS    R9, #0
                MOVS    R10, #0
rle_outer:
                CMP     R9, R5
                BHS     rle_done
                LDRB    R11, [R4, R9]
                MOVS    R3, #1
                ADDS    R9, R9, #1
rle_count:
                CMP     R9, R5
                BHS     rle_emit
                CMP     R3, #255
                BEQ     rle_emit
                LDRB    R0, [R4, R9]
                CMP     R0, R11
                BNE     rle_emit
                ADDS    R3, R3, #1
                ADDS    R9, R9, #1
                B       rle_count
rle_emit:
                CMP     R10, R8
                BHS     rle_capacity_fail
                STRB    R11, [R6, R10]
                STRB    R3, [R7, R10]
                ADDS    R10, R10, #1
                B       rle_outer
rle_done:
                MOV     R0, R10
                POP     {R4-R11}
                BX      LR
rle_capacity_fail:
                POP     {R4-R11}
rle_invalid:
                MOVS    R0, #0
                BX      LR
.ltorg
.balign 4
