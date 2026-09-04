; Matching Cortex-M3 Thumb implementation generated from reference.c.

                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  algorithm_lower_bound_insertion_position
                EXPORT  algorithm_lower_bound_insertion_position_exact

                ALIGN   2
algorithm_lower_bound_insertion_position
; %bb.0:
	cmp	r0, #0
	mov.w	r12, #0
	it	ne
	cmpne	r1, #0
	bne	LBB0_2
; %bb.1:
	mov	r0, r12
	bx	lr
LBB0_2
	push	{r7, lr}
	mov	r7, sp
	mov.w	r12, #0
                ALIGN   2
LBB0_3                                ; =>This Inner Loop Header: Depth=1
	sub.w	r3, r1, r12
	add.w	lr, r12, r3, lsr #1
	ldr.w	r3, [r0, lr, lsl #2]
	cmp	r3, r2
	ite	lt
	addlt.w	r12, lr, #1
	movge	r1, lr
	cmp	r12, r1
	blo	LBB0_3
; %bb.4:
	pop.w	{r7, lr}
	mov	r0, r12
	bx	lr
Lfunc_end0
                                        ; -- End function
                ALIGN   2
algorithm_lower_bound_insertion_position_exact
; %bb.0:
	push	{r4, r6, r7, lr}
	add	r7, sp, #8
	mov	r12, r0
	cmp	r0, #0
	mov.w	r0, #0
	it	ne
	cmpne	r1, #0
	beq	LBB1_3
; %bb.1:
	mov	lr, r1
                ALIGN   2
LBB1_2                                ; =>This Inner Loop Header: Depth=1
	sub.w	r3, lr, r0
	add.w	r3, r0, r3, lsr #1
	ldr.w	r4, [r12, r3, lsl #2]
	cmp	r4, r2
	ite	lt
	addlt	r0, r3, #1
	movge	lr, r3
	cmp	r0, lr
	blo	LBB1_2
LBB1_3
	cmp.w	r12, #0
	beq	LBB1_6
; %bb.4:
	cmp	r0, r1
	bhs	LBB1_6
; %bb.5:
	ldr.w	r1, [r12, r0, lsl #2]
	cmp	r1, r2
	it	ne
	movne.w	r0, #-1
	pop	{r4, r6, r7, pc}
LBB1_6
	mov.w	r0, #-1
	pop	{r4, r6, r7, pc}
Lfunc_end1
                                        ; -- End function

                END
