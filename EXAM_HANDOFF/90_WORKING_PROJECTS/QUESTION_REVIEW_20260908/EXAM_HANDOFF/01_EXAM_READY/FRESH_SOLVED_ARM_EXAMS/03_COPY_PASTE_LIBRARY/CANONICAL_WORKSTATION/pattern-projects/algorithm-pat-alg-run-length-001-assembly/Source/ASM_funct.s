; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; uint32_t algorithm_algorithm_pat_alg_run_length_001_assembly(const uint8_t *input, uint32_t n,
;                                      uint8_t *values, uint8_t *runs,
;                                      uint32_t capacity)
; Fifth argument is [SP]. Leaf; saves R4-R11 (32-byte frame).
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  algorithm_algorithm_pat_alg_run_length_001_assembly

algorithm_algorithm_pat_alg_run_length_001_assembly PROC
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
                MOVS    R9, #0          ; input index
                MOVS    R10, #0         ; output index
rle_outer
                CMP     R9, R5
                BHS     rle_done
                LDRB    R11, [R4, R9]
                MOVS    R3, #1
                ADDS    R9, R9, #1
rle_count
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
rle_emit
                CMP     R10, R8
                BHS     rle_capacity_fail
                STRB    R11, [R6, R10]
                STRB    R3, [R7, R10]
                ADDS    R10, R10, #1
                B       rle_outer
rle_done
                MOV     R0, R10
                POP     {R4-R11}
                BX      LR
rle_capacity_fail
                POP     {R4-R11}
rle_invalid
                MOVS    R0, #0
                BX      LR
                ENDP

                LTORG
                ALIGN   2
                END
