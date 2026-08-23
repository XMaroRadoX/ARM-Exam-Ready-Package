; Rare/dangerous template: SysTick free-running down-counter, no interrupt.
; CSR=0xE000E010, RVR=+4, CVR=+8. Reload must fit 24 bits.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  systick_raw_start

systick_raw_start PROC
                LDR     R0, =0xE000E010
                MOVS    R1, #0
                STR     R1, [R0, #0]
                LDR     R1, =0x000FFFFF
                STR     R1, [R0, #4]
                MOVS    R1, #0
                STR     R1, [R0, #8]
                MOVS    R1, #5          ; ENABLE + processor clock, no TICKINT
                STR     R1, [R0, #0]
                BX      LR
                ENDP

                LTORG
                END
