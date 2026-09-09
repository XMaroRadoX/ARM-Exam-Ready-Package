.syntax unified
.cpu cortex-m3
.thumb
.text
.global mazeSolver
mazeSolver:
                PUSH    {R4-R11, R12, LR}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                MUL     R7, R4, R5
                MOVS    R8, #0
ms_iteration:
MOVS    R9, #0
                MOVS    R10, #0
ms_phase1:
CMP     R10, R7
                BHS     ms_phase2_begin
                LDRB    R0, [R6, R10]
                CMP     R0, #' '
                BNE     ms_p1_next
                SUB     R1, R10, R5
                LDRB    R0, [R6, R1]
                CMP     R0, #'a'
                BLO     ms_right
                CMP     R0, #'z'
                BHI     ms_right
                MOVS    R0, #'N'
                B       ms_mark
ms_right:
ADD     R1, R10, #1
                LDRB    R0, [R6, R1]
                CMP     R0, #'a'
                BLO     ms_bottom
                CMP     R0, #'z'
                BHI     ms_bottom
                MOVS    R0, #'E'
                B       ms_mark
ms_bottom:
ADD     R1, R10, R5
                LDRB    R0, [R6, R1]
                CMP     R0, #'a'
                BLO     ms_left
                CMP     R0, #'z'
                BHI     ms_left
                MOVS    R0, #'S'
                B       ms_mark
ms_left:
SUB     R1, R10, #1
                LDRB    R0, [R6, R1]
                CMP     R0, #'a'
                BLO     ms_p1_next
                CMP     R0, #'z'
                BHI     ms_p1_next
                MOVS    R0, #'W'
ms_mark:
STRB    R0, [R6, R10]
                MOVS    R9, #1
ms_p1_next:
ADDS    R10, R10, #1
                B       ms_phase1
ms_phase2_begin:
MOVS    R10, #0
ms_phase2:
CMP     R10, R7
                BHS     ms_phase_done
                LDRB    R0, [R6, R10]
                CMP     R0, #'N'
                BEQ     ms_lower
                CMP     R0, #'E'
                BEQ     ms_lower
                CMP     R0, #'S'
                BEQ     ms_lower
                CMP     R0, #'W'
                BNE     ms_p2_next
ms_lower:
ADDS    R0, R0, #32
                STRB    R0, [R6, R10]
ms_p2_next:
ADDS    R10, R10, #1
                B       ms_phase2
ms_phase_done:
CMP     R9, #0
                BEQ     ms_done
                ADDS    R8, R8, #1
                B       ms_iteration
ms_done:
MOV     R0, R8
                POP     {R4-R11, R12, PC}
