.syntax unified
.cpu cortex-m3
.thumb
.text
.global Mastermind
Mastermind:
                PUSH    {R4-R11, R12, LR}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOV     R7, R3
                MOVS    R8, #0
                MOVS    R9, #0
                MOVS    R10, #0
mm_exact_loop:
CMP     R10, #4
                BHS     mm_exact_done
                LDR     R0, [R4, R10, LSL #2]
                LDR     R1, [R5, R10, LSL #2]
                CMP     R0, R1
                BNE     mm_exact_next
                ADDS    R8, R8, #1
                MOVS    R2, #1
                STR     R2, [R6, R10, LSL #2]
                STR     R2, [R7, R10, LSL #2]
mm_exact_next:
ADDS    R10, R10, #1
                B       mm_exact_loop
mm_exact_done:
MOVS    R10, #0
mm_outer_loop:
CMP     R10, #4
                BHS     mm_return
                LDR     R0, [R6, R10, LSL #2]
                CMP     R0, #0
                BNE     mm_outer_next
                LDR     R2, [R4, R10, LSL #2]
                MOVS    R11, #0
mm_inner_loop:
CMP     R11, #4
                BHS     mm_outer_next
                LDR     R0, [R7, R11, LSL #2]
                CMP     R0, #0
                BNE     mm_inner_next
                LDR     R1, [R5, R11, LSL #2]
                CMP     R2, R1
                BNE     mm_inner_next
                ADDS    R9, R9, #1
                MOVS    R0, #1
                STR     R0, [R6, R10, LSL #2]
                STR     R0, [R7, R11, LSL #2]
                B       mm_outer_next
mm_inner_next:
ADDS    R11, R11, #1
                B       mm_inner_loop
mm_outer_next:
ADDS    R10, R10, #1
                B       mm_outer_loop
mm_return:
MOVS    R0, #1
                LSL     R0, R0, R8
                SUBS    R0, R0, #1
                LSLS    R0, R0, #4
                MOVS    R1, #1
                LSL     R1, R1, R9
                SUBS    R1, R1, #1
                ADDS    R0, R0, R1
                POP     {R4-R11, R12, PC}
