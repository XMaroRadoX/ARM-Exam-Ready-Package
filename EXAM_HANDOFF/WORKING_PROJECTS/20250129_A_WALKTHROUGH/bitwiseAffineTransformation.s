        AREA    AffineCode, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT  bitwiseAffineTransformation

; R0 = address of eight row bytes, top row first
; R1 = b (low eight bits)
; R2 = c (low eight bits)
; Returns R0 = d (zero extended)
bitwiseAffineTransformation PROC
        PUSH    {R4-R7}
        MOVS    R3, #0          ; Accumulated matrix-vector product
        MOVS    R4, #8          ; Eight rows

row_loop
        LDRB    R5, [R0], #1    ; Read one row and advance one byte
        AND     R5, R5, R1      ; Eight pairwise AND products
        MOVS    R6, #0          ; Parity accumulator
        MOVS    R7, #8          ; Eight bits in this row

bit_loop
        AND     R12, R5, #1     ; Extract current least significant bit
        EOR     R6, R6, R12     ; XOR it into the parity
        LSRS    R5, R5, #1      ; Bring next bit into bit zero
        SUBS    R7, R7, #1
        BNE     bit_loop

        LSLS    R3, R3, #1      ; Make room for next row result
        ORR     R3, R3, R6      ; Append parity as bit zero
        SUBS    R4, R4, #1
        BNE     row_loop

        EOR     R0, R3, R2      ; Add c using XOR
        UXTB    R0, R0          ; Return an unsigned eight-bit result
        POP     {R4-R7}
        BX      LR
        ENDP
        END
