                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  isSociable
                EXPORT  aliquotSum

; uint32_t isSociable(uint32_t n)
; R0: input n, then return value (0 or a cycle length from 1 to 8).
isSociable      PROC
                PUSH    {R4-R6, LR}     ; 16 bytes; keep SP 8-byte aligned.
                CMP     R0, #2          ; 0 and 1 are not sociable.
                BLO     not_found
                MOV     R4, R0          ; Preserve original n across BL.
                MOV     R5, R0          ; Current sequence value.
                MOVS    R6, #0          ; Computed sums, excluding input.

sequence_loop
                MOV     R0, R5          ; Argument for aliquotSum.
                BL      aliquotSum     ; R0 becomes s(current).
                ADDS    R6, R6, #1      ; Exactly one new term computed.
                CMP     R0, R4
                BEQ     found          ; Success even on the eighth term.
                CMP     R0, #1
                BLS     not_found      ; 1 per paper; also safely handles 0.
                CMP     R6, #8
                BEQ     not_found      ; No return to n within 8 terms.
                MOV     R5, R0          ; Next input is the latest sum.
                B       sequence_loop

found
                MOV     R0, R6          ; Return cycle length.
                POP     {R4-R6, PC}
not_found
                MOVS    R0, #0
                POP     {R4-R6, PC}
                ENDP

; uint32_t aliquotSum(uint32_t n)
; Implements the paper's divisor-pair algorithm literally for n >= 2.
; R0=n, R1=sum, R2=a, R3=b, R12=remainder. No nested calls.
; Exam inputs and intermediate sums are assumed to fit uint32_t.
aliquotSum      PROC
                CMP     R0, #2
                BLO     small_number
                MOVS    R1, #1          ; Include divisor 1, exclude n.
                MOVS    R2, #2          ; First candidate divisor.
divisor_loop
                UDIV    R3, R0, R2      ; b = floor(n / a).
                MLS     R12, R3, R2, R0 ; remainder = n - b*a.
                CMP     R12, #0
                BNE     next_divisor   ; Not divisible: try a+1.
                CMP     R2, R3
                BLO     add_pair       ; a < b: add two distinct divisors.
                BEQ     add_square     ; a == b: count sqrt(n) once.
                B       sum_done       ; a > b: pair already counted.
add_pair
                ADDS    R1, R1, R2
                ADDS    R1, R1, R3
                B       next_divisor
add_square
                ADDS    R1, R1, R2
sum_done
                MOV     R0, R1
                BX      LR
next_divisor
                ADDS    R2, R2, #1
                B       divisor_loop
small_number
                MOVS    R0, #0
                BX      LR
                ENDP
                ALIGN
                END
