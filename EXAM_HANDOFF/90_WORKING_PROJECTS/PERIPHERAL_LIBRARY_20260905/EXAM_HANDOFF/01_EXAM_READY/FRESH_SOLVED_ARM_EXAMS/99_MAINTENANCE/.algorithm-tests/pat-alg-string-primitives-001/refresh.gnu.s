	.text
	.syntax unified
	.eabi_attribute	67, "2.09"	@ Tag_conformance
	.cpu	cortex-m3
	.eabi_attribute	6, 10	@ Tag_CPU_arch
	.eabi_attribute	7, 77	@ Tag_CPU_arch_profile
	.eabi_attribute	8, 0	@ Tag_ARM_ISA_use
	.eabi_attribute	9, 2	@ Tag_THUMB_ISA_use
	.eabi_attribute	34, 1	@ Tag_CPU_unaligned_access
	.eabi_attribute	17, 1	@ Tag_ABI_PCS_GOT_use
	.eabi_attribute	20, 1	@ Tag_ABI_FP_denormal
	.eabi_attribute	21, 0	@ Tag_ABI_FP_exceptions
	.eabi_attribute	23, 3	@ Tag_ABI_FP_number_model
	.eabi_attribute	24, 1	@ Tag_ABI_align_needed
	.eabi_attribute	25, 1	@ Tag_ABI_align_preserved
	.eabi_attribute	38, 1	@ Tag_ABI_FP_16bit_format
	.eabi_attribute	18, 4	@ Tag_ABI_PCS_wchar_t
	.eabi_attribute	26, 2	@ Tag_ABI_enum_size
	.eabi_attribute	14, 0	@ Tag_ABI_PCS_R9_use
	.file	"reference.c"
	.globl	pat_alg_string_primitives_001_length @ -- Begin function pat_alg_string_primitives_001_length
	.p2align	2
	.type	pat_alg_string_primitives_001_length,%function
	.code	16                              @ @pat_alg_string_primitives_001_length
	.thumb_func
pat_alg_string_primitives_001_length:
	.fnstart
@ %bb.0:
	mov	r2, r0
	cmp	r0, #0
	mov.w	r0, #0
	it	ne
	cmpne	r1, #0
	bne	.LBB0_2
@ %bb.1:
	bx	lr
	.p2align	2
.LBB0_2:                                @ =>This Inner Loop Header: Depth=1
	ldrb	r3, [r2, r0]
	cmp	r3, #0
	it	eq
	bxeq	lr
.LBB0_3:                                @   in Loop: Header=BB0_2 Depth=1
	adds	r0, #1
	cmp	r1, r0
	bne	.LBB0_2
@ %bb.4:
	mov	r0, r1
	bx	lr
.Lfunc_end0:
	.size	pat_alg_string_primitives_001_length, .Lfunc_end0-pat_alg_string_primitives_001_length
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_string_primitives_001_compare @ -- Begin function pat_alg_string_primitives_001_compare
	.p2align	2
	.type	pat_alg_string_primitives_001_compare,%function
	.code	16                              @ @pat_alg_string_primitives_001_compare
	.thumb_func
pat_alg_string_primitives_001_compare:
	.fnstart
@ %bb.0:
	mov	r12, r0
	cmp	r0, #0
	mov.w	r0, #0
	it	ne
	cmpne	r1, #0
	bne	.LBB1_2
@ %bb.1:
	bx	lr
.LBB1_2:
	cmp	r2, #0
	it	eq
	bxeq	lr
.LBB1_3:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
                                        @ implicit-def: $r0
	.p2align	2
.LBB1_4:                                @ =>This Inner Loop Header: Depth=1
	ldrb	r3, [r12], #1
	ldrb	lr, [r1], #1
	cmp	r3, #0
	sub.w	lr, r3, lr
	clz	r4, lr
	it	ne
	movne	r3, #1
	lsrs	r4, r4, #5
	ands	r3, r4
	it	eq
	moveq	r0, lr
	beq	.LBB1_7
@ %bb.5:                                @   in Loop: Header=BB1_4 Depth=1
	subs	r2, #1
	bne	.LBB1_4
@ %bb.6:
	movs	r0, #0
.LBB1_7:
	pop.w	{r4, r6, r7, lr}
	bx	lr
.Lfunc_end1:
	.size	pat_alg_string_primitives_001_compare, .Lfunc_end1-pat_alg_string_primitives_001_compare
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_string_primitives_001_copy @ -- Begin function pat_alg_string_primitives_001_copy
	.p2align	2
	.type	pat_alg_string_primitives_001_copy,%function
	.code	16                              @ @pat_alg_string_primitives_001_copy
	.thumb_func
pat_alg_string_primitives_001_copy:
	.fnstart
@ %bb.0:
	cmp	r1, #0
	mov.w	r3, #0
	it	ne
	cmpne	r0, #0
	bne	.LBB2_2
.LBB2_1:
	mov	r0, r3
	bx	lr
.LBB2_2:
	cmp	r2, #0
	beq	.LBB2_1
@ %bb.3:
	mov.w	r12, #0
	cmp	r1, #2
	blo	.LBB2_8
@ %bb.4:
	.save	{r7, lr}
	push	{r7, lr}
	.setfp	r7, sp
	mov	r7, sp
	sub.w	lr, r1, #1
	movs	r3, #0
	.p2align	2
.LBB2_5:                                @ =>This Inner Loop Header: Depth=1
	ldrb	r1, [r2, r3]
	cbz	r1, .LBB2_7
@ %bb.6:                                @   in Loop: Header=BB2_5 Depth=1
	strb	r1, [r0, r3]
	adds	r3, #1
	cmp	lr, r3
	bne	.LBB2_5
.LBB2_7:
	pop.w	{r7, lr}
.LBB2_8:
	strb.w	r12, [r0, r3]
	mov	r0, r3
	bx	lr
.Lfunc_end2:
	.size	pat_alg_string_primitives_001_copy, .Lfunc_end2-pat_alg_string_primitives_001_copy
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_string_primitives_001   @ -- Begin function pat_alg_string_primitives_001
	.p2align	2
	.type	pat_alg_string_primitives_001,%function
	.code	16                              @ @pat_alg_string_primitives_001
	.thumb_func
pat_alg_string_primitives_001:
	.fnstart
@ %bb.0:
	mov	r12, r0
	cmp	r0, #0
	mov.w	r0, #-1
	it	ne
	cmpne	r1, #0
	bne	.LBB3_2
@ %bb.1:
	bx	lr
.LBB3_2:
	ldrb	r0, [r1]
	cbz	r0, .LBB3_15
@ %bb.3:
	cmp	r2, #0
	itt	eq
	moveq.w	r0, #-1
	bxeq	lr
.LBB3_4:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8}
	str	r8, [sp, #-4]!
	add.w	lr, r1, #1
	movs	r0, #0
	mov	r8, r12
	.p2align	2
.LBB3_5:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB3_8 Depth 2
	ldrb.w	r3, [r12, r0]
	cbz	r3, .LBB3_13
@ %bb.6:                                @   in Loop: Header=BB3_5 Depth=1
	ldrb	r4, [r1]
	cbz	r4, .LBB3_11
@ %bb.7:                                @   in Loop: Header=BB3_5 Depth=1
	subs	r5, r2, r0
	movs	r3, #0
	.p2align	2
.LBB3_8:                                @   Parent Loop BB3_5 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldrb.w	r6, [r8, r3]
	cmp	r6, r4
	bne	.LBB3_11
@ %bb.9:                                @   in Loop: Header=BB3_8 Depth=2
	adds	r6, r3, #1
	ldrb.w	r4, [lr, r3]
	cmp	r6, r5
	bhs	.LBB3_11
@ %bb.10:                               @   in Loop: Header=BB3_8 Depth=2
	cmp	r4, #0
	mov	r3, r6
	bne	.LBB3_8
	.p2align	2
.LBB3_11:                               @   in Loop: Header=BB3_5 Depth=1
	cbz	r4, .LBB3_14
@ %bb.12:                               @   in Loop: Header=BB3_5 Depth=1
	adds	r0, #1
	cmp	r0, r2
	add.w	r8, r8, #1
	bne	.LBB3_5
.LBB3_13:
	mov.w	r0, #-1
.LBB3_14:
	ldr	r8, [sp], #4
	pop	{r4, r5, r6, r7, pc}
.LBB3_15:
	movs	r0, #0
	bx	lr
.Lfunc_end3:
	.size	pat_alg_string_primitives_001, .Lfunc_end3-pat_alg_string_primitives_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
