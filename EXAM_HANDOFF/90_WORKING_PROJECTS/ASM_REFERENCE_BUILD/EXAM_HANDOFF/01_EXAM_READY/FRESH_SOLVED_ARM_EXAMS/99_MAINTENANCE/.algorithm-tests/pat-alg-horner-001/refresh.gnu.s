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
	.globl	pat_alg_horner_001              @ -- Begin function pat_alg_horner_001
	.p2align	2
	.type	pat_alg_horner_001,%function
	.code	16                              @ @pat_alg_horner_001
	.thumb_func
pat_alg_horner_001:
	.fnstart
@ %bb.0:
	mov	r12, r0
	cmp	r0, #0
	mov.w	r0, #0
	beq	.LBB0_5
@ %bb.1:
	mov.w	r3, #0
	cbz	r1, .LBB0_6
@ %bb.2:
	.save	{r4, r5, r7, lr}
	push	{r4, r5, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	sub.w	r12, r12, #4
	movs	r0, #0
	asr.w	lr, r2, #31
	movs	r3, #0
	.p2align	2
.LBB0_3:                                @ =>This Inner Loop Header: Depth=1
	umull	r4, r5, r0, r2
	mla	r0, r0, lr, r5
	ldr.w	r5, [r12, r1, lsl #2]
	mla	r3, r3, r2, r0
	subs	r1, #1
	adds	r0, r4, r5
	adc.w	r3, r3, r5, asr #31
	cmp	r1, #0
	bne	.LBB0_3
@ %bb.4:
	pop.w	{r4, r5, r7, lr}
	mov	r1, r3
	bx	lr
.LBB0_5:
	movs	r3, #0
.LBB0_6:
	mov	r1, r3
	bx	lr
.Lfunc_end0:
	.size	pat_alg_horner_001, .Lfunc_end0-pat_alg_horner_001
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_horner_001_checked      @ -- Begin function pat_alg_horner_001_checked
	.p2align	2
	.type	pat_alg_horner_001_checked,%function
	.code	16                              @ @pat_alg_horner_001_checked
	.thumb_func
pat_alg_horner_001_checked:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r10, r11}
	push.w	{r8, r9, r10, r11}
	.pad	#4
	sub	sp, #4
	cmp	r3, #0
	beq.w	.LBB1_24
@ %bb.1:
	mov	r6, r2
	mov	r5, r1
	mov.w	r10, #0
	cbnz	r0, .LBB1_3
@ %bb.2:
	cmp	r5, #0
	bne.w	.LBB1_25
.LBB1_3:
	sub.w	r11, r0, #4
	adds	r4, r6, #1
	mov.w	r8, #0
	mov.w	r9, #0
	str	r3, [sp]                        @ 4-byte Spill
	b	.LBB1_6
	.p2align	2
.LBB1_4:                                @   in Loop: Header=BB1_6 Depth=1
	movs	r0, #0
.LBB1_5:                                @   in Loop: Header=BB1_6 Depth=1
	cmp	r0, #0
	sub.w	r5, r5, #1
	beq	.LBB1_24
.LBB1_6:                                @ =>This Inner Loop Header: Depth=1
	cmp	r5, #0
	beq	.LBB1_26
@ %bb.7:                                @   in Loop: Header=BB1_6 Depth=1
	cmp	r4, #0
	beq	.LBB1_17
@ %bb.8:                                @   in Loop: Header=BB1_6 Depth=1
	cmp	r6, #1
	blt	.LBB1_11
@ %bb.9:                                @   in Loop: Header=BB1_6 Depth=1
	mov.w	r0, #-1
	mvn	r1, #-2147483648
	mov	r2, r6
	movs	r3, #0
	bl	__aeabi_uldivmod
	subs.w	r0, r0, r8
	sbcs.w	r0, r1, r9
	blt	.LBB1_24
@ %bb.10:                               @   in Loop: Header=BB1_6 Depth=1
	movs	r0, #0
	mov.w	r1, #-2147483648
	mov	r2, r6
	movs	r3, #0
	bl	__aeabi_ldivmod
	subs.w	r0, r8, r0
	sbcs.w	r0, r9, r1
	blt	.LBB1_24
.LBB1_11:                               @   in Loop: Header=BB1_6 Depth=1
	cmn.w	r6, #2
	bgt	.LBB1_16
@ %bb.12:                               @   in Loop: Header=BB1_6 Depth=1
	subs.w	r0, r8, #1
	sbcs	r0, r9, #0
	blt	.LBB1_14
@ %bb.13:                               @   in Loop: Header=BB1_6 Depth=1
	asrs	r3, r6, #31
	movs	r0, #0
	mov.w	r1, #-2147483648
	mov	r2, r6
	bl	__aeabi_ldivmod
	subs.w	r0, r0, r8
	sbcs.w	r0, r1, r9
	blt	.LBB1_24
.LBB1_14:                               @   in Loop: Header=BB1_6 Depth=1
	cmp.w	r9, #-1
	bgt	.LBB1_16
@ %bb.15:                               @   in Loop: Header=BB1_6 Depth=1
	asrs	r3, r6, #31
	mov.w	r0, #-1
	mvn	r1, #-2147483648
	mov	r2, r6
	bl	__aeabi_ldivmod
	subs.w	r0, r8, r0
	sbcs.w	r0, r9, r1
	blt	.LBB1_24
	.p2align	2
.LBB1_16:                               @   in Loop: Header=BB1_6 Depth=1
	umull	r0, r1, r8, r6
	asrs	r2, r6, #31
	mla	r1, r8, r2, r1
	mov	r8, r0
	mla	r9, r9, r6, r1
	b	.LBB1_19
	.p2align	2
.LBB1_17:                               @   in Loop: Header=BB1_6 Depth=1
	mov.w	r0, #-2147483648
	eor.w	r0, r0, r9
	orrs.w	r0, r0, r8
	beq	.LBB1_24
@ %bb.18:                               @   in Loop: Header=BB1_6 Depth=1
	rsbs.w	r8, r8, #0
	sbc.w	r9, r10, r9
.LBB1_19:                               @   in Loop: Header=BB1_6 Depth=1
	ldr.w	r0, [r11, r5, lsl #2]
	cmp	r0, #1
	blt	.LBB1_21
@ %bb.20:                               @   in Loop: Header=BB1_6 Depth=1
	mvns	r1, r0
	subs.w	r1, r1, r8
	mvn	r1, #-2147483648
	sbcs.w	r1, r1, r9
	blt	.LBB1_4
.LBB1_21:                               @   in Loop: Header=BB1_6 Depth=1
	cmp.w	r0, #-1
	bgt	.LBB1_23
@ %bb.22:                               @   in Loop: Header=BB1_6 Depth=1
	rsbs	r1, r0, #0
	mov.w	r2, #-2147483648
	sbc.w	r2, r2, r0, asr #31
	subs.w	r1, r8, r1
	sbcs.w	r1, r9, r2
	blt.w	.LBB1_4
.LBB1_23:                               @   in Loop: Header=BB1_6 Depth=1
	adds.w	r8, r8, r0
	adc.w	r9, r9, r0, asr #31
	movs	r0, #1
	b	.LBB1_5
.LBB1_24:
	mov.w	r10, #0
.LBB1_25:
	mov	r0, r10
	add	sp, #4
	pop.w	{r8, r9, r10, r11}
	pop	{r4, r5, r6, r7, pc}
.LBB1_26:
	ldr	r0, [sp]                        @ 4-byte Reload
	mov.w	r10, #1
	strd	r8, r9, [r0]
	b	.LBB1_25
.Lfunc_end1:
	.size	pat_alg_horner_001_checked, .Lfunc_end1-pat_alg_horner_001_checked
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
