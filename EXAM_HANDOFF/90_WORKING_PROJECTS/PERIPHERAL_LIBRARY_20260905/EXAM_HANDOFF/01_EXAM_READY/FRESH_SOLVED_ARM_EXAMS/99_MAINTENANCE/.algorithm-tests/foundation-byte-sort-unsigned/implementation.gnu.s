.syntax unified
.cpu cortex-m3
.thumb
.text
.global copyData
.global insertionSortUnsigned
copyData:
                CMP     R2, #0
                BEQ     copy_done
copy_loop:
                LDRB    R3, [R0], #1
                STRB    R3, [R1], #1
                SUBS    R2, R2, #1
                BNE     copy_loop
copy_done:
                BX      LR
insertionSortUnsigned:
                PUSH    {R4-R8, LR}
                MOV     R4, R0
                MOV     R5, R1
                CMP     R5, #1
                BLS     sort_done
                MOVS    R6, #1
sort_outer:
                CMP     R6, R5
                BHS     sort_done
                LDRB   R7, [R4, R6]
                SUBS    R8, R6, #1
sort_inner:
                CMP     R8, #0
                BLT     sort_insert
                LDRB   R0, [R4, R8]
                CMP     R0, R7
                BLS     sort_insert
                ADDS    R1, R8, #1
                STRB    R0, [R4, R1]
                SUBS    R8, R8, #1
                B       sort_inner
sort_insert:
                ADDS    R8, R8, #1
                STRB    R7, [R4, R8]
                ADDS    R6, R6, #1
                B       sort_outer
sort_done:
                POP     {R4-R8, PC}
.ltorg
.balign 4
