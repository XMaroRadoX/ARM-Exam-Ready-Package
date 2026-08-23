; ARMv7-M Thumb assembly, Keil syntax.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

; uint32_t exam_asm_solution(uint32_t value)
; R0 contains the first argument and the 32-bit return value.
                EXPORT  exam_asm_solution
exam_asm_solution PROC
                BX      LR
                ENDP

                LTORG
                ALIGN   4
                END
