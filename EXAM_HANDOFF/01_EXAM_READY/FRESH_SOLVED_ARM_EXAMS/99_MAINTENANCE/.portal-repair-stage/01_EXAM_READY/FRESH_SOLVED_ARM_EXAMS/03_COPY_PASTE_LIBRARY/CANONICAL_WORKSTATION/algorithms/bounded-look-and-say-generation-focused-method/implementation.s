; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; uint32_t algorithm_bounded_look_and_say_generation_focused_method(const uint8_t *input, uint32_t n,
;                                       uint8_t *output, uint32_t capacity)
; R0-R3 are the four arguments. Leaf; saves R4-R7 (16-byte frame).
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  algorithm_bounded_look_and_say_generation_focused_method

algorithm_bounded_look_and_say_generation_focused_method PROC
                CMP     R0, #0
                BEQ     look_invalid
                CMP     R2, #0
                BEQ     look_invalid
                PUSH    {R4-R7}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOV     R7, R3
                MOVS    R0, #0          ; output index
                MOVS    R1, #0          ; input index
look_outer
                CMP     R1, R5
                BHS     look_done
                LDRB    R2, [R4, R1]
                MOVS    R3, #1
                ADDS    R1, R1, #1
look_count
                CMP     R1, R5
                BHS     look_emit
                CMP     R3, #255
                BHI     look_fail
                LDRB    R12, [R4, R1]
                CMP     R12, R2
                BNE     look_emit
                ADDS    R3, R3, #1
                ADDS    R1, R1, #1
                B       look_count
look_emit
                SUB     R12, R7, R0
                CMP     R12, #2
                BLO     look_fail
                ADD     R12, R6, R0
                STRB    R3, [R12]
                STRB    R2, [R12, #1]
                ADDS    R0, R0, #2
                B       look_outer
look_done
                POP     {R4-R7}
                BX      LR
look_fail
                POP     {R4-R7}
look_invalid
                MOVS    R0, #0
                BX      LR
                ENDP

                LTORG
                ALIGN   2
                END
