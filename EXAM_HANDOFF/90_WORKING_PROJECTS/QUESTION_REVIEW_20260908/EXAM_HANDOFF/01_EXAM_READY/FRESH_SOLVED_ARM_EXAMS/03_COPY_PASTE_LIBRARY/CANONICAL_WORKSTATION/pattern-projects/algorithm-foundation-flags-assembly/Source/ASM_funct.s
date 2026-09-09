; Rare/dangerous template: set N/Z from R0 and clear C/V in APSR_nzcvq.
; Flags are caller-clobbered. Use only when the paper requires flag output.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  classify_result_flags

classify_result_flags PROC
                CMP     R0, #0
                MRS     R1, APSR
                LDR     R2, =0xC0000000
                ANDS    R1, R1, R2
                MSR     APSR_nzcvq, R1
                BX      LR
                ENDP

                LTORG
                EXPORT classify_and_read
classify_and_read PROC
                PUSH {R4,LR}
                BL classify_result_flags
                MRS R0,APSR
                POP {R4,PC}
                ENDP
                END
