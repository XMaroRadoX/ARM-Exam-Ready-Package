; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; uint32_t algorithm_seven_argument_component_merge(uint32_t *labels, uint32_t n,
;                                           uint32_t from, uint32_t to,
;                                           uint32_t limit)
; Fifth argument is [SP]. Leaf; saves R4-R7 (16-byte frame).
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  algorithm_seven_argument_component_merge

algorithm_seven_argument_component_merge PROC
                LDR     R12, [SP]
                CMP     R0, #0
                BEQ     merge_invalid
                CMP     R1, R12
                BHI     merge_invalid
                PUSH    {R4-R7}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOV     R7, R3
                MOVS    R0, #0
                MOVS    R1, #0
merge_scan
                CMP     R1, R5
                BHS     merge_done
                LDR     R2, [R4, R1, LSL #2]
                CMP     R2, R6
                BNE     merge_next
                STR     R7, [R4, R1, LSL #2]
                ADDS    R0, R0, #1
merge_next
                ADDS    R1, R1, #1
                B       merge_scan
merge_done
                POP     {R4-R7}
                BX      LR
merge_invalid
                MOVS    R0, #0
                BX      LR
                ENDP

                LTORG
                ALIGN   2
                END
