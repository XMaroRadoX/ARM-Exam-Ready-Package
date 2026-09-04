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
	.globl	pat_alg_bubble_sort_001         @ -- Begin function pat_alg_bubble_sort_001
	.p2align	2
	.type	pat_alg_bubble_sort_001,%function
	.code	16                              @ @pat_alg_bubble_sort_001
	.thumb_func
pat_alg_bubble_sort_001:
	.fnstart
@ %bb.0:
	cbz	r0, .LBB0_7
@ %bb.1:
	cmp	r1, #2
	it	lo
	bxlo	lr
.LBB0_2:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	.p2align	2
.LBB0_3:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_4 Depth 2
	subs	r1, #1
	movs	r2, #0
	mov.w	r12, #0
	.p2align	2
.LBB0_4:                                @   Parent Loop BB0_3 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	add.w	lr, r0, r2, lsl #2
	ldr.w	r3, [r0, r2, lsl #2]
	ldr.w	r4, [lr, #4]
	adds	r2, #1
	cmp	r3, r4
	itt	gt
	strdgt	r4, r3, [lr]
	movgt.w	r12, #1
	cmp	r1, r2
	bne	.LBB0_4
@ %bb.5:                                @   in Loop: Header=BB0_3 Depth=1
	cmp.w	r12, #0
	it	ne
	cmpne	r1, #1
	bhi	.LBB0_3
@ %bb.6:
	pop.w	{r4, r6, r7, lr}
.LBB0_7:
	bx	lr
.Lfunc_end0:
	.size	pat_alg_bubble_sort_001, .Lfunc_end0-pat_alg_bubble_sort_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
