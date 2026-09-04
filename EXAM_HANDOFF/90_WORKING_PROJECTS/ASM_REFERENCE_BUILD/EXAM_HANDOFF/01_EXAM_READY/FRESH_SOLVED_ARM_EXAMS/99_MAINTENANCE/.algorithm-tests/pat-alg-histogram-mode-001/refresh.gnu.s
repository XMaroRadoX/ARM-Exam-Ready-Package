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
	.globl	pat_alg_histogram_mode_001      @ -- Begin function pat_alg_histogram_mode_001
	.p2align	2
	.type	pat_alg_histogram_mode_001,%function
	.code	16                              @ @pat_alg_histogram_mode_001
	.thumb_func
pat_alg_histogram_mode_001:
	.fnstart
@ %bb.0:
	cmp	r3, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
.LBB0_1:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	clz	r4, r0
	lsr.w	r12, r4, #5
	cmp	r1, #0
	mov	r4, r1
	it	ne
	movne	r4, #1
	tst.w	r12, r4
	mov.w	r12, #0
	bne	.LBB0_14
@ %bb.2:
	subw	r4, r2, #257
	cmn.w	r4, #256
	blo	.LBB0_14
@ %bb.3:
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
	cbnz	r1, .LBB0_11
.LBB0_7:
	cmp	r2, #2
	blo	.LBB0_13
@ %bb.8:
	rsb.w	lr, r2, #0
	adds	r1, r3, #4
	movs	r2, #0
	mov.w	r12, #0
	.p2align	2
.LBB0_9:                                @ =>This Inner Loop Header: Depth=1
	ldr.w	r4, [r1, r2, lsl #2]
	ldr.w	r0, [r3, r12, lsl #2]
	adds	r2, #1
	cmp	r4, r0
	add.w	r0, lr, r2
	it	hi
	movhi	r12, r2
	adds	r0, #1
	bne	.LBB0_9
	b	.LBB0_14
	.p2align	2
.LBB0_10:                               @   in Loop: Header=BB0_11 Depth=1
	subs	r1, #1
	beq	.LBB0_7
.LBB0_11:                               @ =>This Inner Loop Header: Depth=1
	ldrb	r12, [r0], #1
	cmp	r12, r2
	bhs	.LBB0_10
@ %bb.12:                               @   in Loop: Header=BB0_11 Depth=1
	ldr.w	r4, [r3, r12, lsl #2]
	adds	r4, #1
	str.w	r4, [r3, r12, lsl #2]
	b	.LBB0_10
.LBB0_13:
	mov.w	r12, #0
.LBB0_14:
	pop.w	{r4, r6, r7, lr}
	mov	r0, r12
	bx	lr
.Lfunc_end0:
	.size	pat_alg_histogram_mode_001, .Lfunc_end0-pat_alg_histogram_mode_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
