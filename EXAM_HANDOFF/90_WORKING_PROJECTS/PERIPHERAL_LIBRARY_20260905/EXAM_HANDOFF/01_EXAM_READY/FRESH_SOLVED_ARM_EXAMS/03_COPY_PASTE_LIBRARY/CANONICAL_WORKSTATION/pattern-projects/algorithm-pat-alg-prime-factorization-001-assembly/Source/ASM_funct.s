; Matching Cortex-M3 Thumb implementation generated from reference.c.

                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  algorithm_algorithm_pat_alg_prime_factorization_001_assembly
                EXPORT  algorithm_algorithm_pat_alg_prime_factorization_001_assembly_factorize

                ALIGN   2
algorithm_algorithm_pat_alg_prime_factorization_001_assembly
; %bb.0:
	cmp	r0, #2
	bhs	LBB0_2
LBB0_1
	movs	r0, #0
	bx	lr
LBB0_2
	lsls	r1, r0, #31
	bne	LBB0_4
; %bb.3:
	subs	r0, #2
	clz	r0, r0
	lsrs	r0, r0, #5
	bx	lr
LBB0_4
	cmp	r0, #9
	itt	lo
	movlo	r0, #1
	bxlo	lr
LBB0_5
	movs	r1, #3
                ALIGN   2
LBB0_6                                ; =>This Inner Loop Header: Depth=1
	udiv	r2, r0, r1
	mls	r2, r2, r1, r0
	cmp	r2, #0
	beq	LBB0_1
; %bb.7:                                ;   in Loop: Header=BB0_6 Depth=1
	adds	r1, #2
	udiv	r2, r0, r1
	cmp	r1, r2
	itt	hi
	movhi	r0, #1
	bxhi	lr
	b	LBB0_6
Lfunc_end0
                                        ; -- End function
                ALIGN   2
algorithm_algorithm_pat_alg_prime_factorization_001_assembly_factorize
; %bb.0:
	push	{r4, r6, r7, lr}
	add	r7, sp, #8
	clz	r3, r1
	lsr.w	r12, r3, #5
	cmp	r2, #0
	mov	r3, r2
	it	ne
	movne	r3, #1
	tst.w	r12, r3
	mov.w	r4, #0
	bne	LBB1_8
; %bb.1:
	cmp	r0, #2
	blo	LBB1_8
; %bb.2:
	mov.w	r12, #2
	b	LBB1_4
                ALIGN   2
LBB1_3                                ;   in Loop: Header=BB1_4 Depth=1
	cmp.w	r12, #2
	add.w	r12, r12, #2
	it	eq
	moveq.w	r12, #3
	cmp	r0, #1
	bls	LBB1_8
LBB1_4                                ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB1_6 Depth 2
	udiv	lr, r0, r12
	cmp	r12, lr
	bhi	LBB1_7
; %bb.5:                                ;   in Loop: Header=BB1_4 Depth=1
	mls	r3, lr, r12, r0
	cmp	r3, #0
	bne	LBB1_3
                ALIGN   2
LBB1_6                                ;   Parent Loop BB1_4 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	udiv	r0, r0, r12
	cmp	r4, r2
	udiv	r3, r0, r12
	it	lo
	strlo.w	r12, [r1, r4, lsl #2]
	mls	r3, r3, r12, r0
	adds	r4, #1
	cmp	r3, #0
	beq	LBB1_6
	b	LBB1_3
LBB1_7
	cmp	r4, r2
	it	lo
	strlo.w	r0, [r1, r4, lsl #2]
	adds	r4, #1
LBB1_8
	mov	r0, r4
	pop	{r4, r6, r7, pc}
Lfunc_end1
                                        ; -- End function

                END
