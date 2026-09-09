.syntax unified
.cpu cortex-m3
.thumb
.text
.global Look_and_Say
Look_and_Say:
                PUSH    {R4-R10, LR}
                SUB     SP, SP, #16
                MOV     R4, SP
                MOV     R5, R0
                MOVS    R6, #0
                MOVS    R10, #10
extract_digits:
                UDIV    R7, R5, R10
                MLS     R8, R7, R10, R5
                STRB    R8, [R4, R6]
                ADDS    R6, R6, #1
                MOV     R5, R7
                CMP     R5, #0
                BNE     extract_digits
                SUBS    R6, R6, #1
                LDRB    R7, [R4, R6]
                MOVS    R8, #1
                MOVS    R9, #0
look_loop:
                CMP     R6, #0
                BEQ     append_look_run
                SUBS    R6, R6, #1
                LDRB    R5, [R4, R6]
                CMP     R5, R7
                BNE     append_then_continue
                ADDS    R8, R8, #1
                B       look_loop
append_then_continue:
                MUL     R9, R9, R10
                ADD     R9, R9, R8
                MUL     R9, R9, R10
                ADD     R9, R9, R7
                MOV     R7, R5
                MOVS    R8, #1
                B       look_loop
append_look_run:
                MUL     R9, R9, R10
                ADD     R9, R9, R8
                MUL     R9, R9, R10
                ADD     R9, R9, R7
                MOV     R0, R9
                ADD     SP, SP, #16
                POP     {R4-R10, PC}
.ltorg
.balign 4
