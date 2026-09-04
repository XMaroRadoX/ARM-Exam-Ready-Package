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
	.globl	pat_alg_selection_sort_001      @ -- Begin function pat_alg_selection_sort_001
	.p2align	2
	.type	pat_alg_selection_sort_001,%function
	.code	16                              @ @pat_alg_selection_sort_001
	.thumb_func
pat_alg_selection_sort_001:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	it	ne
	cmpne	r1, #0
	bne	.LBB0_2
@ %bb.1:
	bx	lr
.LBB0_2:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8}
	str	r8, [sp, #-4]!
	rsb.w	r8, r1, #0
	adds	r3, r0, #4
	mov.w	r12, #0
	b	.LBB0_4
	.p2align	2
.LBB0_3:                                @   in Loop: Header=BB0_4 Depth=1
	cmp	lr, r1
	mov	r12, lr
	beq	.LBB0_9
.LBB0_4:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_6 Depth 2
	add.w	lr, r12, #1
	cmp	lr, r1
	mov	r4, r12
	bhs	.LBB0_7
@ %bb.5:                                @   in Loop: Header=BB0_4 Depth=1
	mov	r5, r12
	mov	r4, r12
	.p2align	2
.LBB0_6:                                @   Parent Loop BB0_4 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldr.w	r6, [r3, r5, lsl #2]
	ldr.w	r2, [r0, r4, lsl #2]
	adds	r5, #1
	cmp	r6, r2
	add.w	r2, r8, r5
	it	lt
	movlt	r4, r5
	adds	r2, #1
	bne	.LBB0_6
.LBB0_7:                                @   in Loop: Header=BB0_4 Depth=1
	cmp	r4, r12
	beq	.LBB0_3
@ %bb.8:                                @   in Loop: Header=BB0_4 Depth=1
	ldr.w	r2, [r0, r4, lsl #2]
	ldr.w	r5, [r0, r12, lsl #2]
	str.w	r2, [r0, r12, lsl #2]
	str.w	r5, [r0, r4, lsl #2]
	b	.LBB0_3
.LBB0_9:
	ldr	r8, [sp], #4
	pop.w	{r4, r5, r6, r7, lr}
	bx	lr
.Lfunc_end0:
	.size	pat_alg_selection_sort_001, .Lfunc_end0-pat_alg_selection_sort_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
