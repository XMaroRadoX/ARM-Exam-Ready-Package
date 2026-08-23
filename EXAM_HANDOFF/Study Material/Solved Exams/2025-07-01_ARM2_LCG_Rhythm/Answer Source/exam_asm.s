                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  LCGsequence

DIM             EQU     10

                AREA    LCG_TEST_DATA, DATA, READWRITE
lcg_test_values SPACE   DIM

                AREA    |.text|, CODE, READONLY

                EXPORT  Reset_Handler
                IMPORT  __main
Reset_Handler   PROC
                SUB     SP, SP, #8
                MOV     R4, #256
                STR     R4, [SP]
                LDR     R4, =lcg_test_values
                MOVS    R0, #6          ; Seed.
                MOVS    R5, #0

lcg_reset_loop
                MOVS    R1, #157
                MOVS    R2, #3
                MOVS    R3, #3
                BL      LCGsequence
                STRB    R0, [R4, R5]
                ADDS    R5, R5, #1
                CMP     R5, #DIM
                BLO     lcg_reset_loop

                ADD     SP, SP, #8
                LDR     R0, =__main
                BX      R0
                ENDP

; uint32_t LCGsequence(previous, a, c, shift, modulus)
LCGsequence     PROC
                LDR     R12, [SP]       ; Fifth argument: modulus.
                LSR     R3, R0, R3      ; previous >> shift.
                MUL     R0, R0, R1
                ADDS    R0, R0, R2
                EORS    R0, R0, R3
                UDIV    R1, R0, R12
                MLS     R0, R1, R12, R0
                BX      LR
                ENDP

                LTORG
                ALIGN   4
                END
