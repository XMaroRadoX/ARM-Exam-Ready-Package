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
	.globl	pat_alg_memmove_001             @ -- Begin function pat_alg_memmove_001
	.p2align	2
	.type	pat_alg_memmove_001,%function
	.code	16                              @ @pat_alg_memmove_001
	.thumb_func
pat_alg_memmove_001:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	it	ne
	cmpne	r1, #0
	bne	.LBB0_2
.LBB0_1:
	bx	lr
.LBB0_2:
	cmp	r0, r1
	bhs	.LBB0_6
@ %bb.3:
	cmp	r2, #0
	beq	.LBB0_1
@ %bb.4:
	subs	r3, r0, #1
	subs	r1, #1
	.p2align	2
.LBB0_5:                                @ =>This Inner Loop Header: Depth=1
	ldrb	r12, [r1, #1]!
	subs	r2, #1
	strb	r12, [r3, #1]!
	bne	.LBB0_5
	b	.LBB0_1
.LBB0_6:
	bls	.LBB0_1
@ %bb.7:
	cmp	r2, #0
	it	eq
	bxeq	lr
.LBB0_8:
	sub.w	r12, r0, #1
	subs	r1, #1
	.p2align	2
.LBB0_9:                                @ =>This Inner Loop Header: Depth=1
	ldrb	r3, [r1, r2]
	strb.w	r3, [r12, r2]
	subs	r2, #1
	bne	.LBB0_9
	b	.LBB0_1
.Lfunc_end0:
	.size	pat_alg_memmove_001, .Lfunc_end0-pat_alg_memmove_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
