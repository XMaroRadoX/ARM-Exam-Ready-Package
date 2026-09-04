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
	.globl	pat_alg_coin_change_001         @ -- Begin function pat_alg_coin_change_001
	.p2align	2
	.type	pat_alg_coin_change_001,%function
	.code	16                              @ @pat_alg_coin_change_001
	.thumb_func
pat_alg_coin_change_001:
	.fnstart
@ %bb.0:
	cmp	r3, #0
	itt	eq
	moveq.w	r0, #-1
	bxeq	lr
.LBB0_1:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r11}
	str	r11, [sp, #-4]!
	clz	r5, r0
	lsrs	r5, r5, #5
	cmp	r1, #0
	mov	r4, r1
	it	ne
	movne	r4, #1
	tst	r5, r4
	mov.w	r12, #-1
	bne	.LBB0_15
@ %bb.2:
	movw	r5, #65534
	movt	r5, #16383
	cmp	r2, r5
	bhi	.LBB0_15
@ %bb.3:
	add.w	r12, r2, #1
	movs	r4, #0
	mov.w	lr, #-1
	.p2align	2
.LBB0_4:                                @ =>This Inner Loop Header: Depth=1
	str.w	lr, [r3, r4, lsl #2]
	adds	r4, #1
	cmp	r12, r4
	bne	.LBB0_4
@ %bb.5:
	movs	r5, #0
	str	r5, [r3]
	cbz	r2, .LBB0_14
@ %bb.6:
	mov.w	r12, #1
	b	.LBB0_8
	.p2align	2
.LBB0_7:                                @   in Loop: Header=BB0_8 Depth=1
	cmp	r12, r2
	add.w	r12, r12, #1
	beq	.LBB0_14
.LBB0_8:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_11 Depth 2
	cmp	r1, #0
	beq	.LBB0_7
@ %bb.9:                                @   in Loop: Header=BB0_8 Depth=1
	mov	lr, r0
	mov	r4, r1
	b	.LBB0_11
	.p2align	2
.LBB0_10:                               @   in Loop: Header=BB0_11 Depth=2
	subs	r4, #1
	beq	.LBB0_7
.LBB0_11:                               @   Parent Loop BB0_8 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldrh	r5, [lr], #2
	cmp	r12, r5
	blo	.LBB0_10
@ %bb.12:                               @   in Loop: Header=BB0_11 Depth=2
	sub.w	r5, r12, r5
	ldr.w	r5, [r3, r5, lsl #2]
	adds	r5, #1
	bhs	.LBB0_10
@ %bb.13:                               @   in Loop: Header=BB0_11 Depth=2
	ldr.w	r6, [r3, r12, lsl #2]
	cmp	r5, r6
	it	lo
	strlo.w	r5, [r3, r12, lsl #2]
	b	.LBB0_10
.LBB0_14:
	ldr.w	r12, [r3, r2, lsl #2]
.LBB0_15:
	ldr	r11, [sp], #4
	pop.w	{r4, r5, r6, r7, lr}
	mov	r0, r12
	bx	lr
.Lfunc_end0:
	.size	pat_alg_coin_change_001, .Lfunc_end0-pat_alg_coin_change_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
