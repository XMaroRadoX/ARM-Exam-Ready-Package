; Rare template: unsigned 64-bit addition.
; Inputs a=R0(low):R1(high), b=R2(low):R3(high).
; Output R0(low):R1(high). ADDS feeds carry to ADC.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  add_u64_words

add_u64_words   PROC
                ADDS    R0, R0, R2
                ADC     R1, R1, R3
                BX      LR
                ENDP

                END
