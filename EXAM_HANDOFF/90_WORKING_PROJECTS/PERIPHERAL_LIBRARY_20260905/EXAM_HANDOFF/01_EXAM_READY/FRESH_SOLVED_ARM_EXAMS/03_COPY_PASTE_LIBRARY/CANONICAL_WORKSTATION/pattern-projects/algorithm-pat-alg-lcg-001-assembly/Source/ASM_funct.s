; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; uint32_t algorithm_algorithm_pat_alg_lcg_001_assembly(uint32_t x, uint32_t a, uint32_t c,
;                              uint32_t modulus, uint32_t shift)
; Fifth argument is [SP]. Leaf; no stack frame. Arithmetic wraps modulo 2^32.
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  algorithm_algorithm_pat_alg_lcg_001_assembly

algorithm_algorithm_pat_alg_lcg_001_assembly PROC
                LDR     R12, [SP]
                MLA     R1, R1, R0, R2
                CMP     R3, #0
                BEQ     lcg_modulo_done
                UDIV    R0, R1, R3
                MLS     R1, R0, R3, R1
lcg_modulo_done
                MOVS    R0, #0
                CMP     R12, #32
                IT      LO
                LSRLO   R0, R1, R12
                BX      LR
                ENDP

                LTORG
                ALIGN   2
                END
