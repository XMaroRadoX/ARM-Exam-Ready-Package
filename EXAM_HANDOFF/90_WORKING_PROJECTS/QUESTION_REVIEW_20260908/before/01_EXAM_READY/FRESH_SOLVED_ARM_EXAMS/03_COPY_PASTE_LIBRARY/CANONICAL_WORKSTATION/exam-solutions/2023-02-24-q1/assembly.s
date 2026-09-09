                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  KaprekarRoutine
                EXPORT  SVC_Handler

; uint32_t KaprekarRoutine(uint32_t a)
; R0 is a four-digit number. The 10-word local table counts its digits.
KaprekarRoutine PROC
                PUSH    {R4-R11, LR}
                SUB     SP, SP, #44     ; 36+44 = 80 bytes, preserving alignment
                MOV     R4, SP          ; frequency[10]
                MOVS    R5, #0
kap_clear       CMP     R5, #10
                BHS     kap_extract
                MOVS    R6, #0
                STR     R6, [R4, R5, LSL #2]
                ADDS    R5, R5, #1
                B       kap_clear

kap_extract     MOV     R7, R0
                MOVS    R5, #4
                MOVS    R8, #10
kap_digit       UDIV    R9, R7, R8
                MLS     R10, R9, R8, R7 ; remainder = value - quotient*10
                LDR     R11, [R4, R10, LSL #2]
                ADDS    R11, R11, #1
                STR     R11, [R4, R10, LSL #2]
                MOV     R7, R9
                SUBS    R5, R5, #1
                BNE     kap_digit

                MOVS    R6, #0          ; descending number b
                MOVS    R5, #9
kap_desc_digit  LDR     R7, [R4, R5, LSL #2]
kap_desc_repeat CMP     R7, #0
                BEQ     kap_desc_next
                MUL     R6, R6, R8
                ADD     R6, R6, R5
                SUBS    R7, R7, #1
                B       kap_desc_repeat
kap_desc_next   SUBS    R5, R5, #1
                BPL     kap_desc_digit

                MOVS    R7, #0          ; ascending number c
                MOVS    R5, #0
kap_asc_digit   LDR     R9, [R4, R5, LSL #2]
kap_asc_repeat  CMP     R9, #0
                BEQ     kap_asc_next
                MUL     R7, R7, R8
                ADD     R7, R7, R5
                SUBS    R9, R9, #1
                B       kap_asc_repeat
kap_asc_next    ADDS    R5, R5, #1
                CMP     R5, #10
                BLO     kap_asc_digit

                SUB     R0, R6, R7
                ADD     SP, SP, #44
                POP     {R4-R11, PC}
                ENDP

; Supervisor service 50 repeatedly applies KaprekarRoutine and leaves the
; iteration count in R6 as required by the paper. The caller uses MSP.
SVC_Handler     PROC
                MRS     R7, MSP         ; original hardware frame before software saves
                PUSH    {R4, R5, R7, LR}
                LDR     R5, [R7, #24]
                LDRB    R5, [R5, #-2]
                CMP     R5, #50
                BNE     svc_return
                LDR     R0, [R7]
                MOVS    R6, #0
svc_loop        BL      KaprekarRoutine
                ADDS    R6, R6, #1
                MOVW    R5, #6174
                CMP     R0, R5
                BNE     svc_loop
                STR     R0, [R7]        ; make final R0 visible after exception return
svc_return      POP     {R4, R5, R7, LR}
                BX      LR
                ENDP
                END
