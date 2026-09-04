; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT pat_ds_circular_queue_001
        ALIGN 2
pat_ds_circular_queue_001
        cbz	r0, _LBB0_10
        ldr.w	r12, [r0]
        cmp.w	r12, #0
        beq	_LBB0_10
        mov.w	r3, #0
        cbz	r2, _LBB0_11
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r8, [sp, #-4]!
        ldr	r4, [r0, #4]
        cbz	r4, _LBB0_16
        mov	r3, r0
        ldr	r5, [r3, #8]!
        cmp	r5, r4
        bhs	_LBB0_15
        mov	lr, r0
        ldr	r6, [lr, #12]!
        cmp	r6, r4
        bhs	_LBB0_15
        ldr.w	r8, [r0, #16]
        cmp	r8, r4
        bhi	_LBB0_15
        cbz	r1, _LBB0_12
        cmp	r8, r4
        beq	_LBB0_15
        ldr	r1, [r2]
        str.w	r1, [r12, r6, lsl #2]
        movs	r1, #1
        b	_LBB0_14
_LBB0_10
        movs	r3, #0
_LBB0_11
        mov	r0, r3
        bx	lr
_LBB0_12
        cmp.w	r8, #0
        beq	_LBB0_15
        ldr.w	r1, [r12, r5, lsl #2]
        mov	lr, r3
        str	r1, [r2]
        mov.w	r1, #-1
_LBB0_14
        ldr.w	r2, [lr]
        ldr	r3, [r0, #4]
        adds	r2, #1
        udiv	r6, r2, r3
        mls	r2, r6, r3, r2
        ldr	r3, [r0, #16]
        str.w	r2, [lr]
        add	r1, r3
        movs	r3, #1
        str	r1, [r0, #16]
        b	_LBB0_16
_LBB0_15
        movs	r3, #0
_LBB0_16
        ldr	r8, [sp], #4
        pop.w	{r4, r5, r6, r7, lr}
        mov	r0, r3
        bx	lr
_Lfunc_end0
        ALIGN
        END
