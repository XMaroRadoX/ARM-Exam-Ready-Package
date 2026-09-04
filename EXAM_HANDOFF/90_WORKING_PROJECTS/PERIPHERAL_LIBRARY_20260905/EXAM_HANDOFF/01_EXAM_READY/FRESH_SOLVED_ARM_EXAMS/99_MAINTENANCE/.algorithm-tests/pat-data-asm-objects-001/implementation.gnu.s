.syntax unified
.cpu cortex-m3
.thumb
.text
.global pat_data_asm_objects_001
pat_data_asm_objects_001:
                MOVS    R2, #0
                CMP     R1, #0
                BEQ     data_sum_done
                CMP     R0, #0
                BEQ     data_sum_done
data_sum_loop:
                LDR     R3, [R0], #4
                ADD     R2, R2, R3
                SUBS    R1, R1, #1
                BNE     data_sum_loop
data_sum_done:
                MOV     R0, R2
                BX      LR
.equ PATTERN_OBJECT_COUNT,4
.section .data
.balign 4
.global pattern_initialized_words
.global pat_data_asm_objects_001_initialized_words
pat_data_asm_objects_001_initialized_words:
pattern_initialized_words:
.word 1, 2, 3, 4
.global pattern_workspace
.global pat_data_asm_objects_001_workspace
pat_data_asm_objects_001_workspace:
pattern_workspace:
.space 32
.section .rodata
.balign 4
.global pattern_masks
.global pat_data_asm_objects_001_magic
pat_data_asm_objects_001_magic:
.word 0x13579BDF
.global pat_data_asm_objects_001_masks
pat_data_asm_objects_001_masks:
pattern_masks:
.word 1, 2, 4, 8
.ltorg
.balign 4
