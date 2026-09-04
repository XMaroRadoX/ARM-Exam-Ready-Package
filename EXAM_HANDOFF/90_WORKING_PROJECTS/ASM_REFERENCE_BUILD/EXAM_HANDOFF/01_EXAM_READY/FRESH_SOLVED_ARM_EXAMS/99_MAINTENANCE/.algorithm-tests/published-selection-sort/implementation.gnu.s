.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_selection_sort
.balign 4
algorithm_selection_sort:
        cmp	r0, #0
        it	ne
        cmpne	r1, #0
        bne	_LBB0_2
        bx	lr
_LBB0_2:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r8, [sp, #-4]!
        rsb.w	r8, r1, #0
        adds	r3, r0, #4
        mov.w	r12, #0
        b	_LBB0_4
.balign 4
_LBB0_3:
        cmp	lr, r1
        mov	r12, lr
        beq	_LBB0_9
_LBB0_4:
        add.w	lr, r12, #1
        cmp	lr, r1
        mov	r4, r12
        bhs	_LBB0_7
        mov	r5, r12
        mov	r4, r12
.balign 4
_LBB0_6:
        ldr.w	r6, [r3, r5, lsl #2]
        ldr.w	r2, [r0, r4, lsl #2]
        adds	r5, #1
        cmp	r6, r2
        add.w	r2, r8, r5
        it	lt
        movlt	r4, r5
        adds	r2, #1
        bne	_LBB0_6
_LBB0_7:
        cmp	r4, r12
        beq	_LBB0_3
        ldr.w	r2, [r0, r4, lsl #2]
        ldr.w	r5, [r0, r12, lsl #2]
        str.w	r2, [r0, r12, lsl #2]
        str.w	r5, [r0, r4, lsl #2]
        b	_LBB0_3
_LBB0_9:
        ldr	r8, [sp], #4
        pop.w	{r4, r5, r6, r7, lr}
        bx	lr
_Lfunc_end0:
.balign 4
