; Recommended exam template: minimal AAPCS leaf function
; C prototype: uint32_t add_then_double(uint32_t a, uint32_t b);
; Inputs R0=a, R1=b. Output R0. Clobbers R0/APSR only.
; No stack use, no privilege requirement, safe in Thread or Handler mode.

                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  add_then_double

add_then_double PROC
                ADDS    R0, R0, R1
                LSLS    R0, R0, #1
                BX      LR
                ENDP

                END
