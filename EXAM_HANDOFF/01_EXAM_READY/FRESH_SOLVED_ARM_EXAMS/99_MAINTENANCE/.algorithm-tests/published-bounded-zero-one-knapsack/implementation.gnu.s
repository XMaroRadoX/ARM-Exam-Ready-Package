.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_bounded_zero_one_knapsack
.balign 4
algorithm_bounded_zero_one_knapsack:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10}
        ldr.w	lr, [r7, #8]
        mov.w	r12, #0
        cmp.w	lr, #0
        beq	_LBB0_13
        cmp	r2, #0
        mov	r4, r2
        it	ne
        movne	r4, #1
        cmp.w	r12, r2, lsr #16
        bne	_LBB0_13
        clz	r5, r0
        clz	r6, r1
        lsrs	r5, r5, #5
        lsrs	r6, r6, #5
        orrs	r5, r6
        ands	r4, r5
        bne	_LBB0_13
        movw	r4, #65534
        movt	r4, #16383
        cmp	r3, r4
        bhi	_LBB0_13
        sub.w	r6, lr, #4
        mov.w	r5, #-1
        movs	r4, #0
.balign 4
_LBB0_5:
        adds	r5, #1
        cmp	r3, r5
        str	r4, [r6, #4]!
        bne	_LBB0_5
        cbz	r2, _LBB0_12
        mov.w	r12, #0
        b	_LBB0_9
.balign 4
_LBB0_8:
        add.w	r12, r12, #1
        cmp	r12, r2
        beq	_LBB0_12
_LBB0_9:
        ldrh.w	r9, [r0, r12, lsl #1]
        cmp	r9, r3
        bhi	_LBB0_8
        ldrh.w	r8, [r1, r12, lsl #1]
        sub.w	r10, lr, r9, lsl #2
        mov	r5, r3
.balign 4
_LBB0_11:
        ldr.w	r4, [r10, r5, lsl #2]
        ldr.w	r6, [lr, r5, lsl #2]
        add	r4, r8
        cmp	r4, r6
        it	hi
        strhi.w	r4, [lr, r5, lsl #2]
        cmp	r5, r9
        sub.w	r5, r5, #1
        bhi	_LBB0_11
        b	_LBB0_8
_LBB0_12:
        ldr.w	r12, [lr, r3, lsl #2]
_LBB0_13:
        mov	r0, r12
        pop.w	{r8, r9, r10}
        pop	{r4, r5, r6, r7, pc}
_Lfunc_end0:
.balign 4
