; Rare/dangerous template: strong Reset_Handler in the answer assembly file.
; C runtime is not ready before __main. Do not return through LR.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  Reset_Handler
                IMPORT  __main

Reset_Handler   PROC
                ; Perform only the paper's reset-safe register/data work here.
                LDR     R0, =__main
                BX      R0
                ENDP

                END
