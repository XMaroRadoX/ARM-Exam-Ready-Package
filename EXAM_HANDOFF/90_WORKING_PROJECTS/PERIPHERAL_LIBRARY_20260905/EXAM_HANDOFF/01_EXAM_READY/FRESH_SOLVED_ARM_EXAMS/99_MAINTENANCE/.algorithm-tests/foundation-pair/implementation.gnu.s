.syntax unified
.cpu cortex-m3
.thumb
.text
.global first_equal_pair
first_equal_pair:
                PUSH    {R4-R6, LR}
                MOVS    R4, #0
outer_loop:
CMP     R4, R2
                BHS     pair_not_found
                LDR     R5, [R0, R4, LSL #2]
                MOVS    R6, #0
inner_loop:
CMP     R6, R3
                BHS     outer_next
                LDR     R12, [R1, R6, LSL #2]
                CMP     R5, R12
                BEQ     pair_found
                ADDS    R6, R6, #1
                B       inner_loop
outer_next:
ADDS    R4, R4, #1
                B       outer_loop
pair_found:
LSLS    R0, R4, #16
                ORRS    R0, R0, R6
                POP     {R4-R6, PC}
pair_not_found:
MOVS    R0, #0
                MVNS    R0, R0
                POP     {R4-R6, PC}
