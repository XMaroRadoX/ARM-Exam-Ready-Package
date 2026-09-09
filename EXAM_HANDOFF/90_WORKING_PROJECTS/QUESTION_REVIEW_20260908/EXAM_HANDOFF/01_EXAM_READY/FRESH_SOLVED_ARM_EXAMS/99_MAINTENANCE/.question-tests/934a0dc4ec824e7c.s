.syntax unified
.cpu cortex-m3
.thumb
.text
.global kruskal
kruskal:
                MOV     R12, SP
                PUSH    {R4-R11, LR}
                SUB     SP, SP, #4
                LDR     R4, [R12]
                LDR     R5, [R12, #4]
                LDR     R6, [R12, #8]
                MOV     R7, R0
                MOV     R8, R1
                MOV     R9, R2
                MUL     R10, R3, R4
kr_loop:
ADD     R6, R6, R5
                CMP     R6, R10
                BHS     kr_vertical
                LDRB    R0, [R8, R6]
                CMP     R0, #0
                BNE     kr_h_wall
                ADDS    R5, R5, #1
                B       kr_check_done
kr_h_wall:
CMP     R0, #1
                BNE     kr_check_done
                ADD     R11, R6, #1
                LDRB    R2, [R7, R6]
                LDRB    R3, [R7, R11]
                CMP     R2, R3
                BEQ     kr_check_done
                MOVS    R0, #0
                STRB    R0, [R8, R6]
                B       kr_merge
kr_vertical:
SUB     R6, R6, R10
                CMP     R6, R10
                BHS     kr_check_done
                LDRB    R0, [R9, R6]
                CMP     R0, #0
                BNE     kr_v_wall
                ADDS    R5, R5, #1
                B       kr_check_done
kr_v_wall:
CMP     R0, #1
                BNE     kr_check_done
                ADD     R11, R6, R4
                LDRB    R2, [R7, R6]
                LDRB    R3, [R7, R11]
                CMP     R2, R3
                BEQ     kr_check_done
                MOVS    R0, #0
                STRB    R0, [R9, R6]
kr_merge:
CMP     R2, R3
                ITE     LO
                MOVLO   R0, R2
                MOVHS   R0, R3
                ITE     LO
                MOVLO   R1, R3
                MOVHS   R1, R2
                MOVS    R11, #0
kr_replace:
CMP     R11, R10
                BHS     kr_check_done
                LDRB    R2, [R7, R11]
                CMP     R2, R1
                IT      EQ
                STRBEQ  R0, [R7, R11]
                ADDS    R11, R11, #1
                B       kr_replace
kr_check_done:
MOVS    R11, #0
kr_nonzero:
CMP     R11, R10
                BHS     kr_done
                LDRB    R0, [R7, R11]
                CMP     R0, #0
                BNE     kr_loop
                ADDS    R11, R11, #1
                B       kr_nonzero
kr_done:
ADD     SP, SP, #4
                POP     {R4-R11, PC}
