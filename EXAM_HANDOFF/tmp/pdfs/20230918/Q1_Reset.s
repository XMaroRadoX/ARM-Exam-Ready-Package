                AREA    SERIES_DATA, DATA, READWRITE, NOINIT
                ALIGN
                EXPORT  series50
series50        SPACE   200
                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  Reset_Handler
                IMPORT  digitaddition
Reset_Handler   PROC
                LDR     R0, =series50
                MOVS    R2, #47
                STR     R2, [R0]
                MOVS    R1, #5
                BL      digitaddition
finished        B       finished
                ENDP
                LTORG
                END
