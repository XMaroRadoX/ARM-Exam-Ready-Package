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
	.globl	pat_alg_knapsack_001            @ -- Begin function pat_alg_knapsack_001
	.p2align	2
	.type	pat_alg_knapsack_001,%function
	.code	16                              @ @pat_alg_knapsack_001
	.thumb_func
pat_alg_knapsack_001:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r10}
	push.w	{r8, r9, r10}
	ldr.w	lr, [r7, #8]
	mov.w	r12, #0
	cmp.w	lr, #0
	beq	.LBB0_13
@ %bb.1:
	cmp	r2, #0
	mov	r4, r2
	it	ne
	movne	r4, #1
	cmp.w	r12, r2, lsr #16
	bne	.LBB0_13
@ %bb.2:
	clz	r5, r0
	clz	r6, r1
	lsrs	r5, r5, #5
	lsrs	r6, r6, #5
	orrs	r5, r6
	ands	r4, r5
	bne	.LBB0_13
@ %bb.3:
	movw	r4, #65534
	movt	r4, #16383
	cmp	r3, r4
	bhi	.LBB0_13
@ %bb.4:
	sub.w	r6, lr, #4
	mov.w	r5, #-1
	movs	r4, #0
	.p2align	2
.LBB0_5:                                @ =>This Inner Loop Header: Depth=1
	adds	r5, #1
	cmp	r3, r5
	str	r4, [r6, #4]!
	bne	.LBB0_5
@ %bb.6:
	cbz	r2, .LBB0_12
@ %bb.7:
	mov.w	r12, #0
	b	.LBB0_9
	.p2align	2
.LBB0_8:                                @   in Loop: Header=BB0_9 Depth=1
	add.w	r12, r12, #1
	cmp	r12, r2
	beq	.LBB0_12
.LBB0_9:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_11 Depth 2
	ldrh.w	r9, [r0, r12, lsl #1]
	cmp	r9, r3
	bhi	.LBB0_8
@ %bb.10:                               @   in Loop: Header=BB0_9 Depth=1
	ldrh.w	r8, [r1, r12, lsl #1]
	sub.w	r10, lr, r9, lsl #2
	mov	r5, r3
	.p2align	2
.LBB0_11:                               @   Parent Loop BB0_9 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldr.w	r4, [r10, r5, lsl #2]
	ldr.w	r6, [lr, r5, lsl #2]
	add	r4, r8
	cmp	r4, r6
	it	hi
	strhi.w	r4, [lr, r5, lsl #2]
	cmp	r5, r9
	sub.w	r5, r5, #1
	bhi	.LBB0_11
	b	.LBB0_8
.LBB0_12:
	ldr.w	r12, [lr, r3, lsl #2]
.LBB0_13:
	mov	r0, r12
	pop.w	{r8, r9, r10}
	pop	{r4, r5, r6, r7, pc}
.Lfunc_end0:
	.size	pat_alg_knapsack_001, .Lfunc_end0-pat_alg_knapsack_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
