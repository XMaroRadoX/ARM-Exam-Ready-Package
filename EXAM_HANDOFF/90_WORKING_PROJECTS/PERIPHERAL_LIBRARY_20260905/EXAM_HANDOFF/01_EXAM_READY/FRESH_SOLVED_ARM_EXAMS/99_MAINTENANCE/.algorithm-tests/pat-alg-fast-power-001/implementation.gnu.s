.syntax unified
.cpu cortex-m3
.thumb
.text
.extern __aeabi_uldivmod
.global pat_alg_fast_power_001
.global pat_alg_fast_power_001_checked
.balign 4
pat_alg_fast_power_001:
	push	{r4, r5, r6, r7, lr}
	add	r7, sp, #12
	push.w	{r8, r9, r10}
	mov	r10, r2
	mov	r5, r1
	mov	r6, r0
	cbz	r2, LBB0_2
	udiv	r0, r6, r10
	subs.w	r8, r10, #1
	mls	r6, r0, r10, r6
	mov.w	r9, #0
	it	ne
	movne.w	r8, #1
	cbnz	r5, LBB0_3
	b	LBB0_11
LBB0_2:
	mov.w	r9, #0
	mov.w	r8, #1
	cbz	r5, LBB0_11
LBB0_3:
	movs	r4, #0
	b	LBB0_5
.balign 4
LBB0_4:
	movs	r4, #0
	mov	r6, r0
	lsrs	r5, r5, #1
	beq	LBB0_11
LBB0_5:
	lsls	r0, r5, #31
	beq	LBB0_9
	cmp.w	r10, #0
	umull	r0, r1, r6, r8
	beq	LBB0_8
	mla	r1, r6, r9, r1
	mov	r2, r10
	mla	r1, r4, r8, r1
	movs	r3, #0
	bl	__aeabi_uldivmod
	mov	r8, r2
	mov	r9, r3
	b	LBB0_9
LBB0_8:
	mov.w	r9, #0
	mov	r8, r0
.balign 4
LBB0_9:
	cmp.w	r10, #0
	umull	r0, r1, r6, r6
	beq	LBB0_4
	mla	r1, r6, r4, r1
	mov	r2, r10
	mla	r1, r6, r4, r1
	movs	r3, #0
	bl	__aeabi_uldivmod
	mov	r6, r2
	mov	r4, r3
	lsrs	r5, r5, #1
	bne	LBB0_5
LBB0_11:
	mov	r0, r8
	pop.w	{r8, r9, r10}
	pop	{r4, r5, r6, r7, pc}
Lfunc_end0:
.balign 4
pat_alg_fast_power_001_checked:
	cmp	r2, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB1_1:
	push	{r7, lr}
	mov	r7, sp
	mov.w	r12, #1
	cbnz	r1, LBB1_5
LBB1_2:
	movs	r3, #1
	str.w	r12, [r2]
LBB1_3:
	pop.w	{r7, lr}
	mov	r0, r3
	bx	lr
.balign 4
LBB1_4:
	cmp	r1, #1
	lsr.w	r1, r1, #1
	bls	LBB1_2
LBB1_5:
	lsls	r3, r1, #31
	beq	LBB1_9
	cbz	r0, LBB1_8
	umull	r3, lr, r0, r12
	cmp.w	lr, #0
	bne	LBB1_12
LBB1_8:
	mul	r12, r12, r0
LBB1_9:
	cmp	r1, #1
	beq	LBB1_4
	movs	r3, #0
	cmp.w	r3, r0, lsr #16
	bne	LBB1_3
	muls	r0, r0, r0
	b	LBB1_4
LBB1_12:
	movs	r3, #0
	b	LBB1_3
Lfunc_end1:
