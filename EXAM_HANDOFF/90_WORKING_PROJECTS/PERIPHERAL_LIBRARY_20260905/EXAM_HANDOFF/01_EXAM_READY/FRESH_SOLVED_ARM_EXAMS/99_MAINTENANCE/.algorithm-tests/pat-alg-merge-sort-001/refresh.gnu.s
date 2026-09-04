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
	.globl	merge                           @ -- Begin function merge
	.p2align	2
	.type	merge,%function
	.code	16                              @ @merge
	.thumb_func
merge:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r11}
	push.w	{r8, r9, r11}
	ldr.w	r12, [r7, #8]
	cmp	r2, r3
	mov	r8, r2
	mov	lr, r3
	mov	r5, r2
	bhs	.LBB0_5
@ %bb.1:
	cmp	r3, r12
	mov	r8, r2
	mov	lr, r3
	mov	r5, r2
	bhs	.LBB0_5
@ %bb.2:
	mov	r5, r2
	mov	lr, r3
	mov	r8, r2
	.p2align	2
.LBB0_3:                                @ =>This Inner Loop Header: Depth=1
	ldr.w	r9, [r0, r8, lsl #2]
	ldr.w	r4, [r0, lr, lsl #2]
	movs	r6, #0
	cmp	r9, r4
	ite	gt
	movgt	r6, #1
	addle.w	r8, r8, #1
	cmp	r9, r4
	add	lr, r6
	it	lt
	movlt	r4, r9
	str.w	r4, [r1, r5, lsl #2]
	cmp	r8, r3
	add.w	r5, r5, #1
	bhs	.LBB0_5
@ %bb.4:                                @   in Loop: Header=BB0_3 Depth=1
	cmp	lr, r12
	blo	.LBB0_3
.LBB0_5:
	cmp	r3, r8
	bls	.LBB0_9
@ %bb.6:
	add.w	r6, r0, r8, lsl #2
	subs	r6, #4
	sub.w	r3, r3, r8
	.p2align	2
.LBB0_7:                                @ =>This Inner Loop Header: Depth=1
	ldr	r8, [r6, #4]!
	adds	r4, r5, #1
	str.w	r8, [r1, r5, lsl #2]
	subs	r3, #1
	mov	r5, r4
	bne	.LBB0_7
@ %bb.8:
	cmp	r12, lr
	bhi	.LBB0_10
	b	.LBB0_12
.LBB0_9:
	mov	r4, r5
	cmp	r12, lr
	bls	.LBB0_12
.LBB0_10:
	add.w	r3, r1, r4, lsl #2
	add.w	r4, r0, lr, lsl #2
	subs	r3, #4
	subs	r4, #4
	sub.w	r6, r12, lr
	.p2align	2
.LBB0_11:                               @ =>This Inner Loop Header: Depth=1
	ldr	r5, [r4, #4]!
	subs	r6, #1
	str	r5, [r3, #4]!
	bne	.LBB0_11
.LBB0_12:
	cmp	r12, r2
	bls	.LBB0_15
@ %bb.13:
	mvn	r6, #3
	sub.w	r3, r12, r2
	add.w	r2, r6, r2, lsl #2
	add	r0, r2
	add	r1, r2
	.p2align	2
.LBB0_14:                               @ =>This Inner Loop Header: Depth=1
	ldr	r2, [r1, #4]!
	subs	r3, #1
	str	r2, [r0, #4]!
	bne	.LBB0_14
.LBB0_15:
	pop.w	{r8, r9, r11}
	pop	{r4, r5, r6, r7, pc}
.Lfunc_end0:
	.size	merge, .Lfunc_end0-merge
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	ms                              @ -- Begin function ms
	.p2align	2
	.type	ms,%function
	.code	16                              @ @ms
	.thumb_func
ms:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r10, r11}
	push.w	{r8, r9, r10, r11}
	.pad	#4
	sub	sp, #4
	subs	r4, r3, r2
	mov	r10, r1
	lsrs	r1, r4, #1
	beq	.LBB1_17
@ %bb.1:
	add.w	r8, r1, r2
	mov	r9, r3
	mov	r1, r10
	mov	r3, r8
	mov	r11, r0
	mov	r5, r2
	bl	ms
	mov	r0, r11
	mov	r1, r10
	mov	r2, r8
	mov	r3, r9
	bl	ms
	mov	r12, r5
	cmp	r8, r5
	bls	.LBB1_10
@ %bb.2:
	cmp	r8, r9
	bhs	.LBB1_10
@ %bb.3:
	mov	r2, r12
	mov	r0, r8
	mov	r1, r12
	.p2align	2
.LBB1_4:                                @ =>This Inner Loop Header: Depth=1
	ldr.w	r3, [r11, r1, lsl #2]
	ldr.w	r6, [r11, r0, lsl #2]
	movs	r5, #0
	cmp	r3, r6
	ite	gt
	movgt	r5, #1
	addle	r1, #1
	cmp	r3, r6
	add	r0, r5
	it	lt
	movlt	r6, r3
	str.w	r6, [r10, r2, lsl #2]
	cmp	r1, r8
	add.w	r2, r2, #1
	bhs	.LBB1_6
@ %bb.5:                                @   in Loop: Header=BB1_4 Depth=1
	cmp	r0, r9
	blo	.LBB1_4
.LBB1_6:
	cmp	r1, r8
	bhs	.LBB1_11
.LBB1_7:
	add.w	r3, r11, r1, lsl #2
	subs	r3, #4
	sub.w	r1, r8, r1
	.p2align	2
.LBB1_8:                                @ =>This Inner Loop Header: Depth=1
	ldr	r6, [r3, #4]!
	adds	r5, r2, #1
	str.w	r6, [r10, r2, lsl #2]
	subs	r1, #1
	mov	r2, r5
	bne	.LBB1_8
@ %bb.9:
	cmp	r9, r0
	bhi	.LBB1_12
	b	.LBB1_14
.LBB1_10:
	mov	r1, r12
	mov	r0, r8
	mov	r2, r12
	cmp	r1, r8
	blo	.LBB1_7
.LBB1_11:
	mov	r5, r2
	cmp	r9, r0
	bls	.LBB1_14
.LBB1_12:
	add.w	r1, r10, r5, lsl #2
	add.w	r2, r11, r0, lsl #2
	subs	r1, #4
	subs	r2, #4
	sub.w	r0, r9, r0
	.p2align	2
.LBB1_13:                               @ =>This Inner Loop Header: Depth=1
	ldr	r3, [r2, #4]!
	subs	r0, #1
	str	r3, [r1, #4]!
	bne	.LBB1_13
.LBB1_14:
	cmp	r9, r12
	bls	.LBB1_17
@ %bb.15:
	mvn	r0, #3
	add.w	r1, r0, r12, lsl #2
	add.w	r0, r11, r1
	add	r1, r10
	.p2align	2
.LBB1_16:                               @ =>This Inner Loop Header: Depth=1
	ldr	r2, [r1, #4]!
	subs	r4, #1
	str	r2, [r0, #4]!
	bne	.LBB1_16
.LBB1_17:
	add	sp, #4
	pop.w	{r8, r9, r10, r11}
	pop	{r4, r5, r6, r7, pc}
.Lfunc_end1:
	.size	ms, .Lfunc_end1-ms
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_merge_sort_001          @ -- Begin function pat_alg_merge_sort_001
	.p2align	2
	.type	pat_alg_merge_sort_001,%function
	.code	16                              @ @pat_alg_merge_sort_001
	.thumb_func
pat_alg_merge_sort_001:
	.fnstart
@ %bb.0:
	cmp	r0, r2
	it	ne
	cmpne	r0, #0
	bne	.LBB2_2
@ %bb.1:
	bx	lr
.LBB2_2:
	cmp	r2, #0
	it	eq
	bxeq	lr
.LBB2_3:
	mov	r3, r1
	mov	r1, r2
	movs	r2, #0
	b	ms
.Lfunc_end2:
	.size	pat_alg_merge_sort_001, .Lfunc_end2-pat_alg_merge_sort_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
