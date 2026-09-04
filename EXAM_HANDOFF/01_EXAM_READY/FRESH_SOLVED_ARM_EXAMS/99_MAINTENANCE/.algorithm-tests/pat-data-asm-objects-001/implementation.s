; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; uint32_t pat_data_asm_objects_001(const uint32_t *values, uint32_t count)
; R0=values, R1=count, R0=sum. Leaf; no stack frame.
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  pat_data_asm_objects_001

pat_data_asm_objects_001 PROC
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
        EXPORT  pat_data_asm_objects_001_initialized_words
pat_data_asm_objects_001_initialized_words
pattern_initialized_words DCD 1, 2, 3, 4
                EXPORT  pattern_workspace
        EXPORT  pat_data_asm_objects_001_workspace
pat_data_asm_objects_001_workspace
pattern_workspace SPACE 32

                AREA    |.constdata.patterns|, DATA, READONLY
                ALIGN   2
                EXPORT  pattern_masks
        EXPORT  pat_data_asm_objects_001_magic
pat_data_asm_objects_001_magic DCD 0x13579BDF
        EXPORT  pat_data_asm_objects_001_masks
pat_data_asm_objects_001_masks
pattern_masks   DCD     1, 2, 4, 8

                LTORG
                ALIGN   2
                END
