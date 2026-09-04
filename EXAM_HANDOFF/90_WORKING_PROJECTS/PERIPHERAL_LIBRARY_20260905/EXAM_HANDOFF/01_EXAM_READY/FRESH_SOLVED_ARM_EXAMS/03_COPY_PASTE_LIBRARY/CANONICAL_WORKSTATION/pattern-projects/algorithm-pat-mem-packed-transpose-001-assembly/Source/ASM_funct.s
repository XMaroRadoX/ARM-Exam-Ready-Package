; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; uint64_t algorithm_algorithm_pat_mem_packed_transpose_001_assembly(uint64_t packed)
; R0:R1=input, R0:R1=output. Leaf. R4-R9 saved (24-byte frame).
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  algorithm_algorithm_pat_mem_packed_transpose_001_assembly

algorithm_algorithm_pat_mem_packed_transpose_001_assembly PROC
                PUSH    {R4-R9}
                MOV     R4, R0
                MOV     R5, R1
                MOVS    R6, #0
                MOVS    R7, #0
                MOVS    R8, #0          ; source bit index 0..63
transpose_loop
                CMP     R8, #32
                BLO     transpose_source_low
                SUB     R1, R8, #32
                LSR     R2, R5, R1
                B       transpose_have_bit
transpose_source_low
                LSR     R2, R4, R8
transpose_have_bit
                TST     R2, #1
                BEQ     transpose_next
                AND     R0, R8, #7      ; source column
                LSR     R1, R8, #3      ; source row
                LSL     R0, R0, #3
                ADD     R9, R0, R1      ; destination = column*8 + row
                MOVS    R2, #1
                CMP     R9, #32
                BLO     transpose_set_low
                SUB     R9, R9, #32
                LSL     R2, R2, R9
                ORR     R7, R7, R2
                B       transpose_next
transpose_set_low
                LSL     R2, R2, R9
                ORR     R6, R6, R2
transpose_next
                ADDS    R8, R8, #1
                CMP     R8, #64
                BNE     transpose_loop
                MOV     R0, R6
                MOV     R1, R7
                POP     {R4-R9}
                BX      LR
                ENDP

                LTORG
                ALIGN   2
                END
