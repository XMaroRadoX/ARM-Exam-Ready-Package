        AREA    Maclaurin_Code, CODE, READONLY
        THUMB
        EXPORT  Maclaurin

; int Maclaurin(int y, int n)
; R0: y on entry, answer on return. R1: nonnegative n.
; R2: y*y. R3: current term. R4: total. R5: i.
; R6: denominator. R7: temporary value.

Maclaurin PROC
        PUSH    {R4-R7, LR}

        MUL     R2, R0, R0      ; y squared
        MOV     R3, #10
        MUL     R3, R0, R3      ; t0 = 10*y
        MOV     R4, R3          ; total = t0
        MOV     R5, #1          ; first new term has index 1

next_term
        CMP     R5, R1
        BGT     finished       ; stop when i > n

        MUL     R3, R3, R2
        RSB     R3, R3, #0      ; numerator = -previous_term*y*y

        ADD     R6, R5, R5      ; 2*i
        ADD     R7, R6, #1      ; 2*i + 1
        MUL     R6, R6, R7
        MOV     R7, #100
        MUL     R6, R6, R7      ; denominator = (2*i)*(2*i+1)*100

        SDIV    R3, R3, R6      ; signed division, truncate toward zero
        ADD     R4, R4, R3      ; add new term
        ADD     R5, R5, #1
        B       next_term

finished
        MOV     R0, R4
        POP     {R4-R7, PC}
        ENDP
        END
