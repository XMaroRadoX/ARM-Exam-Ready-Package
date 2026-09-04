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
	.globl	pat_alg_flood_fill_001          @ -- Begin function pat_alg_flood_fill_001
	.p2align	2
	.type	pat_alg_flood_fill_001,%function
	.code	16                              @ @pat_alg_flood_fill_001
	.thumb_func
pat_alg_flood_fill_001:
	.fnstart
@ %bb.0:
	cmp	r2, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
.LBB0_1:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r10}
	push.w	{r8, r9, r10}
	mov	r12, r0
	umull	r0, r6, r2, r1
	cbz	r6, .LBB0_4
@ %bb.2:
	movs	r0, #0
.LBB0_3:
	pop.w	{r8, r9, r10}
	pop	{r4, r5, r6, r7, pc}
.LBB0_4:
	ldrd	r8, lr, [r7, #8]
	movs	r0, #0
	cmp	r8, lr
	beq	.LBB0_3
@ %bb.5:
	mul	r4, r2, r1
	cmp	r4, r3
	bls	.LBB0_3
@ %bb.6:
	cmp.w	r12, #0
	beq	.LBB0_3
@ %bb.7:
	ldr.w	r9, [r7, #16]
	cmp.w	r9, #0
	beq	.LBB0_3
@ %bb.8:
	ldrb.w	r0, [r12, r3]
	cmp	r0, r8
	bne	.LBB0_19
@ %bb.9:
	mov.w	r10, #1
	movs	r0, #0
	strb.w	lr, [r12, r3]
	str.w	r3, [r9]
	b	.LBB0_11
	.p2align	2
.LBB0_10:                               @   in Loop: Header=BB0_11 Depth=1
	adds	r0, #1
	cmp	r0, r10
	bhs	.LBB0_3
.LBB0_11:                               @ =>This Inner Loop Header: Depth=1
	ldr.w	r6, [r9, r0, lsl #2]
	cmp	r6, r2
	blo	.LBB0_13
@ %bb.12:                               @   in Loop: Header=BB0_11 Depth=1
	subs	r4, r6, r2
	ldrb.w	r5, [r12, r4]
	cmp	r5, r8
	ittt	eq
	strbeq.w	lr, [r12, r4]
	streq.w	r4, [r9, r10, lsl #2]
	addeq.w	r10, r10, #1
.LBB0_13:                               @   in Loop: Header=BB0_11 Depth=1
	udiv	r4, r6, r2
	adds	r5, r4, #1
	cmp	r5, r1
	bhs	.LBB0_15
@ %bb.14:                               @   in Loop: Header=BB0_11 Depth=1
	adds	r5, r6, r2
	ldrb.w	r3, [r12, r5]
	cmp	r3, r8
	ittt	eq
	strbeq.w	lr, [r12, r5]
	streq.w	r5, [r9, r10, lsl #2]
	addeq.w	r10, r10, #1
.LBB0_15:                               @   in Loop: Header=BB0_11 Depth=1
	mls	r4, r4, r2, r6
	cbz	r4, .LBB0_17
@ %bb.16:                               @   in Loop: Header=BB0_11 Depth=1
	subs	r5, r6, #1
	ldrb.w	r3, [r12, r5]
	cmp	r3, r8
	ittt	eq
	strbeq.w	lr, [r12, r5]
	streq.w	r5, [r9, r10, lsl #2]
	addeq.w	r10, r10, #1
.LBB0_17:                               @   in Loop: Header=BB0_11 Depth=1
	adds	r3, r4, #1
	cmp	r3, r2
	bhs	.LBB0_10
@ %bb.18:                               @   in Loop: Header=BB0_11 Depth=1
	adds	r4, r6, #1
	ldrb.w	r3, [r12, r4]
	cmp	r3, r8
	ittt	eq
	strbeq.w	lr, [r12, r4]
	streq.w	r4, [r9, r10, lsl #2]
	addeq.w	r10, r10, #1
	b	.LBB0_10
.LBB0_19:
	movs	r0, #0
	pop.w	{r8, r9, r10}
	pop	{r4, r5, r6, r7, pc}
.Lfunc_end0:
	.size	pat_alg_flood_fill_001, .Lfunc_end0-pat_alg_flood_fill_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
