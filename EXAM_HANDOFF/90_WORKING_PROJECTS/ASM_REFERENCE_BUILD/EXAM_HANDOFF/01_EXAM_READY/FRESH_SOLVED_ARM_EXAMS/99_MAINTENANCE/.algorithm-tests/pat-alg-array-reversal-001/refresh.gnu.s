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
	.globl	pat_alg_array_reversal_001      @ -- Begin function pat_alg_array_reversal_001
	.p2align	2
	.type	pat_alg_array_reversal_001,%function
	.code	16                              @ @pat_alg_array_reversal_001
	.thumb_func
pat_alg_array_reversal_001:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	it	ne
	lsrsne.w	r2, r1, #1
	beq	.LBB0_3
@ %bb.1:
	subs	r0, #4
	add.w	r1, r0, r1, lsl #2
	.p2align	2
.LBB0_2:                                @ =>This Inner Loop Header: Depth=1
	ldr	r12, [r0, #4]!
	ldr	r3, [r1]
	subs	r2, #1
	str	r3, [r0]
	str	r12, [r1], #-4
	bne	.LBB0_2
.LBB0_3:
	bx	lr
.Lfunc_end0:
	.size	pat_alg_array_reversal_001, .Lfunc_end0-pat_alg_array_reversal_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
