; Recommended exam template: build a word recurrence iteratively.
; C prototype: void triangular_sequence(uint32_t *v, uint32_t n);
; v[0]=0; v[i]=v[i-1]+i. Static/global storage is preferred for large arrays.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  triangular_sequence

triangular_sequence PROC
                CMP     R1, #0
                BEQ     sequence_done
                MOVS    R2, #0
                STR     R2, [R0]
                MOVS    R3, #1
sequence_loop   CMP     R3, R1
                BHS     sequence_done
                ADDS    R2, R2, R3
                STR     R2, [R0, R3, LSL #2]
                ADDS    R3, R3, #1
                B       sequence_loop
sequence_done   BX      LR
                ENDP

                END
