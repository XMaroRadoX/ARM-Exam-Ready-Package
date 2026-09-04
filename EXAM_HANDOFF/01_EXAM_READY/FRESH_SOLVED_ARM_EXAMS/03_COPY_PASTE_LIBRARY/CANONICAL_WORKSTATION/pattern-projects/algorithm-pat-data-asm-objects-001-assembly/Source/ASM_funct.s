; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; uint32_t algorithm_algorithm_pat_data_asm_objects_001_assembly(const uint32_t *values, uint32_t count)
; R0=values, R1=count, R0=sum. Leaf; no stack frame.
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  algorithm_algorithm_pat_data_asm_objects_001_assembly

algorithm_algorithm_pat_data_asm_objects_001_assembly PROC
                MOVS    R2, #0
                CMP     R1, #0
                BEQ     data_sum_done
                CMP     R0, #0
                BEQ     data_sum_done
data_sum_loop
                LDR     R3, [R0], #4
                ADD     R2, R2, R3
                SUBS    R1, R1, #1
                BNE     data_sum_loop
data_sum_done
                MOV     R0, R2
                BX      LR
                ENDP

PATTERN_OBJECT_COUNT EQU 4

                AREA    |.data.patterns|, DATA, READWRITE
                ALIGN   2
                EXPORT  pattern_initialized_words
        EXPORT  algorithm_algorithm_pat_data_asm_objects_001_assembly_initialized_words
algorithm_algorithm_pat_data_asm_objects_001_assembly_initialized_words
pattern_initialized_words DCD 1, 2, 3, 4
                EXPORT  pattern_workspace
        EXPORT  algorithm_algorithm_pat_data_asm_objects_001_assembly_workspace
algorithm_algorithm_pat_data_asm_objects_001_assembly_workspace
pattern_workspace SPACE 32

                AREA    |.constdata.patterns|, DATA, READONLY
                ALIGN   2
                EXPORT  pattern_masks
        EXPORT  algorithm_algorithm_pat_data_asm_objects_001_assembly_magic
algorithm_algorithm_pat_data_asm_objects_001_assembly_magic DCD 0x13579BDF
        EXPORT  algorithm_algorithm_pat_data_asm_objects_001_assembly_masks
algorithm_algorithm_pat_data_asm_objects_001_assembly_masks
pattern_masks   DCD     1, 2, 4, 8

                LTORG
                ALIGN   2
                END
