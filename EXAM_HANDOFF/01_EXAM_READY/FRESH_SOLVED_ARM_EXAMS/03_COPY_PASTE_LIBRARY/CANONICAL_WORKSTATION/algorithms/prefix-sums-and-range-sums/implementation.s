; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_prefix_sums_and_range_sums
        EXPORT algorithm_prefix_sums_and_range_sums_range
        ALIGN 2
algorithm_prefix_sums_and_range_sums
        cmp	r2, #0
        itt	eq
        moveq	r0, #0
        bxeq	lr
_LBB0_1
        push	{r7, lr}
        mov	r7, sp
        movw	r3, #65534
        cmp	r1, #0
        mov	lr, r1
        movt	r3, #8191
        it	ne
        movne.w	lr, #1
        cmp	r1, r3
        mov.w	r12, #0
        bhi	_LBB0_7
        clz	r3, r0
        lsrs	r3, r3, #5
        ands.w	r3, r3, lr
        bne	_LBB0_7
        movs	r3, #0
        str	r3, [r2]
        str	r3, [r2, #4]
        cbz	r1, _LBB0_6
        ldrd	r3, r12, [r2], #-8
        sub.w	lr, r0, #4
        ALIGN 2
_LBB0_5
        ldr	r0, [lr, #4]!
        adds	r3, r3, r0
        adc.w	r12, r12, r0, asr #31
        strd	r3, r12, [r2, #16]
        subs	r1, #1
        add.w	r2, r2, #8
        bne	_LBB0_5
_LBB0_6
        mov.w	r12, #1
_LBB0_7
        pop.w	{r7, lr}
        mov	r0, r12
        bx	lr
_Lfunc_end0
        ALIGN 2
algorithm_prefix_sums_and_range_sums_range
        mov	r12, r0
        cmp	r3, r1
        mov.w	r0, #0
        it	ls
        cmpls	r2, r3
        bls	_LBB1_2
        bx	lr
_LBB1_2
        cmp.w	r12, #0
        it	eq
        bxeq	lr
_LBB1_3
        push	{r7, lr}
        mov	r7, sp
        ldr.w	lr, [r7, #8]
        cmp.w	lr, #0
        beq	_LBB1_5
        add.w	r0, r12, r3, lsl #3
        ldr.w	r3, [r12, r3, lsl #3]
        add.w	r1, r12, r2, lsl #3
        ldr.w	r2, [r12, r2, lsl #3]
        ldr	r0, [r0, #4]
        ldr	r1, [r1, #4]
        subs	r2, r3, r2
        sbcs	r0, r1
        strd	r2, r0, [lr]
        movs	r0, #1
_LBB1_5
        pop.w	{r7, lr}
        bx	lr
_Lfunc_end1
        ALIGN
        END
