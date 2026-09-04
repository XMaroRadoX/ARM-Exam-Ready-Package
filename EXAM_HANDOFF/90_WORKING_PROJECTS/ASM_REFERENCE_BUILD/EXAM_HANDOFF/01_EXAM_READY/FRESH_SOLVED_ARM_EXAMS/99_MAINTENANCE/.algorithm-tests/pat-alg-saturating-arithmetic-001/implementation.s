; Matching Cortex-M3 Thumb implementation generated from reference.c.
; Verification status: COMPILE_ONLY until executed in a simulator/board.
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  pat_alg_saturating_arithmetic_001
                EXPORT  pat_alg_saturating_arithmetic_001_abs_i32
                EXPORT  pat_alg_saturating_arithmetic_001_add_i32

                ALIGN   2
pat_alg_saturating_arithmetic_001
; %bb.0:
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
Lfunc_end0
                                        ; -- End function
                ALIGN   2
pat_alg_saturating_arithmetic_001_abs_i32
; %bb.0:
	cmp	r0, #0
	it	mi
	rsbmi	r0, r0, #0
	bx	lr
Lfunc_end1
                                        ; -- End function
                ALIGN   2
pat_alg_saturating_arithmetic_001_add_i32
; %bb.0:
	adds	r0, r0, r1
	mov.w	r1, #-2147483648
	it	vs
	eorvs.w	r0, r1, r0, asr #31
	bx	lr
Lfunc_end2
                                        ; -- End function

                END
