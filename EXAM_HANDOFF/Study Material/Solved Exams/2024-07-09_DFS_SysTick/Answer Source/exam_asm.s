; ============================================================================
; 2_WRITE_ASM_HERE.s
; This is the assembly file you normally edit during the exam.
; ============================================================================

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB

; C declaration: extern uint32_t exam_asm_example(uint32_t value);
; Input R0. Return value R0.
                EXPORT  exam_asm_example
exam_asm_example PROC
                ADDS    R0, R0, #1
                BX      LR
                ENDP

; COPY THIS SHAPE WHEN YOU USE R4-R11 OR CALL ANOTHER FUNCTION
; my_function   PROC
;               EXPORT  my_function
;               PUSH    {R4, LR}       ; preserve R4 and the return address
;               MOV     R4, R0
;               BL      helper
;               ADD     R0, R0, R4
;               POP     {R4, PC}
;               ENDP

; WHEN THERE ARE MORE THAN FOUR ARGUMENTS
; Save the caller's original SP before pushing registers.
; five_args     PROC
;               EXPORT  five_args
;               MOV     R12, SP
;               PUSH    {R4-R7, R12, LR} ; six registers keeps SP aligned
;               LDR     R4, [R12]       ; argument 5
;               LDR     R5, [R12, #4]   ; argument 6
;               ; R0-R3 still hold arguments 1-4
;               ; ... required calculation ...
;               POP     {R4-R7, R12, PC}
;               ENDP

; WHEN THE QUESTION REQUIRES THE EXACT SVC HANDLER
; 1. Set EXAM_OWN_SVC_HANDLER to 1 in exam_config.h.
; 2. Uncomment this shape and add the required service cases.
; Hardware stacked: R0,R1,R2,R3,R12,LR,PC,xPSR.
;
;               EXPORT  SVC_Handler
; SVC_Handler   PROC
;               TST     LR, #4
;               ITE     EQ
;               MRSEQ   R0, MSP         ; R0 = active stack frame
;               MRSNE   R0, PSP
;               LDR     R1, [R0, #24]   ; stacked return PC
;               LDRB    R1, [R1, #-2]   ; SVC immediate number
;               CMP     R1, #0
;               BNE     svc_done
;               LDR     R2, [R0]        ; stacked R0 argument/result
;               ADDS    R2, R2, #1
;               STR     R2, [R0]
; svc_done      BX      LR
;               ENDP

; AAPCS reminders:
; - R0-R3 hold the first four arguments and may be changed by a call.
; - Preserve R4-R11 when you use them.
; - Save LR before BL. Keep SP eight-byte aligned at public call boundaries.
; - Argument 5 is at the caller's original SP, argument 6 at original SP+4.
; - Return 32 bits in R0, or 64 bits in R0:R1.
; - Use LDRSB/LDRSH and signed branches for signed data.
; - Put ALIGN after byte or halfword data before words or code.

                LTORG
                ALIGN   4
                END
