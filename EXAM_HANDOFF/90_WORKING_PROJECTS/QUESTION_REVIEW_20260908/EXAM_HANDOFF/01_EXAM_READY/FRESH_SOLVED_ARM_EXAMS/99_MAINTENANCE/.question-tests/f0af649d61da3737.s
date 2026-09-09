.syntax unified
.cpu cortex-m3
.thumb
.text
.global Recaman
Recaman:
                PUSH    {R4-R10, LR}
                MOV     R4, R0
                UXTB    R5, R1
                CMP     R5, #0
                BEQ     recaman_done
                MOVS    R6, #0
                STR     R6, [R4]
                MOVS    R6, #1
recaman_loop:
                CMP     R6, R5
                BHS     recaman_done
                SUBS    R7, R6, #1
                LDR     R8, [R4, R7, LSL #2]
                SUBS    R9, R8, R6
                CMP     R9, #0
                BLE     recaman_add
                MOVS    R7, #0
recaman_search:
                CMP     R7, R6
                BHS     recaman_use_candidate
                LDR     R10, [R4, R7, LSL #2]
                CMP     R10, R9
                BEQ     recaman_add
                ADDS    R7, R7, #1
                B       recaman_search
recaman_use_candidate:
                STR     R9, [R4, R6, LSL #2]
                B       recaman_next
recaman_add:
                ADDS    R9, R8, R6
                STR     R9, [R4, R6, LSL #2]
recaman_next:
                ADDS    R6, R6, #1
                B       recaman_loop
recaman_done:
                POP     {R4-R10, PC}
.ltorg
.balign 4
