; Recommended exam template: scan an unsigned word array for its maximum.
; C prototype: uint32_t array_max_u32(const uint32_t *v, uint32_t n);
; Precondition: v != NULL and n > 0. Uses unsigned BHS/HI conditions.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  array_max_u32

array_max_u32   PROC
                LDR     R2, [R0]
                MOVS    R3, #1
max_loop        CMP     R3, R1
                BHS     max_done
                LDR     R12, [R0, R3, LSL #2]
                CMP     R12, R2
                BLS     max_next
                MOV     R2, R12
max_next        ADDS    R3, R3, #1
                B       max_loop
max_done        MOV     R0, R2
                BX      LR
                ENDP

                END
