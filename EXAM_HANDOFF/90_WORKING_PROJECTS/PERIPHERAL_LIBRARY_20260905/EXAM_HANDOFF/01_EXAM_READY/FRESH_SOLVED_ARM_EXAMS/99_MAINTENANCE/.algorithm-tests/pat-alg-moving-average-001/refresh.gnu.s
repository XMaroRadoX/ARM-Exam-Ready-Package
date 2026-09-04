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
	.globl	pat_alg_moving_average_001      @ -- Begin function pat_alg_moving_average_001
	.p2align	2
	.type	pat_alg_moving_average_001,%function
	.code	16                              @ @pat_alg_moving_average_001
	.thumb_func
pat_alg_moving_average_001:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r10, r11}
	push.w	{r8, r9, r10, r11}
	.pad	#12
	sub	sp, #12
	mov.w	r11, #0
	str	r3, [sp, #8]                    @ 4-byte Spill
	cbz	r2, .LBB0_11
@ %bb.1:
	mov	r9, r0
	cbz	r0, .LBB0_11
@ %bb.2:
	ldr	r0, [sp, #8]                    @ 4-byte Reload
	cbz	r0, .LBB0_11
@ %bb.3:
	mov	r5, r2
	mov	r10, r1
	cmp	r2, r1
	bhi	.LBB0_11
@ %bb.4:
	cmp	r5, #0
	bmi	.LBB0_11
@ %bb.5:
	sub.w	r0, r9, r5, lsl #2
	movs	r6, #0
	movs	r4, #0
	mov.w	r8, #0
	cmp.w	r10, #1
	it	ls
	movls.w	r10, #1
	str	r0, [sp, #4]                    @ 4-byte Spill
	b	.LBB0_7
	.p2align	2
.LBB0_6:                                @   in Loop: Header=BB0_7 Depth=1
	cmp	r10, r8
	beq	.LBB0_11
.LBB0_7:                                @ =>This Inner Loop Header: Depth=1
	ldr.w	r0, [r9, r8, lsl #2]
	adds	r6, r6, r0
	adc.w	r4, r4, r0, asr #31
	cmp	r8, r5
	blo	.LBB0_9
@ %bb.8:                                @   in Loop: Header=BB0_7 Depth=1
	ldr	r0, [sp, #4]                    @ 4-byte Reload
	ldr.w	r0, [r0, r8, lsl #2]
	subs	r6, r6, r0
	sbc.w	r4, r4, r0, asr #31
.LBB0_9:                                @   in Loop: Header=BB0_7 Depth=1
	add.w	r8, r8, #1
	cmp	r8, r5
	blo	.LBB0_6
@ %bb.10:                               @   in Loop: Header=BB0_7 Depth=1
	mov	r0, r6
	mov	r1, r4
	mov	r2, r5
	movs	r3, #0
	bl	__aeabi_ldivmod
	ldr	r1, [sp, #8]                    @ 4-byte Reload
	str.w	r0, [r1, r11, lsl #2]
	add.w	r11, r11, #1
	b	.LBB0_6
.LBB0_11:
	mov	r0, r11
	add	sp, #12
	pop.w	{r8, r9, r10, r11}
	pop	{r4, r5, r6, r7, pc}
.Lfunc_end0:
	.size	pat_alg_moving_average_001, .Lfunc_end0-pat_alg_moving_average_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
