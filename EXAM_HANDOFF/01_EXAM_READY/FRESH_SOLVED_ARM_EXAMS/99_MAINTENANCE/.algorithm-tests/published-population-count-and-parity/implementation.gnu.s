.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_population_count_and_parity
.global algorithm_population_count_and_parity_parity
.balign 4
algorithm_population_count_and_parity:
	cmp	r0, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB0_1:
	mov	r1, r0
	movs	r0, #0
.balign 4
LBB0_2:
	subs	r2, r1, #1
	ands	r1, r2
	add.w	r0, r0, #1
	bne	LBB0_2
	bx	lr
Lfunc_end0:
.balign 4
algorithm_population_count_and_parity_parity:
	cmp	r0, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB1_1:
	movs	r1, #0
.balign 4
LBB1_2:
	subs	r2, r0, #1
	ands	r0, r2
	add.w	r1, r1, #1
	bne	LBB1_2
	and	r0, r1, #1
	bx	lr
Lfunc_end1:
