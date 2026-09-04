.syntax unified
.cpu cortex-m3
.thumb
.text
.global pat_alg_integer_sqrt_001
.balign 4
pat_alg_integer_sqrt_001:
	mov.w	r1, #1073741824
.balign 4
LBB0_1:
	mov	r2, r1
	cmp	r1, r0
	lsr.w	r1, r1, #2
	bhi	LBB0_1
	cmp	r2, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB0_3:
	movs	r3, #0
.balign 4
LBB0_4:
	adds	r1, r3, r2
	subs	r1, r0, r1
	it	hs
	movhs	r0, r1
	add.w	r1, r2, r3, lsr #1
	it	lo
	lsrlo	r1, r3, #1
	lsrs	r2, r2, #2
	mov	r3, r1
	bne	LBB0_4
	mov	r0, r1
	bx	lr
Lfunc_end0:
