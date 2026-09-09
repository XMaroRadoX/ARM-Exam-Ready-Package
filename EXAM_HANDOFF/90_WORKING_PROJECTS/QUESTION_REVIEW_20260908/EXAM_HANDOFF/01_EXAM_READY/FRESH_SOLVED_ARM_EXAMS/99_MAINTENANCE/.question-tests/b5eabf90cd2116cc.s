.syntax unified
.cpu cortex-m3
.thumb
.text
.global chooseNeighbor
.global chooseRandomNeighbor
.global depthFirstSearch
.global depthFirstSearchRandom
chooseNeighbor:
                CMP     R0, #0
                ITE     EQ
                MOVEQ   R0, #1
                BNE     cn_bottom
                BX      LR
cn_bottom:
CMP     R1, #0
                ITE     EQ
                MOVEQ   R0, #2
                BNE     cn_left
                BX      LR
cn_left:
CMP     R2, #0
                ITE     EQ
                MOVEQ   R0, #3
                BNE     cn_top
                BX      LR
cn_top:
CMP     R3, #0
                ITE     EQ
                MOVEQ   R0, #4
                MOVNE   R0, #0
                BX      LR
chooseRandomNeighbor:
                PUSH    {R4-R7, LR}
                SUB     SP, SP, #20
                MOV     R4, SP
                MOVS    R5, #0
                CMP     R0, #0
                BNE     crn_bottom
                MOVS    R6, #1
                STR     R6, [R4, R5, LSL #2]
                ADDS    R5, R5, #1
crn_bottom:
CMP     R1, #0
                BNE     crn_left
                MOVS    R6, #2
                STR     R6, [R4, R5, LSL #2]
                ADDS    R5, R5, #1
crn_left:
CMP     R2, #0
                BNE     crn_top
                MOVS    R6, #3
                STR     R6, [R4, R5, LSL #2]
                ADDS    R5, R5, #1
crn_top:
CMP     R3, #0
                BNE     crn_choose
                MOVS    R6, #4
                STR     R6, [R4, R5, LSL #2]
                ADDS    R5, R5, #1
crn_choose:
CMP     R5, #0
                BEQ     crn_done
                LDR     R6, =0xE000E018
                LDR     R6, [R6]
                UDIV    R7, R6, R5
                MLS     R6, R7, R5, R6
                SUB     R7, R5, #1
                SUB     R6, R7, R6
                LDR     R0, [R4, R6, LSL #2]
crn_return:
ADD     SP, SP, #20
                POP     {R4-R7, PC}
crn_done:
MOVS    R0, #0
                B       crn_return
depthFirstSearch:
                MOVS    R12, #0
                B       dfs_core
depthFirstSearchRandom:
                MOVS    R12, #1
                B       dfs_core
dfs_core:
                PUSH    {R4-R11, R12, LR}
                MOV     R11, R12
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MOV     R7, R3
                MOVS    R8, #0
                LDRB    R9, [R4, R7]
                ORR     R9, R9, #1
                STRB    R9, [R4, R7]
dfs_loop:
ADD     R9, R7, #1
                LDRB    R0, [R4, R9]
                AND     R0, R0, #1
                ADD     R9, R7, R6
                LDRB    R1, [R4, R9]
                AND     R1, R1, #1
                SUB     R9, R7, #1
                LDRB    R2, [R4, R9]
                AND     R2, R2, #1
                SUB     R9, R7, R6
                LDRB    R3, [R4, R9]
                AND     R3, R3, #1
                CMP     R11, #0
                BNE     dfs_choose_random
                BL      chooseNeighbor
                B       dfs_chosen
dfs_choose_random:
                BL      chooseRandomNeighbor
dfs_chosen:
                CMP     R0, #0
                BEQ     dfs_backtrack
                PUSH    {R7, R12}
                ADDS    R8, R8, #1
                CMP     R0, #1
                BEQ     dfs_right
                CMP     R0, #2
                BEQ     dfs_bottom
                CMP     R0, #3
                BEQ     dfs_left
                ORR     R9, R7, #0
                LDRB    R10, [R4, R7]
                ORR     R10, R10, #16
                STRB    R10, [R4, R7]
                SUB     R7, R7, R6
                MOVS    R10, #5
                B       dfs_store_neighbor
dfs_right:
LDRB    R10, [R4, R7]
                ORR     R10, R10, #2
                STRB    R10, [R4, R7]
                ADDS    R7, R7, #1
                MOVS    R10, #9
                B       dfs_store_neighbor
dfs_bottom:
LDRB    R10, [R4, R7]
                ORR     R10, R10, #4
                STRB    R10, [R4, R7]
                ADD     R7, R7, R6
                MOVS    R10, #17
                B       dfs_store_neighbor
dfs_left:
LDRB    R10, [R4, R7]
                ORR     R10, R10, #8
                STRB    R10, [R4, R7]
                SUBS    R7, R7, #1
                MOVS    R10, #3
dfs_store_neighbor:
                LDRB    R9, [R4, R7]
                ORR     R9, R9, R10
                STRB    R9, [R4, R7]
                B       dfs_loop
dfs_backtrack:
CMP     R8, #0
                BEQ     dfs_done
                POP     {R7, R12}
                SUBS    R8, R8, #1
                B       dfs_loop
dfs_done:
POP     {R4-R11, R12, PC}
.balign 4
.ltorg
.global Reset_Handler
.extern SystemInit
.extern __main
Reset_Handler:
                BL      SystemInit
                LDR     R0, =0xE000E010
                MOVS    R1, #0
                STR     R1, [R0]
                LDR     R2, =0xFFFFF
                STR     R2, [R0, #4]
                STR     R1, [R0, #8]
                MOVS    R1, #5
                STR     R1, [R0]
                LDR     R0, =__main
                BX      R0
.ltorg
