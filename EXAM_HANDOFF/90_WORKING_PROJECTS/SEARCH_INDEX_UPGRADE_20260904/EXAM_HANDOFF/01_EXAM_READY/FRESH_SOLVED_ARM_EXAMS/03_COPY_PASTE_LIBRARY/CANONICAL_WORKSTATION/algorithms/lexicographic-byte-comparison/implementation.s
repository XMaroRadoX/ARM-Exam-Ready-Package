; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_lexicographic_byte_comparison_length
        EXPORT algorithm_lexicographic_byte_comparison_compare
        EXPORT algorithm_lexicographic_byte_comparison_copy
        EXPORT algorithm_lexicographic_byte_comparison
        ALIGN 2
algorithm_lexicographic_byte_comparison_length
        mov	r2, r0
        cmp	r0, #0
        mov.w	r0, #0
        it	ne
        cmpne	r1, #0
        bne	_LBB0_2
        bx	lr
        ALIGN 2
_LBB0_2
        ldrb	r3, [r2, r0]
        cmp	r3, #0
        it	eq
        bxeq	lr
_LBB0_3
        adds	r0, #1
        cmp	r1, r0
        bne	_LBB0_2
        mov	r0, r1
        bx	lr
_Lfunc_end0
        ALIGN 2
algorithm_lexicographic_byte_comparison_compare
        mov	r12, r0
        cmp	r0, #0
        mov.w	r0, #0
        it	ne
        cmpne	r1, #0
        bne	_LBB1_2
        bx	lr
_LBB1_2
        cmp	r2, #0
        it	eq
        bxeq	lr
_LBB1_3
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        ALIGN 2
_LBB1_4
        ldrb	r3, [r12], #1
        ldrb	lr, [r1], #1
        cmp	r3, #0
        sub.w	lr, r3, lr
        clz	r4, lr
        it	ne
        movne	r3, #1
        lsrs	r4, r4, #5
        ands	r3, r4
        it	eq
        moveq	r0, lr
        beq	_LBB1_7
        subs	r2, #1
        bne	_LBB1_4
        movs	r0, #0
_LBB1_7
        pop.w	{r4, r6, r7, lr}
        bx	lr
_Lfunc_end1
        ALIGN 2
algorithm_lexicographic_byte_comparison_copy
        cmp	r1, #0
        mov.w	r3, #0
        it	ne
        cmpne	r0, #0
        bne	_LBB2_2
_LBB2_1
        mov	r0, r3
        bx	lr
_LBB2_2
        cmp	r2, #0
        beq	_LBB2_1
        mov.w	r12, #0
        cmp	r1, #2
        blo	_LBB2_8
        push	{r7, lr}
        mov	r7, sp
        sub.w	lr, r1, #1
        movs	r3, #0
        ALIGN 2
_LBB2_5
        ldrb	r1, [r2, r3]
        cbz	r1, _LBB2_7
        strb	r1, [r0, r3]
        adds	r3, #1
        cmp	lr, r3
        bne	_LBB2_5
_LBB2_7
        pop.w	{r7, lr}
_LBB2_8
        strb.w	r12, [r0, r3]
        mov	r0, r3
        bx	lr
_Lfunc_end2
        ALIGN 2
algorithm_lexicographic_byte_comparison
        mov	r12, r0
        cmp	r0, #0
        mov.w	r0, #-1
        it	ne
        cmpne	r1, #0
        bne	_LBB3_2
        bx	lr
_LBB3_2
        ldrb	r0, [r1]
        cbz	r0, _LBB3_15
        cmp	r2, #0
        itt	eq
        moveq.w	r0, #-1
        bxeq	lr
_LBB3_4
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r8, [sp, #-4]!
        add.w	lr, r1, #1
        movs	r0, #0
        mov	r8, r12
        ALIGN 2
_LBB3_5
        ldrb.w	r3, [r12, r0]
        cbz	r3, _LBB3_13
        ldrb	r4, [r1]
        cbz	r4, _LBB3_11
        subs	r5, r2, r0
        movs	r3, #0
        ALIGN 2
_LBB3_8
        ldrb.w	r6, [r8, r3]
        cmp	r6, r4
        bne	_LBB3_11
        adds	r6, r3, #1
        ldrb.w	r4, [lr, r3]
        cmp	r6, r5
        bhs	_LBB3_11
        cmp	r4, #0
        mov	r3, r6
        bne	_LBB3_8
        ALIGN 2
_LBB3_11
        cbz	r4, _LBB3_14
        adds	r0, #1
        cmp	r0, r2
        add.w	r8, r8, #1
        bne	_LBB3_5
_LBB3_13
        mov.w	r0, #-1
_LBB3_14
        ldr	r8, [sp], #4
        pop	{r4, r5, r6, r7, pc}
_LBB3_15
        movs	r0, #0
        bx	lr
_Lfunc_end3
        ALIGN
        END
