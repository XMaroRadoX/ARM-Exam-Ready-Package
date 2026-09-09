                PRESERVE8
                THUMB

DIM             EQU     10

; Reserve one byte for each result. Every byte is written by the loop.
                AREA    LCG_DATA, DATA, READWRITE, NOINIT
sequence        SPACE   DIM

                AREA    |.text|, CODE, READONLY
                EXPORT  Reset_Handler

; Keep the template startup file: it supplies the stack and vector table.
; This strong handler replaces its WEAK Reset_Handler for Q1 only.
; R4=previous value, R5=index n, R6=array address.
Reset_Handler   PROC
                MOV     R4, #1
                MOV     R5, #0
                LDR     R6, =sequence

generate_loop
                MOV     R0, R4          ; Argument 1: previous value
                MOV     R1, #131        ; Argument 2: a
                MOV     R2, #7          ; Argument 3: c
                MOV     R3, R5          ; Argument 4: n

                SUB     SP, SP, #8      ; Argument 5 plus alignment padding
                MOV     R12, #255
                STR     R12, [SP]       ; Argument 5: m
                BL      nextElementLCG
                ADD     SP, SP, #8      ; Caller releases its argument space

                STRB    R0, [R6, R5]    ; sequence[n] = result (ONE byte)
                MOV     R4, R0          ; Feed result into the next call
                ADD     R5, R5, #1
                CMP     R5, #DIM
                BLO     generate_loop  ; Indices 0..9: exactly ten calls

finished
                B       finished       ; Inspect sequence in the debugger
                ENDP
                LTORG

                AREA    asm_functions, CODE, READONLY
                EXPORT  nextElementLCG

; Inputs: R0=previous, R1=a, R2=c, R3=n, [SP]=m.
; Output: R0=((a * previous + c) XOR n) mod m.
; Parameters in this paper are unsigned and m=255 is nonzero.
nextElementLCG  PROC
                ; Preserve the caller's R4 and the return address: 8 bytes.
                PUSH    {R4, LR}

                ; The fifth argument was at [SP] on entry.
                ; The push moved SP down 8 bytes, so now read [SP + 8].
                LDR     R4, [SP, #8]

                MUL     R0, R1, R0      ; a * previous
                ADD     R0, R0, R2      ; Add c
                EOR     R0, R0, R3      ; XOR with iteration n

                ; Modulo = value - (integer quotient * modulus).
                ; R1's original multiplier is no longer needed.
                UDIV    R1, R0, R4
                MUL     R1, R1, R4
                SUB     R0, R0, R1      ; Leave the remainder in R0

                ; Restore R4 and return by loading the saved LR into PC.
                ; Do not restore R0: that would overwrite our answer.
                POP     {R4, PC}
                ENDP
                END
