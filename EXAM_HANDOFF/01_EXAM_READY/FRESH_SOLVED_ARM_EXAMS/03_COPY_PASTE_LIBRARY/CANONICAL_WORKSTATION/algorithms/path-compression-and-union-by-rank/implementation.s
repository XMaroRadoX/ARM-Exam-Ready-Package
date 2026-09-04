; Matching Cortex-M3 Thumb implementation generated from reference.c.

                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  find
                EXPORT  algorithm_path_compression_and_union_by_rank

                ALIGN   2
find
; %bb.0:
	ldr.w	r2, [r0, r1, lsl #2]
	cmp	r2, r1
	beq	LBB0_3
; %bb.1:
	add.w	r3, r0, r1, lsl #2
                ALIGN   2
LBB0_2                                ; =>This Inner Loop Header: Depth=1
	ldr.w	r1, [r0, r2, lsl #2]
	str	r1, [r3]
	ldr.w	r2, [r0, r1, lsl #2]
	add.w	r3, r0, r1, lsl #2
	cmp	r2, r1
	bne	LBB0_2
LBB0_3
	mov	r0, r1
	bx	lr
Lfunc_end0
                                        ; -- End function
                ALIGN   2
algorithm_path_compression_and_union_by_rank
; %bb.0:
	cmp	r0, #0
	mov.w	r12, #0
	it	ne
	cmpne	r1, #0
	bne	LBB1_2
LBB1_1
	mov	r0, r12
	bx	lr
LBB1_2
	cmp	r3, r2
	bhs	LBB1_1
; %bb.3:
	push	{r7, lr}
	mov	r7, sp
	ldr.w	lr, [r7, #8]
	cmp	lr, r2
	bhs	LBB1_16
; %bb.4:
	ldr.w	r2, [r0, r3, lsl #2]
	cmp	r2, r3
	beq	LBB1_7
; %bb.5:
	add.w	r12, r0, r3, lsl #2
                ALIGN   2
LBB1_6                                ; =>This Inner Loop Header: Depth=1
	ldr.w	r3, [r0, r2, lsl #2]
	str.w	r3, [r12]
	ldr.w	r2, [r0, r3, lsl #2]
	add.w	r12, r0, r3, lsl #2
	cmp	r2, r3
	bne	LBB1_6
LBB1_7
	ldr.w	r2, [r0, lr, lsl #2]
	cmp	r2, lr
	beq	LBB1_10
; %bb.8:
	add.w	r12, r0, lr, lsl #2
                ALIGN   2
LBB1_9                                ; =>This Inner Loop Header: Depth=1
	ldr.w	lr, [r0, r2, lsl #2]
	str.w	lr, [r12]
	ldr.w	r2, [r0, lr, lsl #2]
	add.w	r12, r0, lr, lsl #2
	cmp	r2, lr
	bne	LBB1_9
LBB1_10
	cmp	r3, lr
	beq	LBB1_15
; %bb.11:
	ldrb.w	r12, [r1, r3]
	ldrb.w	r2, [r1, lr]
	cmp	r12, r2
	bhs	LBB1_13
; %bb.12:
	str.w	lr, [r0, r3, lsl #2]
	b	LBB1_15
LBB1_13
	cmp	r12, r2
	str.w	r3, [r0, lr, lsl #2]
	bhi	LBB1_15
; %bb.14:
	ldrb	r0, [r1, r3]
	adds	r0, #1
	strb	r0, [r1, r3]
LBB1_15
	mov.w	r12, #1
LBB1_16
	pop.w	{r7, lr}
	mov	r0, r12
	bx	lr
Lfunc_end1
                                        ; -- End function

                END
