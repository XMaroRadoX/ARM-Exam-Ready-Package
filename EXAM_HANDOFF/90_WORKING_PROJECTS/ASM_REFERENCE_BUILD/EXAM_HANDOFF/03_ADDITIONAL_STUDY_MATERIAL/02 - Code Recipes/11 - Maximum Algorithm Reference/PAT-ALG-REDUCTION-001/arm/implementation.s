; Handwritten Cortex-M3 Thumb exam reference.
; Verification status is supplied by the simulator/build reports.
; int pat_alg_reduction_001(const int32_t *values, uint32_t count,
;                               signed_result_t *result)
; result offsets: minimum=0, maximum=4, int64 sum low=8/high=12.
; Leaf; saves R4-R11 (32-byte frame).
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  pat_alg_reduction_001

pat_alg_reduction_001 PROC
                CMP     R0, #0
                BEQ     reduction_invalid
                CMP     R2, #0
                BEQ     reduction_invalid
                CMP     R1, #0
                BEQ     reduction_invalid
                PUSH    {R4-R11}
                MOV     R4, R0
                MOV     R5, R1
                MOV     R6, R2
                LDR     R8, [R4]
                MOV     R9, R8
                MOVS    R10, #0
                MOVS    R11, #0
                MOVS    R7, #0
reduction_loop
                LDR     R3, [R4, R7, LSL #2]
                CMP     R3, R8
                IT      LT
                MOVLT   R8, R3
                CMP     R3, R9
                IT      GT
                MOVGT   R9, R3
                ADDS    R10, R10, R3
                ASR     R2, R3, #31
                ADC     R11, R11, R2
                ADDS    R7, R7, #1
                CMP     R7, R5
                BNE     reduction_loop
                STR     R8, [R6, #0]
                STR     R9, [R6, #4]
                STR     R10, [R6, #8]
                STR     R11, [R6, #12]
                MOVS    R0, #1
                POP     {R4-R11}
                BX      LR
reduction_invalid
                MOVS    R0, #0
                BX      LR
                ENDP

                LTORG
                ALIGN   2
        EXPORT pat_alg_reduction_001_unsigned
pat_alg_reduction_001_unsigned
        cmp r0,#0
        beq ur_bad
        cmp r2,#0
        beq ur_bad
        cmp r1,#0
        beq ur_bad
        push {r4-r9}
        ldr r4,[r0]
        mov r5,r4
        movs r6,#0
        movs r7,#0
        movs r8,#0
ur_loop
        cmp r8,r1
        bhs ur_done
        ldr r9,[r0,r8,lsl #2]
        cmp r9,r4
        bhs ur_max
        mov r4,r9
ur_max
        cmp r9,r5
        bls ur_sum
        mov r5,r9
ur_sum
        adds r6,r6,r9
        adc r7,r7,#0
        adds r8,#1
        b ur_loop
ur_done
        str r4,[r2]
        str r5,[r2,#4]
        str r6,[r2,#8]
        str r7,[r2,#12]
        movs r0,#1
        pop {r4-r9}
        bx lr
ur_bad
        movs r0,#0
        bx lr

        ALIGN
        END
