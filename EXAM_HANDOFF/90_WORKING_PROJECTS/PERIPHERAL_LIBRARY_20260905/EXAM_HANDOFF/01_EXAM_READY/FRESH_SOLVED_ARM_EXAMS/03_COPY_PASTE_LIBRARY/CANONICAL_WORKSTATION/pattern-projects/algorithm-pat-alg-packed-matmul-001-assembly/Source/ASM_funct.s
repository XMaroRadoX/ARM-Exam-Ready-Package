; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; uint64_t algorithm_algorithm_pat_alg_packed_matmul_001_assembly(uint64_t a, uint64_t b)
; R0:R1=a, R2:R3=b, R0:R1=result over GF(2). Leaf; saves R4-R11.
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  algorithm_algorithm_pat_alg_packed_matmul_001_assembly

algorithm_algorithm_pat_alg_packed_matmul_001_assembly PROC
                PUSH    {R4-R11}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOV     R7, R3
                MOVS    R8, #0
                MOVS    R9, #0
                MOVS    R10, #0         ; row
matmul_row
                MOVS    R11, #0         ; column
matmul_column
                MOVS    R0, #0          ; parity accumulator
                MOVS    R12, #0         ; k
matmul_dot
                LSL     R1, R10, #3
                ADD     R1, R1, R12     ; a index = row*8+k
                CMP     R1, #32
                BLO     matmul_a_low
                SUB     R2, R1, #32
                LSR     R2, R5, R2
                B       matmul_a_ready
matmul_a_low
                LSR     R2, R4, R1
matmul_a_ready
                AND     R2, R2, #1

                LSL     R1, R12, #3
                ADD     R1, R1, R11     ; b index = k*8+column
                CMP     R1, #32
                BLO     matmul_b_low
                SUB     R3, R1, #32
                LSR     R3, R7, R3
                B       matmul_b_ready
matmul_b_low
                LSR     R3, R6, R1
matmul_b_ready
                AND     R3, R3, #1
                AND     R2, R2, R3
                EOR     R0, R0, R2
                ADD     R12, R12, #1
                CMP     R12, #8
                BNE     matmul_dot

                CMP     R0, #0
                BEQ     matmul_next_column
                LSL     R1, R10, #3
                ADD     R1, R1, R11
                MOVS    R2, #1
                CMP     R1, #32
                BLO     matmul_set_low
                SUB     R1, R1, #32
                LSL     R2, R2, R1
                ORR     R9, R9, R2
                B       matmul_next_column
matmul_set_low
                LSL     R2, R2, R1
                ORR     R8, R8, R2
matmul_next_column
                ADD     R11, R11, #1
                CMP     R11, #8
                BNE     matmul_column
                ADD     R10, R10, #1
                CMP     R10, #8
                BNE     matmul_row
                MOV     R0, R8
                MOV     R1, R9
                POP     {R4-R11}
                BX      LR
                ENDP

                LTORG
                ALIGN   2
                END
