; Rare/dangerous template: SVC immediate decode and stacked-R0 result.
; Enable exact SVC ownership before defining this handler.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  SVC_Handler

SVC_Handler     PROC
                TST     LR, #4
                ITE     EQ
                MRSEQ   R0, MSP
                MRSNE   R0, PSP
                LDR     R1, [R0, #24]
                LDRB    R1, [R1, #-2]
                CMP     R1, #50
                BNE     svc_invalid
                LDR     R2, [R0]
                ADDS    R2, R2, #1
                STR     R2, [R0]
                BX      LR
svc_invalid     MOVS    R2, #0
                MVNS    R2, R2
                STR     R2, [R0]
                BX      LR
                ENDP

                END
