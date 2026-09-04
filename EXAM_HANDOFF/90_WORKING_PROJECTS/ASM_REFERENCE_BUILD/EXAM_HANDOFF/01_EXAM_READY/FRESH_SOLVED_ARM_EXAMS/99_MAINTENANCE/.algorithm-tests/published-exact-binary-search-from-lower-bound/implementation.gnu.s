.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_exact_binary_search_from_lower_bound
.global algorithm_exact_binary_search_from_lower_bound_exact
.balign 4
algorithm_exact_binary_search_from_lower_bound:
	cmp	r0, #0
	mov.w	r12, #0
	it	ne
	cmpne	r1, #0
	bne	LBB0_2
	mov	r0, r12
	bx	lr
LBB0_2:
	push	{r7, lr}
	mov	r7, sp
	mov.w	r12, #0
.balign 4
LBB0_3:
	sub.w	r3, r1, r12
	add.w	lr, r12, r3, lsr #1
	ldr.w	r3, [r0, lr, lsl #2]
	cmp	r3, r2
	ite	lt
	addlt.w	r12, lr, #1
	movge	r1, lr
	cmp	r12, r1
	blo	LBB0_3
	pop.w	{r7, lr}
	mov	r0, r12
	bx	lr
Lfunc_end0:
.balign 4
algorithm_exact_binary_search_from_lower_bound_exact:
	push	{r4, r6, r7, lr}
	add	r7, sp, #8
	mov	r12, r0
	cmp	r0, #0
	mov.w	r0, #0
	it	ne
	cmpne	r1, #0
	beq	LBB1_3
	mov	lr, r1
.balign 4
LBB1_2:
	sub.w	r3, lr, r0
	add.w	r3, r0, r3, lsr #1
	ldr.w	r4, [r12, r3, lsl #2]
	cmp	r4, r2
	ite	lt
	addlt	r0, r3, #1
	movge	lr, r3
	cmp	r0, lr
	blo	LBB1_2
LBB1_3:
	cmp.w	r12, #0
	beq	LBB1_6
	cmp	r0, r1
	bhs	LBB1_6
	ldr.w	r1, [r12, r0, lsl #2]
	cmp	r1, r2
	it	ne
	movne.w	r0, #-1
	pop	{r4, r6, r7, pc}
LBB1_6:
	mov.w	r0, #-1
	pop	{r4, r6, r7, pc}
Lfunc_end1:
