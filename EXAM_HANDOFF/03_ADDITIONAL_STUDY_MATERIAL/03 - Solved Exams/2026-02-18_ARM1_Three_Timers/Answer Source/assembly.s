                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  HofstadterQ

; uint32_t HofstadterQ(uint32_t *v, int dim)
; R0 = v, R1 = dim, return maximum in R0.
HofstadterQ     PROC
                PUSH    {R4-R10, LR}
                MOV     R4, R0
                MOV     R5, R1

                CMP     R5, #0
                BLE     q_empty

                MOVS    R7, #1
                STR     R7, [R4]
                CMP     R5, #1
                BEQ     q_done

                STR     R7, [R4, #4]
                MOVS    R6, #2

q_loop
                CMP     R6, R5
                BHS     q_done

                SUBS    R10, R6, #1
                LDR     R8, [R4, R10, LSL #2]
                SUBS    R10, R6, #2
                LDR     R9, [R4, R10, LSL #2]

                SUBS    R10, R6, R8
                LDR     R10, [R4, R10, LSL #2]
                SUBS    R8, R6, R9
                LDR     R8, [R4, R8, LSL #2]
                ADDS    R10, R10, R8

                STR     R10, [R4, R6, LSL #2]
                CMP     R10, R7
                BLS     q_keep_maximum
                MOV     R7, R10
q_keep_maximum
                ADDS    R6, R6, #1
                B       q_loop

q_done
                MOV     R0, R7
                POP     {R4-R10, PC}

q_empty
                MOVS    R0, #0
                POP     {R4-R10, PC}
                ENDP

                LTORG
                ALIGN   4
                END
