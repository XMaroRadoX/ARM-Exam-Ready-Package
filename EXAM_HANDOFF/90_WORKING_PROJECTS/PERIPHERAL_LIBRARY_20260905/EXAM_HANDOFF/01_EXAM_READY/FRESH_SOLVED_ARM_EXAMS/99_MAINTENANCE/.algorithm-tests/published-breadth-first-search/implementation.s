; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_breadth_first_search
        ALIGN 2
algorithm_breadth_first_search
        cmp	r0, #0
        mov.w	r12, #0
        it	ne
        cmpne	r3, #0
        bne	_LBB0_2
        mov	r0, r12
        bx	lr
_LBB0_2
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r8, [sp, #-4]!
        ldr.w	lr, [r7, #8]
        cmp.w	lr, #0
        beq	_LBB0_12
        mov.w	r12, #0
        cmp.w	r12, r1, lsr #16
        bne	_LBB0_12
        cmp	r2, r1
        bhs	_LBB0_12
        mov.w	r8, #1
        strb.w	r8, [r3, r2]
        str.w	r2, [lr]
        movs	r2, #1
        b	_LBB0_7
        ALIGN 2
_LBB0_6
        cmp	r12, r2
        bhs	_LBB0_12
_LBB0_7
        ldr.w	r5, [lr, r12, lsl #2]
        add.w	r12, r12, #1
        mla	r5, r5, r1, r0
        movs	r6, #0
        b	_LBB0_9
        ALIGN 2
_LBB0_8
        adds	r6, #1
        cmp	r1, r6
        beq	_LBB0_6
_LBB0_9
        ldrb	r4, [r5, r6]
        cmp	r4, #0
        beq	_LBB0_8
        ldrb	r4, [r3, r6]
        cmp	r4, #0
        bne	_LBB0_8
        strb.w	r8, [r3, r6]
        str.w	r6, [lr, r2, lsl #2]
        adds	r2, #1
        b	_LBB0_8
_LBB0_12
        ldr	r8, [sp], #4
        pop.w	{r4, r5, r6, r7, lr}
        mov	r0, r12
        bx	lr
_Lfunc_end0
        ALIGN
        END
