                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  digitSum
                EXPORT  digitaddition
digitSum        PROC
                MOVS    R1, #0
                MOVS    R2, #10
ds_loop         CMP     R0, #0
                BEQ     ds_done
                UDIV    R3, R0, R2
                MLS     R12, R3, R2, R0
                ADD     R1, R1, R12
                MOV     R0, R3
                B       ds_loop
ds_done         MOV     R0, R1
                BX      LR
                ENDP
digitaddition   PROC
                PUSH    {R4-R8, LR}
                CMP     R1, #0
                BEQ     da_fail
                MOV     R4, R0
                MOV     R5, R1
                LDR     R6, [R4]
                MOVS    R7, #0
da_loop         MOV     R0, R6
                BL      digitSum
                ADD     R7, R7, R0
                SUBS    R5, R5, #1
                BEQ     da_done
                ADDS    R6, R6, R0
                BCS     da_fail
                ADD     R4, R4, #4
                STR     R6, [R4]
                B       da_loop
da_done         MOV     R0, R7
                POP     {R4-R8, PC}
da_fail         MOVS    R0, #0
                POP     {R4-R8, PC}
                ENDP
                END
