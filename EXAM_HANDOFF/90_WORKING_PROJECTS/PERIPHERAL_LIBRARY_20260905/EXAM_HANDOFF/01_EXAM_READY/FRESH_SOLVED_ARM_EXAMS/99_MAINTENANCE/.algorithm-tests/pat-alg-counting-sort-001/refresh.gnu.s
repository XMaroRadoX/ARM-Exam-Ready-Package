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
	.globl	pat_alg_counting_sort_001       @ -- Begin function pat_alg_counting_sort_001
	.p2align	2
	.type	pat_alg_counting_sort_001,%function
	.code	16                              @ @pat_alg_counting_sort_001
	.thumb_func
pat_alg_counting_sort_001:
	.fnstart
@ %bb.0:
	cmp.w	r2, #256
	mov.w	r12, #0
	bhi	.LBB0_19
@ %bb.1:
	cmp	r0, #0
	beq	.LBB0_19
@ %bb.2:
	cmp	r3, #0
	beq	.LBB0_19
@ %bb.3:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	cbz	r2, .LBB0_6
@ %bb.4:
	sub.w	r12, r3, #4
	mov.w	lr, #0
	mov	r4, r2
	.p2align	2
.LBB0_5:                                @ =>This Inner Loop Header: Depth=1
	subs	r4, #1
	str	lr, [r12, #4]!
	bne	.LBB0_5
.LBB0_6:
	cbz	r1, .LBB0_10
@ %bb.7:
	mov	r12, r0
	.p2align	2
.LBB0_8:                                @ =>This Inner Loop Header: Depth=1
	ldrb	lr, [r12], #1
	cmp	lr, r2
	bhs	.LBB0_17
@ %bb.9:                                @   in Loop: Header=BB0_8 Depth=1
	ldr.w	r4, [r3, lr, lsl #2]
	subs	r1, #1
	add.w	r4, r4, #1
	str.w	r4, [r3, lr, lsl #2]
	bne	.LBB0_8
.LBB0_10:
	cbz	r2, .LBB0_16
@ %bb.11:
	mov.w	lr, #0
	mov.w	r12, #0
	b	.LBB0_14
	.p2align	2
.LBB0_12:                               @   in Loop: Header=BB0_14 Depth=1
	mov	r4, lr
.LBB0_13:                               @   in Loop: Header=BB0_14 Depth=1
	add.w	r12, r12, #1
	cmp	r12, r2
	mov	lr, r4
	beq	.LBB0_16
.LBB0_14:                               @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_15 Depth 2
	ldr.w	r1, [r3, r12, lsl #2]
	cmp	r1, #0
	beq	.LBB0_12
	.p2align	2
.LBB0_15:                               @   Parent Loop BB0_14 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	subs	r1, #1
	str.w	r1, [r3, r12, lsl #2]
	strb.w	r12, [r0, lr]
	ldr.w	r1, [r3, r12, lsl #2]
	add.w	r4, lr, #1
	cmp	r1, #0
	mov	lr, r4
	bne	.LBB0_15
	b	.LBB0_13
.LBB0_16:
	mov.w	r12, #1
	b	.LBB0_18
.LBB0_17:
	mov.w	r12, #0
.LBB0_18:
	pop.w	{r4, r6, r7, lr}
.LBB0_19:
	mov	r0, r12
	bx	lr
.Lfunc_end0:
	.size	pat_alg_counting_sort_001, .Lfunc_end0-pat_alg_counting_sort_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
