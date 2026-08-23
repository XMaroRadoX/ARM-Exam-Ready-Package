                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  Maclaurin

; int32_t Maclaurin(int32_t y, uint32_t order)
Maclaurin       PROC
                PUSH    {R4-R9, LR}
                SUB     SP, SP, #4      ; Keep the public stack 8-byte aligned.
                MOV     R4, R0          ; y.
                MOV     R5, R1          ; Maximum order.
                MOVS    R6, #10
                MUL     R6, R6, R4      ; t0 = 10*y.
                MOV     R7, R6          ; Sum.
                MOVS    R8, #1          ; i = 1.

sin_term_loop
                CMP     R8, R5
                BHI     sin_done

                MUL     R0, R4, R4      ; y^2.
                MUL     R0, R6, R0      ; previous term * y^2.
                RSBS    R0, R0, #0      ; Negate numerator.

                LSLS    R1, R8, #1      ; 2*i.
                ADDS    R2, R1, #1      ; 2*i+1.
                MUL     R1, R1, R2
                MOVS    R2, #100
                MUL     R1, R1, R2      ; Denominator.
                SDIV    R6, R0, R1
                ADDS    R7, R7, R6
                ADDS    R8, R8, #1
                B       sin_term_loop

sin_done
                MOV     R0, R7
                ADD     SP, SP, #4
                POP     {R4-R9, PC}
                ENDP

                LTORG
                ALIGN   4
                END
