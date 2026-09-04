; Matching Cortex-M3 Thumb implementation generated from reference.c.

                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  algorithm_parity_from_population_count
                EXPORT  algorithm_parity_from_population_count_parity

                ALIGN   2
algorithm_parity_from_population_count
; %bb.0:
	cmp	r0, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB0_1
	mov	r1, r0
	movs	r0, #0
                ALIGN   2
LBB0_2                                ; =>This Inner Loop Header: Depth=1
	subs	r2, r1, #1
	ands	r1, r2
	add.w	r0, r0, #1
	bne	LBB0_2
; %bb.3:
	bx	lr
Lfunc_end0
                                        ; -- End function
                ALIGN   2
algorithm_parity_from_population_count_parity
; %bb.0:
	cmp	r0, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB1_1
	movs	r1, #0
                ALIGN   2
LBB1_2                                ; =>This Inner Loop Header: Depth=1
	subs	r2, r0, #1
	ands	r0, r2
	add.w	r1, r1, #1
	bne	LBB1_2
; %bb.3:
	and	r0, r1, #1
	bx	lr
Lfunc_end1
                                        ; -- End function

                END
