; Inputs: R0=word-array base, R1=count. Output: R0=sum.
; Caller-saved registers only; no stack required.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  asm_sum_words

asm_sum_words   PROC
                MOV     R2, R0
                MOVS    R0, #0
                MOVS    R3, #0
sum_loop        CMP     R3, R1
                BHS     sum_done
                LDR     R12, [R2, R3, LSL #2]
                ADDS    R0, R0, R12
                ADDS    R3, R3, #1
                B       sum_loop
sum_done        BX      LR
                ENDP

                END
