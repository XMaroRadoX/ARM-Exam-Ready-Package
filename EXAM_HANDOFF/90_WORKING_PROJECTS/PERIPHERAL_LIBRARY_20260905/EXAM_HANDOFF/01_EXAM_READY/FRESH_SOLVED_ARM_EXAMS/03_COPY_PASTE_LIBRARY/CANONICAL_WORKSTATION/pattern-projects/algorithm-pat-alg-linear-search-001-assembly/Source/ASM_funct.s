; Matching Cortex-M3 Thumb implementation generated from reference.c.

                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  algorithm_algorithm_pat_alg_linear_search_001_assembly
                EXPORT  algorithm_algorithm_pat_alg_linear_search_001_assembly_last
                EXPORT  algorithm_algorithm_pat_alg_linear_search_001_assembly_all

                ALIGN   2
algorithm_algorithm_pat_alg_linear_search_001_assembly
; %bb.0:
	mov	r12, r0
	cmp	r0, #0
	mov.w	r0, #-1
	it	ne
	cmpne	r1, #0
	bne	LBB0_2
; %bb.1:
	bx	lr
LBB0_2
	movs	r0, #0
                ALIGN   2
LBB0_3                                ; =>This Inner Loop Header: Depth=1
	ldr.w	r3, [r12, r0, lsl #2]
	cmp	r3, r2
	it	eq
	bxeq	lr
LBB0_4                                ;   in Loop: Header=BB0_3 Depth=1
	adds	r0, #1
	cmp	r1, r0
	bne	LBB0_3
; %bb.5:
	mov.w	r0, #-1
	bx	lr
Lfunc_end0
                                        ; -- End function
                ALIGN   2
algorithm_algorithm_pat_alg_linear_search_001_assembly_last
; %bb.0:
	cbz	r0, LBB1_4
; %bb.1:
	sub.w	r12, r0, #4
                ALIGN   2
LBB1_2                                ; =>This Inner Loop Header: Depth=1
	cbz	r1, LBB1_4
; %bb.3:                                ;   in Loop: Header=BB1_2 Depth=1
	ldr.w	r3, [r12, r1, lsl #2]
	subs	r0, r1, #1
	cmp	r3, r2
	mov	r1, r0
	it	eq
	bxeq	lr
	b	LBB1_2
LBB1_4
	mov.w	r0, #-1
	bx	lr
Lfunc_end1
                                        ; -- End function
                ALIGN   2
algorithm_algorithm_pat_alg_linear_search_001_assembly_all
; %bb.0:
	cmp	r0, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB2_1
	push	{r4, r5, r7, lr}
	add	r7, sp, #8
	ldr.w	lr, [r7, #8]
	clz	r4, r3
	lsr.w	r12, r4, #5
	cmp.w	lr, #0
	mov	r4, lr
	it	ne
	movne	r4, #1
	tst.w	r12, r4
	mov.w	r12, #0
	bne	LBB2_7
; %bb.2:
	cbz	r1, LBB2_7
; %bb.3:
	movs	r4, #0
	b	LBB2_5
                ALIGN   2
LBB2_4                                ;   in Loop: Header=BB2_5 Depth=1
	adds	r4, #1
	cmp	r1, r4
	beq	LBB2_7
LBB2_5                                ; =>This Inner Loop Header: Depth=1
	ldr.w	r5, [r0, r4, lsl #2]
	cmp	r5, r2
	bne	LBB2_4
; %bb.6:                                ;   in Loop: Header=BB2_5 Depth=1
	cmp	r12, lr
	it	lo
	strlo.w	r4, [r3, r12, lsl #2]
	add.w	r12, r12, #1
	b	LBB2_4
LBB2_7
	pop.w	{r4, r5, r7, lr}
	mov	r0, r12
	bx	lr
Lfunc_end2
                                        ; -- End function

                END
