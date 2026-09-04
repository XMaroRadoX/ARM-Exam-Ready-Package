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
	.globl	pat_alg_lis_001                 @ -- Begin function pat_alg_lis_001
	.p2align	2
	.type	pat_alg_lis_001,%function
	.code	16                              @ @pat_alg_lis_001
	.thumb_func
pat_alg_lis_001:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r11}
	str	r11, [sp, #-4]!
	mov	lr, r0
	cmp	r0, #0
	mov.w	r0, #0
	it	ne
	cmpne	r2, #0
	bne	.LBB0_2
.LBB0_1:
	ldr	r11, [sp], #4
	pop	{r4, r5, r6, r7, pc}
.LBB0_2:
	cmp	r1, #0
	beq	.LBB0_1
@ %bb.3:
	mov.w	r12, #1
	movs	r3, #0
	b	.LBB0_5
	.p2align	2
.LBB0_4:                                @   in Loop: Header=BB0_5 Depth=1
	ldr.w	r4, [r2, r3, lsl #2]
	adds	r3, #1
	cmp	r4, r0
	it	hi
	movhi	r0, r4
	cmp	r3, r1
	beq	.LBB0_1
.LBB0_5:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_8 Depth 2
	cmp	r3, #0
	str.w	r12, [r2, r3, lsl #2]
	beq	.LBB0_4
@ %bb.6:                                @   in Loop: Header=BB0_5 Depth=1
	movs	r4, #0
	b	.LBB0_8
	.p2align	2
.LBB0_7:                                @   in Loop: Header=BB0_8 Depth=2
	adds	r4, #1
	cmp	r3, r4
	beq	.LBB0_4
.LBB0_8:                                @   Parent Loop BB0_5 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldr.w	r5, [lr, r4, lsl #2]
	ldr.w	r6, [lr, r3, lsl #2]
	cmp	r5, r6
	bge	.LBB0_7
@ %bb.9:                                @   in Loop: Header=BB0_8 Depth=2
	ldr.w	r5, [r2, r4, lsl #2]
	ldr.w	r6, [r2, r3, lsl #2]
	adds	r5, #1
	cmp	r5, r6
	it	hi
	strhi.w	r5, [r2, r3, lsl #2]
	b	.LBB0_7
.Lfunc_end0:
	.size	pat_alg_lis_001, .Lfunc_end0-pat_alg_lis_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
