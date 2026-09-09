.syntax unified
.cpu cortex-m3
.thumb
.text
.global HofstadterConway
HofstadterConway:
                PUSH    {R4-R10, LR}
                MOV     R4, R0
                MOV     R5, R1
                CMP     R5, #0
                BLE     hc_empty
                MOVS    R7, #1
                STR     R7, [R4]
                CMP     R5, #1
                BEQ     hc_done
                STR     R7, [R4, #4]
                MOVS    R6, #2
hc_loop:
                CMP     R6, R5
                BHS     hc_done
                SUBS    R10, R6, #1
                LDR     R8, [R4, R10, LSL #2]
                SUBS    R10, R8, #1
                LDR     R9, [R4, R10, LSL #2]
                SUBS    R10, R6, R8
                LDR     R10, [R4, R10, LSL #2]
                ADDS    R10, R9, R10
                STR     R10, [R4, R6, LSL #2]
                CMP     R10, R7
                BLS     hc_keep_maximum
                MOV     R7, R10
hc_keep_maximum:
                ADDS    R6, R6, #1
                B       hc_loop
hc_done:
                MOV     R0, R7
                POP     {R4-R10, PC}
hc_empty:
                MOVS    R0, #0
                POP     {R4-R10, PC}
.ltorg
.balign 4
