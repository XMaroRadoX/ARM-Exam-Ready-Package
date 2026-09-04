                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  shortestPath

; uint32_t shortestPath(uint32_t rows, uint32_t columns, uint8_t *maze)
shortestPath    PROC
                PUSH    {R4-R11, R12, LR}
                MOV     R4, R1          ; columns
                MOV     R5, R2          ; maze
                MUL     R6, R0, R1      ; cells
                MOVS    R7, #0          ; current wave value
sp_wave        MOVS    R8, #0
sp_scan        CMP     R8, R6
                BHS     sp_next_wave
                LDRB    R9, [R5, R8]
                CMP     R9, #' '
                BNE     sp_check_entry
                SUB     R10, R8, R4
                LDRB    R11, [R5, R10]
                CMP     R11, R7
                BEQ     sp_mark
                ADD     R10, R8, #1
                LDRB    R11, [R5, R10]
                CMP     R11, R7
                BEQ     sp_mark
                ADD     R10, R8, R4
                LDRB    R11, [R5, R10]
                CMP     R11, R7
                BEQ     sp_mark
                SUB     R10, R8, #1
                LDRB    R11, [R5, R10]
                CMP     R11, R7
                BNE     sp_scan_next
sp_mark         ADDS    R9, R7, #1
                STRB    R9, [R5, R8]
                B       sp_scan_next
sp_check_entry  CMP     R9, #'e'
                BNE     sp_scan_next
                SUB     R10, R8, R4
                LDRB    R11, [R5, R10]
                CMP     R11, R7
                BEQ     sp_found
                ADD     R10, R8, #1
                LDRB    R11, [R5, R10]
                CMP     R11, R7
                BEQ     sp_found
                ADD     R10, R8, R4
                LDRB    R11, [R5, R10]
                CMP     R11, R7
                BEQ     sp_found
                SUB     R10, R8, #1
                LDRB    R11, [R5, R10]
                CMP     R11, R7
                BEQ     sp_found
sp_scan_next    ADDS    R8, R8, #1
                B       sp_scan
sp_next_wave    ADDS    R7, R7, #1
                B       sp_wave
sp_found        MOV     R0, R7
                POP     {R4-R11, R12, PC}
                ENDP
                END

