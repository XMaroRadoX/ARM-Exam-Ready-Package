.syntax unified
.cpu cortex-m3
.thumb
.text
.global BullsAndCows
BullsAndCows:
                PUSH    {R4-R11, R12, LR}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOV     R7, R3
                MOVS    R8, #0
                MOVS    R9, #0
                MOVS    R10, #0
bac_exact_loop:
CMP     R10, #4
                BHS     bac_exact_done
                LDR     R0, [R4, R10, LSL #2]
                LDR     R1, [R5, R10, LSL #2]
                CMP     R0, R1
                BNE     bac_unmatched
                ADDS    R8, R8, #1
                B       bac_exact_next
bac_unmatched:
LDR     R2, [R6, R0, LSL #2]
                ADDS    R2, R2, #1
                STR     R2, [R6, R0, LSL #2]
                LDR     R2, [R7, R1, LSL #2]
                ADDS    R2, R2, #1
                STR     R2, [R7, R1, LSL #2]
bac_exact_next:
ADDS    R10, R10, #1
                B       bac_exact_loop
bac_exact_done:
MOVS    R10, #0
bac_cow_loop:
CMP     R10, #4
                BHS     bac_return
                LDR     R0, [R6, R10, LSL #2]
                LDR     R1, [R7, R10, LSL #2]
                CMP     R0, R1
                BLS     bac_use_min
                MOV     R0, R1
bac_use_min:
ADDS    R9, R9, R0
                ADDS    R10, R10, #1
                B       bac_cow_loop
bac_return:
MOVS    R0, #1
                LSL     R0, R0, R8
                SUBS    R0, R0, #1
                LSLS    R0, R0, #4
                MOVS    R1, #1
                LSL     R1, R1, R9
                SUBS    R1, R1, #1
                ADDS    R0, R0, R1
                POP     {R4-R11, R12, PC}
.section .rodata
review_guess:
.word 0,1,2,3
review_secret:
.word 1,2,2,0
.section .data
review_scratch:
.space 32
.text
.global Reset_Handler
Reset_Handler:
                LDR     R2, =review_scratch
                MOVS    R0, #0
                MOVS    R1, #0
review_clear:
STR     R0, [R2, R1]
                ADDS    R1, R1, #4
                CMP     R1, #32
                BLO     review_clear
                ADD     R3, R2, #16
                LDR     R0, =review_guess
                LDR     R1, =review_secret
                BL      BullsAndCows
review_finished:
B       review_finished
.ltorg
