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
	.globl	pat_alg_prefix_sum_001          @ -- Begin function pat_alg_prefix_sum_001
	.p2align	2
	.type	pat_alg_prefix_sum_001,%function
	.code	16                              @ @pat_alg_prefix_sum_001
	.thumb_func
pat_alg_prefix_sum_001:
	.fnstart
@ %bb.0:
	cmp	r2, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
.LBB0_1:
	.save	{r7, lr}
	push	{r7, lr}
	.setfp	r7, sp
	mov	r7, sp
	movw	r3, #65534
	cmp	r1, #0
	mov	lr, r1
	movt	r3, #8191
	it	ne
	movne.w	lr, #1
	cmp	r1, r3
	mov.w	r12, #0
	bhi	.LBB0_7
@ %bb.2:
	clz	r3, r0
	lsrs	r3, r3, #5
	ands.w	r3, r3, lr
	bne	.LBB0_7
@ %bb.3:
	movs	r3, #0
	str	r3, [r2]
	str	r3, [r2, #4]
	cbz	r1, .LBB0_6
@ %bb.4:
	ldrd	r3, r12, [r2], #-8
	sub.w	lr, r0, #4
	.p2align	2
.LBB0_5:                                @ =>This Inner Loop Header: Depth=1
	ldr	r0, [lr, #4]!
	adds	r3, r3, r0
	adc.w	r12, r12, r0, asr #31
	strd	r3, r12, [r2, #16]
	subs	r1, #1
	add.w	r2, r2, #8
	bne	.LBB0_5
.LBB0_6:
	mov.w	r12, #1
.LBB0_7:
	pop.w	{r7, lr}
	mov	r0, r12
	bx	lr
.Lfunc_end0:
	.size	pat_alg_prefix_sum_001, .Lfunc_end0-pat_alg_prefix_sum_001
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_prefix_sum_001_range    @ -- Begin function pat_alg_prefix_sum_001_range
	.p2align	2
	.type	pat_alg_prefix_sum_001_range,%function
	.code	16                              @ @pat_alg_prefix_sum_001_range
	.thumb_func
pat_alg_prefix_sum_001_range:
	.fnstart
@ %bb.0:
	mov	r12, r0
	cmp	r3, r1
	mov.w	r0, #0
	it	ls
	cmpls	r2, r3
	bls	.LBB1_2
@ %bb.1:
	bx	lr
.LBB1_2:
	cmp.w	r12, #0
	it	eq
	bxeq	lr
.LBB1_3:
	.save	{r7, lr}
	push	{r7, lr}
	.setfp	r7, sp
	mov	r7, sp
	ldr.w	lr, [r7, #8]
	cmp.w	lr, #0
	beq	.LBB1_5
@ %bb.4:
	add.w	r0, r12, r3, lsl #3
	ldr.w	r3, [r12, r3, lsl #3]
	add.w	r1, r12, r2, lsl #3
	ldr.w	r2, [r12, r2, lsl #3]
	ldr	r0, [r0, #4]
	ldr	r1, [r1, #4]
	subs	r2, r3, r2
	sbcs	r0, r1
	strd	r2, r0, [lr]
	movs	r0, #1
.LBB1_5:
	pop.w	{r7, lr}
	bx	lr
.Lfunc_end1:
	.size	pat_alg_prefix_sum_001_range, .Lfunc_end1-pat_alg_prefix_sum_001_range
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
