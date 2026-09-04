.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_saturating_addition
.global algorithm_saturating_addition_abs_i32
.global algorithm_saturating_addition_add_i32
.balign 4
algorithm_saturating_addition:
	push	{r7, lr}
	mov	r7, sp
	asr.w	r12, r3, #31
	subs.w	lr, r3, r0
	sbcs.w	r12, r12, r1
	mov	r12, r0
	it	lt
	movlt	r12, r3
	subs	r0, r0, r2
	sbcs.w	r0, r1, r2, asr #31
	it	lt
	movlt	r12, r2
	cmp	r2, r3
	it	gt
	movgt	r12, r2
	mov	r0, r12
	pop	{r7, pc}
Lfunc_end0:
.balign 4
algorithm_saturating_addition_abs_i32:
	cmp	r0, #0
	it	mi
	rsbmi	r0, r0, #0
	bx	lr
Lfunc_end1:
.balign 4
algorithm_saturating_addition_add_i32:
	adds	r0, r0, r1
	mov.w	r1, #-2147483648
	it	vs
	eorvs.w	r0, r1, r0, asr #31
	bx	lr
Lfunc_end2:
