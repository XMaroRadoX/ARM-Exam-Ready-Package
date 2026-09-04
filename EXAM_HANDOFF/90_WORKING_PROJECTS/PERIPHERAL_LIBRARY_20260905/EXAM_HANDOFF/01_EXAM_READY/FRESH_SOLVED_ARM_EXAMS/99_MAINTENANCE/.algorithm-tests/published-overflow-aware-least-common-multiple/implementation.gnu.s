.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_overflow_aware_least_common_multiple
.global algorithm_overflow_aware_least_common_multiple_lcm
.balign 4
algorithm_overflow_aware_least_common_multiple:
	cmp	r1, #0
	it	eq
	bxeq	lr
.balign 4
LBB0_1:
	mov	r2, r1
	udiv	r1, r0, r1
	mls	r1, r1, r2, r0
	mov	r0, r2
	cmp	r1, #0
	bne	LBB0_1
	mov	r0, r2
	bx	lr
Lfunc_end0:
.balign 4
algorithm_overflow_aware_least_common_multiple_lcm:
	cbz	r2, LBB1_6
	cmp	r0, #0
	mov.w	r3, #0
	it	ne
	cmpne	r1, #0
	bne	LBB1_3
LBB1_2:
	movs	r0, #1
	str	r3, [r2]
	bx	lr
LBB1_3:
	push	{r4, r6, r7, lr}
	add	r7, sp, #8
	mov	r12, r0
	mov	lr, r1
.balign 4
LBB1_4:
	udiv	r3, r12, lr
	mov	r4, lr
	mls	lr, r3, lr, r12
	mov	r12, r4
	cmp.w	lr, #0
	bne	LBB1_4
	udiv	r0, r0, r4
	umull	r3, r4, r1, r0
	cmp	r4, #0
	pop.w	{r4, r6, r7, lr}
	beq	LBB1_7
LBB1_6:
	movs	r0, #0
	bx	lr
LBB1_7:
	mul	r3, r0, r1
	b	LBB1_2
Lfunc_end1:
