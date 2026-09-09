; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_algorithm_pat_alg_lis_001_assembly
        ALIGN 2
algorithm_algorithm_pat_alg_lis_001_assembly
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r11, [sp, #-4]!
        mov	lr, r0
        cmp	r0, #0
        mov.w	r0, #0
        it	ne
        cmpne	r2, #0
        bne	_LBB0_2
_LBB0_1
        ldr	r11, [sp], #4
        pop	{r4, r5, r6, r7, pc}
_LBB0_2
        cmp	r1, #0
        beq	_LBB0_1
        mov.w	r12, #1
        movs	r3, #0
        b	_LBB0_5
        ALIGN 2
_LBB0_4
        ldr.w	r4, [r2, r3, lsl #2]
        adds	r3, #1
        cmp	r4, r0
        it	hi
        movhi	r0, r4
        cmp	r3, r1
        beq	_LBB0_1
_LBB0_5
        cmp	r3, #0
        str.w	r12, [r2, r3, lsl #2]
        beq	_LBB0_4
        movs	r4, #0
        b	_LBB0_8
        ALIGN 2
_LBB0_7
        adds	r4, #1
        cmp	r3, r4
        beq	_LBB0_4
_LBB0_8
        ldr.w	r5, [lr, r4, lsl #2]
        ldr.w	r6, [lr, r3, lsl #2]
        cmp	r5, r6
        bge	_LBB0_7
        ldr.w	r5, [r2, r4, lsl #2]
        ldr.w	r6, [r2, r3, lsl #2]
        adds	r5, #1
        cmp	r5, r6
        it	hi
        strhi.w	r5, [r2, r3, lsl #2]
        b	_LBB0_7
_Lfunc_end0
        ALIGN
        END
