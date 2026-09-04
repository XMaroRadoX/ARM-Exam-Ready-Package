; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_bounded_counting_sort
        ALIGN 2
algorithm_bounded_counting_sort
        cmp.w	r2, #256
        mov.w	r12, #0
        bhi	_LBB0_19
        cmp	r0, #0
        beq	_LBB0_19
        cmp	r3, #0
        beq	_LBB0_19
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        cbz	r2, _LBB0_6
        sub.w	r12, r3, #4
        mov.w	lr, #0
        mov	r4, r2
        ALIGN 2
_LBB0_5
        subs	r4, #1
        str	lr, [r12, #4]!
        bne	_LBB0_5
_LBB0_6
        cbz	r1, _LBB0_10
        mov	r12, r0
        ALIGN 2
_LBB0_8
        ldrb	lr, [r12], #1
        cmp	lr, r2
        bhs	_LBB0_17
        ldr.w	r4, [r3, lr, lsl #2]
        subs	r1, #1
        add.w	r4, r4, #1
        str.w	r4, [r3, lr, lsl #2]
        bne	_LBB0_8
_LBB0_10
        cbz	r2, _LBB0_16
        mov.w	lr, #0
        mov.w	r12, #0
        b	_LBB0_14
        ALIGN 2
_LBB0_12
        mov	r4, lr
_LBB0_13
        add.w	r12, r12, #1
        cmp	r12, r2
        mov	lr, r4
        beq	_LBB0_16
_LBB0_14
        ldr.w	r1, [r3, r12, lsl #2]
        cmp	r1, #0
        beq	_LBB0_12
        ALIGN 2
_LBB0_15
        subs	r1, #1
        str.w	r1, [r3, r12, lsl #2]
        strb.w	r12, [r0, lr]
        ldr.w	r1, [r3, r12, lsl #2]
        add.w	r4, lr, #1
        cmp	r1, #0
        mov	lr, r4
        bne	_LBB0_15
        b	_LBB0_13
_LBB0_16
        mov.w	r12, #1
        b	_LBB0_18
_LBB0_17
        mov.w	r12, #0
_LBB0_18
        pop.w	{r4, r6, r7, lr}
_LBB0_19
        mov	r0, r12
        bx	lr
_Lfunc_end0
        ALIGN
        END
