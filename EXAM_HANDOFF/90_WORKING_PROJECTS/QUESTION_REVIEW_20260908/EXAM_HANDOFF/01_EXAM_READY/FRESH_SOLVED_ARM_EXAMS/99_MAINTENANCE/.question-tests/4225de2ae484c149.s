.syntax unified
.cpu cortex-m3
.thumb
.text
.global digitSum
.global digitaddition
digitSum:
                MOVS    R1, #0
                MOVS    R2, #10
ds_loop:
CMP     R0, #0
                BEQ     ds_done
                UDIV    R3, R0, R2
                MLS     R12, R3, R2, R0
                ADD     R1, R1, R12
                MOV     R0, R3
                B       ds_loop
ds_done:
MOV     R0, R1
                BX      LR
digitaddition:
                PUSH    {R4-R8, LR}
                CMP     R1, #0
                BEQ     da_zero
                MOV     R4, R0
                MOV     R5, R1
                LDR     R6, [R4]
                MOV     R0, R6
                BL      digitSum
                MOV     R7, R0
                MOVS    R8, #1
da_loop:
CMP     R8, R5
                BHS     da_done
                MOV     R0, R6
                BL      digitSum
                ADDS    R6, R6, R0
                BCS     da_zero
                STR     R6, [R4, R8, LSL #2]
                MOV     R0, R6
                BL      digitSum
                ADD     R7, R7, R0
                ADDS    R8, R8, #1
                B       da_loop
da_done:
MOV     R0, R7
                POP     {R4-R8, PC}
da_zero:
MOVS    R0, #0
                POP     {R4-R8, PC}
