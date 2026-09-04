.syntax unified
.cpu cortex-m3
.thumb
.text
.global classify_result_flags
classify_result_flags:
                CMP     R0, #0
                MRS     R1, APSR
                LDR     R2, =0xC0000000
                ANDS    R1, R1, R2
                MSR     APSR_nzcvq, R1
                BX      LR
.ltorg
.global classify_and_read
classify_and_read:
                PUSH {R4,LR}
                BL classify_result_flags
                MRS R0,APSR
                POP {R4,PC}
