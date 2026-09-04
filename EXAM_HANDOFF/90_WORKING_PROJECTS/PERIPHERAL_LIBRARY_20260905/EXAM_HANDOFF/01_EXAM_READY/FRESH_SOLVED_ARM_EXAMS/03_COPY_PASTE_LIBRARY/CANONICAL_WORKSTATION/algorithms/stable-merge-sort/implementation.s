; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT merge
        EXPORT ms
        EXPORT algorithm_stable_merge_sort
        ALIGN 2
merge
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r11}
        ldr.w	r12, [r7, #8]
        cmp	r2, r3
        mov	r8, r2
        mov	lr, r3
        mov	r5, r2
        bhs	_LBB0_5
        cmp	r3, r12
        mov	r8, r2
        mov	lr, r3
        mov	r5, r2
        bhs	_LBB0_5
        mov	r5, r2
        mov	lr, r3
        mov	r8, r2
        ALIGN 2
_LBB0_3
        ldr.w	r9, [r0, r8, lsl #2]
        ldr.w	r4, [r0, lr, lsl #2]
        movs	r6, #0
        cmp	r9, r4
        ite	gt
        movgt	r6, #1
        addle.w	r8, r8, #1
        cmp	r9, r4
        add	lr, r6
        it	lt
        movlt	r4, r9
        str.w	r4, [r1, r5, lsl #2]
        cmp	r8, r3
        add.w	r5, r5, #1
        bhs	_LBB0_5
        cmp	lr, r12
        blo	_LBB0_3
_LBB0_5
        cmp	r3, r8
        bls	_LBB0_9
        add.w	r6, r0, r8, lsl #2
        subs	r6, #4
        sub.w	r3, r3, r8
        ALIGN 2
_LBB0_7
        ldr	r8, [r6, #4]!
        adds	r4, r5, #1
        str.w	r8, [r1, r5, lsl #2]
        subs	r3, #1
        mov	r5, r4
        bne	_LBB0_7
        cmp	r12, lr
        bhi	_LBB0_10
        b	_LBB0_12
_LBB0_9
        mov	r4, r5
        cmp	r12, lr
        bls	_LBB0_12
_LBB0_10
        add.w	r3, r1, r4, lsl #2
        add.w	r4, r0, lr, lsl #2
        subs	r3, #4
        subs	r4, #4
        sub.w	r6, r12, lr
        ALIGN 2
_LBB0_11
        ldr	r5, [r4, #4]!
        subs	r6, #1
        str	r5, [r3, #4]!
        bne	_LBB0_11
_LBB0_12
        cmp	r12, r2
        bls	_LBB0_15
        mvn	r6, #3
        sub.w	r3, r12, r2
        add.w	r2, r6, r2, lsl #2
        add	r0, r2
        add	r1, r2
        ALIGN 2
_LBB0_14
        ldr	r2, [r1, #4]!
        subs	r3, #1
        str	r2, [r0, #4]!
        bne	_LBB0_14
_LBB0_15
        pop.w	{r8, r9, r11}
        pop	{r4, r5, r6, r7, pc}
_Lfunc_end0
        ALIGN 2
ms
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10, r11}
        sub	sp, #4
        subs	r4, r3, r2
        mov	r10, r1
        lsrs	r1, r4, #1
        beq	_LBB1_17
        add.w	r8, r1, r2
        mov	r9, r3
        mov	r1, r10
        mov	r3, r8
        mov	r11, r0
        mov	r5, r2
        bl	ms
        mov	r0, r11
        mov	r1, r10
        mov	r2, r8
        mov	r3, r9
        bl	ms
        mov	r12, r5
        cmp	r8, r5
        bls	_LBB1_10
        cmp	r8, r9
        bhs	_LBB1_10
        mov	r2, r12
        mov	r0, r8
        mov	r1, r12
        ALIGN 2
_LBB1_4
        ldr.w	r3, [r11, r1, lsl #2]
        ldr.w	r6, [r11, r0, lsl #2]
        movs	r5, #0
        cmp	r3, r6
        ite	gt
        movgt	r5, #1
        addle	r1, #1
        cmp	r3, r6
        add	r0, r5
        it	lt
        movlt	r6, r3
        str.w	r6, [r10, r2, lsl #2]
        cmp	r1, r8
        add.w	r2, r2, #1
        bhs	_LBB1_6
        cmp	r0, r9
        blo	_LBB1_4
_LBB1_6
        cmp	r1, r8
        bhs	_LBB1_11
_LBB1_7
        add.w	r3, r11, r1, lsl #2
        subs	r3, #4
        sub.w	r1, r8, r1
        ALIGN 2
_LBB1_8
        ldr	r6, [r3, #4]!
        adds	r5, r2, #1
        str.w	r6, [r10, r2, lsl #2]
        subs	r1, #1
        mov	r2, r5
        bne	_LBB1_8
        cmp	r9, r0
        bhi	_LBB1_12
        b	_LBB1_14
_LBB1_10
        mov	r1, r12
        mov	r0, r8
        mov	r2, r12
        cmp	r1, r8
        blo	_LBB1_7
_LBB1_11
        mov	r5, r2
        cmp	r9, r0
        bls	_LBB1_14
_LBB1_12
        add.w	r1, r10, r5, lsl #2
        add.w	r2, r11, r0, lsl #2
        subs	r1, #4
        subs	r2, #4
        sub.w	r0, r9, r0
        ALIGN 2
_LBB1_13
        ldr	r3, [r2, #4]!
        subs	r0, #1
        str	r3, [r1, #4]!
        bne	_LBB1_13
_LBB1_14
        cmp	r9, r12
        bls	_LBB1_17
        mvn	r0, #3
        add.w	r1, r0, r12, lsl #2
        add.w	r0, r11, r1
        add	r1, r10
        ALIGN 2
_LBB1_16
        ldr	r2, [r1, #4]!
        subs	r4, #1
        str	r2, [r0, #4]!
        bne	_LBB1_16
_LBB1_17
        add	sp, #4
        pop.w	{r8, r9, r10, r11}
        pop	{r4, r5, r6, r7, pc}
_Lfunc_end1
        ALIGN 2
algorithm_stable_merge_sort
        cmp	r0, r2
        it	ne
        cmpne	r0, #0
        bne	_LBB2_2
        bx	lr
_LBB2_2
        cmp	r2, #0
        it	eq
        bxeq	lr
_LBB2_3
        mov	r3, r1
        mov	r1, r2
        movs	r2, #0
        b	ms
_Lfunc_end2
        ALIGN
        END
