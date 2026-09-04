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
	.globl	pat_alg_array_rotation_001      @ -- Begin function pat_alg_array_rotation_001
	.p2align	2
	.type	pat_alg_array_rotation_001,%function
	.code	16                              @ @pat_alg_array_rotation_001
	.thumb_func
pat_alg_array_rotation_001:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	beq	.LBB0_13
@ %bb.1:
	cmp	r1, #2
	it	lo
	bxlo	lr
.LBB0_2:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	udiv	r3, r2, r1
	mls	lr, r3, r1, r2
	cmp.w	lr, #0
	beq	.LBB0_12
@ %bb.3:
	subs.w	r3, lr, #1
	beq	.LBB0_6
@ %bb.4:
	movs	r2, #0
	.p2align	2
.LBB0_5:                                @ =>This Inner Loop Header: Depth=1
	ldr.w	r12, [r0, r3, lsl #2]
	ldr.w	r4, [r0, r2, lsl #2]
	str.w	r12, [r0, r2, lsl #2]
	str.w	r4, [r0, r3, lsl #2]
	adds	r2, #1
	subs	r3, #1
	cmp	r2, r3
	blo	.LBB0_5
.LBB0_6:
	subs	r3, r1, #1
	cmp	lr, r3
	bhs	.LBB0_9
@ %bb.7:
	sub.w	r12, r0, #4
	.p2align	2
.LBB0_8:                                @ =>This Inner Loop Header: Depth=1
	ldr.w	r2, [r12, r1, lsl #2]
	ldr.w	r4, [r0, lr, lsl #2]
	str.w	r2, [r0, lr, lsl #2]
	add.w	lr, lr, #1
	subs	r2, r1, #2
	str.w	r4, [r12, r1, lsl #2]
	subs	r1, #1
	cmp	lr, r2
	blo	.LBB0_8
.LBB0_9:
	cbz	r3, .LBB0_12
@ %bb.10:
	movs	r1, #0
	.p2align	2
.LBB0_11:                               @ =>This Inner Loop Header: Depth=1
	ldr.w	r2, [r0, r3, lsl #2]
	ldr.w	r4, [r0, r1, lsl #2]
	str.w	r2, [r0, r1, lsl #2]
	str.w	r4, [r0, r3, lsl #2]
	adds	r1, #1
	subs	r3, #1
	cmp	r1, r3
	blo	.LBB0_11
.LBB0_12:
	pop.w	{r4, r6, r7, lr}
.LBB0_13:
	bx	lr
.Lfunc_end0:
	.size	pat_alg_array_rotation_001, .Lfunc_end0-pat_alg_array_rotation_001
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_array_rotation_001_right @ -- Begin function pat_alg_array_rotation_001_right
	.p2align	2
	.type	pat_alg_array_rotation_001_right,%function
	.code	16                              @ @pat_alg_array_rotation_001_right
	.thumb_func
pat_alg_array_rotation_001_right:
	.fnstart
@ %bb.0:
	cmp	r1, #0
	it	eq
	bxeq	lr
.LBB1_1:
	cmp	r0, #0
	it	ne
	cmpne	r1, #1
	bne	.LBB1_3
@ %bb.2:
	bx	lr
.LBB1_3:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	udiv	r3, r2, r1
	muls	r3, r1, r3
	subs	r2, r3, r2
	add	r2, r1
	udiv	r3, r2, r1
	mls	lr, r3, r1, r2
	cmp.w	lr, #0
	beq	.LBB1_13
@ %bb.4:
	subs.w	r3, lr, #1
	beq	.LBB1_7
@ %bb.5:
	movs	r2, #0
	.p2align	2
.LBB1_6:                                @ =>This Inner Loop Header: Depth=1
	ldr.w	r12, [r0, r3, lsl #2]
	ldr.w	r4, [r0, r2, lsl #2]
	str.w	r12, [r0, r2, lsl #2]
	str.w	r4, [r0, r3, lsl #2]
	adds	r2, #1
	subs	r3, #1
	cmp	r2, r3
	blo	.LBB1_6
.LBB1_7:
	subs	r3, r1, #1
	cmp	lr, r3
	bhs	.LBB1_10
@ %bb.8:
	sub.w	r12, r0, #4
	.p2align	2
.LBB1_9:                                @ =>This Inner Loop Header: Depth=1
	ldr.w	r2, [r12, r1, lsl #2]
	ldr.w	r4, [r0, lr, lsl #2]
	str.w	r2, [r0, lr, lsl #2]
	add.w	lr, lr, #1
	subs	r2, r1, #2
	str.w	r4, [r12, r1, lsl #2]
	subs	r1, #1
	cmp	lr, r2
	blo	.LBB1_9
.LBB1_10:
	cbz	r3, .LBB1_13
@ %bb.11:
	movs	r1, #0
	.p2align	2
.LBB1_12:                               @ =>This Inner Loop Header: Depth=1
	ldr.w	r2, [r0, r3, lsl #2]
	ldr.w	r4, [r0, r1, lsl #2]
	str.w	r2, [r0, r1, lsl #2]
	str.w	r4, [r0, r3, lsl #2]
	adds	r1, #1
	subs	r3, #1
	cmp	r1, r3
	blo	.LBB1_12
.LBB1_13:
	pop.w	{r4, r6, r7, lr}
	bx	lr
.Lfunc_end1:
	.size	pat_alg_array_rotation_001_right, .Lfunc_end1-pat_alg_array_rotation_001_right
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_array_rotation_001_with_scratch @ -- Begin function pat_alg_array_rotation_001_with_scratch
	.p2align	2
	.type	pat_alg_array_rotation_001_with_scratch,%function
	.code	16                              @ @pat_alg_array_rotation_001_with_scratch
	.thumb_func
pat_alg_array_rotation_001_with_scratch:
	.fnstart
@ %bb.0:
	cmp	r0, r3
	mov.w	r12, #0
	it	ne
	cmpne	r0, #0
	bne	.LBB2_2
.LBB2_1:
	mov	r0, r12
	bx	lr
.LBB2_2:
	cmp	r3, #0
	beq	.LBB2_1
@ %bb.3:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	ldr.w	lr, [r7, #8]
	cmp	lr, r1
	blo	.LBB2_10
@ %bb.4:
	cbz	r1, .LBB2_9
@ %bb.5:
	udiv	r12, r2, r1
	mls	r12, r12, r1, r2
	movs	r2, #0
	sub.w	lr, r1, r12
	.p2align	2
.LBB2_6:                                @ =>This Inner Loop Header: Depth=1
	mov	r4, r12
	cmp	r2, lr
	it	hs
	rsbhs.w	r4, lr, #0
	add.w	r4, r0, r4, lsl #2
	ldr.w	r4, [r4, r2, lsl #2]
	str.w	r4, [r3, r2, lsl #2]
	adds	r2, #1
	cmp	r1, r2
	bne	.LBB2_6
@ %bb.7:
	subs	r0, #4
	subs	r2, r3, #4
	.p2align	2
.LBB2_8:                                @ =>This Inner Loop Header: Depth=1
	ldr	r3, [r2, #4]!
	subs	r1, #1
	str	r3, [r0, #4]!
	bne	.LBB2_8
.LBB2_9:
	mov.w	r12, #1
.LBB2_10:
	pop.w	{r4, r6, r7, lr}
	mov	r0, r12
	bx	lr
.Lfunc_end2:
	.size	pat_alg_array_rotation_001_with_scratch, .Lfunc_end2-pat_alg_array_rotation_001_with_scratch
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
