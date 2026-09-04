                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  nextElementLCG

DIM             EQU     10

                AREA    LCG_TEST_DATA, DATA, READWRITE, NOINIT
; The template scatter file places this area in an UNINIT region.
lcg_test_values SPACE   DIM

                AREA    |.text|, CODE, READONLY

; Reset starts at the hardware vector, fills the test array required by
; question 1, then hands control to the C runtime and main program.
                EXPORT  Reset_Handler
                IMPORT  __main
Reset_Handler   PROC
                SUB     SP, SP, #8      ; Keep SP aligned; argument 5 at [SP].
                MOVS    R4, #255
                STR     R4, [SP]
                LDR     R4, =lcg_test_values
                MOVS    R0, #1          ; Seed.
                MOVS    R5, #0          ; Index n.

lcg_reset_loop
                MOVS    R1, #131
                MOVS    R2, #7
                MOV     R3, R5
                BL      nextElementLCG
                STRB    R0, [R4, R5]
                ADDS    R5, R5, #1
                CMP     R5, #DIM
                BLO     lcg_reset_loop

                ADD     SP, SP, #8
                LDR     R0, =__main
                BX      R0
                ENDP

; uint32_t nextElementLCG(previous, a, c, index, modulus)
nextElementLCG  PROC
                LDR     R12, [SP]       ; Fifth argument: modulus.
                MUL     R0, R0, R1
                ADDS    R0, R0, R2
                EORS    R0, R0, R3
                UDIV    R1, R0, R12
                MLS     R0, R1, R12, R0
                BX      LR
                ENDP

                ALIGN   4
                LTORG
                ALIGN   4
                END
