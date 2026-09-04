.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_five_argument_linear_congruential_generator
algorithm_five_argument_linear_congruential_generator:
                LDR     R12, [SP]
                MLA     R1, R1, R0, R2
                CMP     R3, #0
                BEQ     lcg_modulo_done
                UDIV    R0, R1, R3
                MLS     R1, R0, R3, R1
lcg_modulo_done:
                MOVS    R0, #0
                CMP     R12, #32
                IT      LO
                LSRLO   R0, R1, R12
                BX      LR
.ltorg
.balign 4
