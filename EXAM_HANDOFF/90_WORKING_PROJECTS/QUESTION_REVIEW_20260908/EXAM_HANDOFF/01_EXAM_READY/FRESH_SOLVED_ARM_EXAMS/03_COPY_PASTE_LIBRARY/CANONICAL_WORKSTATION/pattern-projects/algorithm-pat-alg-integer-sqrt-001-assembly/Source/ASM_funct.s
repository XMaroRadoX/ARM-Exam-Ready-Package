; Matching Cortex-M3 Thumb implementation generated from reference.c.

                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  algorithm_algorithm_pat_alg_integer_sqrt_001_assembly

                ALIGN   2
algorithm_algorithm_pat_alg_integer_sqrt_001_assembly
; %bb.0:
	mov.w	r1, #1073741824
                ALIGN   2
LBB0_1                                ; =>This Inner Loop Header: Depth=1
	mov	r2, r1
	cmp	r1, r0
	lsr.w	r1, r1, #2
	bhi	LBB0_1
; %bb.2:
	cmp	r2, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB0_3
	movs	r3, #0
                ALIGN   2
LBB0_4                                ; =>This Inner Loop Header: Depth=1
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
; %bb.5:
	mov	r0, r1
	bx	lr
Lfunc_end0
                                        ; -- End function

                END
