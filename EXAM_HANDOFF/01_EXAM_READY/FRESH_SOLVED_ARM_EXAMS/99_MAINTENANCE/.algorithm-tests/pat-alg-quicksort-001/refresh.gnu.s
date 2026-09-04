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
	.globl	qs                              @ -- Begin function qs
	.p2align	2
	.type	qs,%function
	.code	16                              @ @qs
	.thumb_func
qs:
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
	mov	r9, r2
	mov	r8, r0
	sub.w	r10, r0, #8
	mov	r11, r1
	b	.LBB0_2
	.p2align	2
.LBB0_1:                                @   in Loop: Header=BB0_2 Depth=1
	cmp	r11, r9
	mov	r1, r11
	bge	.LBB0_13
.LBB0_2:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_7 Depth 2
                                        @       Child Loop BB0_8 Depth 3
                                        @       Child Loop BB0_10 Depth 3
	subs.w	r0, r9, r1
	mov	r2, r9
	bge	.LBB0_5
.LBB0_3:                                @   in Loop: Header=BB0_2 Depth=1
	cmp	r2, r1
	ble	.LBB0_1
@ %bb.4:                                @   in Loop: Header=BB0_2 Depth=1
	mov	r0, r8
	bl	qs
	b	.LBB0_1
	.p2align	2
.LBB0_5:                                @   in Loop: Header=BB0_2 Depth=1
	add.w	r0, r0, r0, lsr #31
	mvn	r2, #2
	and.w	r0, r2, r0, lsl #1
	add	r0, r8
	ldr.w	r12, [r0, r1, lsl #2]
	mov	r11, r1
	mov	r3, r9
	b	.LBB0_7
	.p2align	2
.LBB0_6:                                @   in Loop: Header=BB0_7 Depth=2
	cmp	r11, r2
	mov	r3, r2
	bgt	.LBB0_3
.LBB0_7:                                @   Parent Loop BB0_2 Depth=1
                                        @ =>  This Loop Header: Depth=2
                                        @       Child Loop BB0_8 Depth 3
                                        @       Child Loop BB0_10 Depth 3
	add.w	r6, r10, r11, lsl #2
	mov	r4, r11
	.p2align	2
.LBB0_8:                                @   Parent Loop BB0_2 Depth=1
                                        @     Parent Loop BB0_7 Depth=2
                                        @ =>    This Inner Loop Header: Depth=3
	ldr	r5, [r6, #8]
	adds	r4, #1
	cmp	r5, r12
	add.w	r6, r6, #4
	blt	.LBB0_8
@ %bb.9:                                @   in Loop: Header=BB0_7 Depth=2
	sub.w	r11, r4, #1
	.p2align	2
.LBB0_10:                               @   Parent Loop BB0_2 Depth=1
                                        @     Parent Loop BB0_7 Depth=2
                                        @ =>    This Inner Loop Header: Depth=3
	ldr.w	r0, [r8, r3, lsl #2]
	subs	r3, #1
	cmp	r0, r12
	bgt	.LBB0_10
@ %bb.11:                               @   in Loop: Header=BB0_7 Depth=2
	adds	r2, r3, #1
	cmp	r11, r2
	bgt	.LBB0_6
@ %bb.12:                               @   in Loop: Header=BB0_7 Depth=2
	add.w	r2, r8, r3, lsl #2
	str	r0, [r6, #4]
	str	r5, [r2, #4]
	mov	r2, r3
	mov	r11, r4
	b	.LBB0_6
.LBB0_13:
	add	sp, #4
	pop.w	{r8, r9, r10, r11}
	pop	{r4, r5, r6, r7, pc}
.Lfunc_end0:
	.size	qs, .Lfunc_end0-qs
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_quicksort_001           @ -- Begin function pat_alg_quicksort_001
	.p2align	2
	.type	pat_alg_quicksort_001,%function
	.code	16                              @ @pat_alg_quicksort_001
	.thumb_func
pat_alg_quicksort_001:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	it	eq
	bxeq	lr
.LBB1_1:
	cmp	r1, #1
	blt	.LBB1_3
@ %bb.2:
	subs	r2, r1, #1
	movs	r1, #0
	b	qs
.LBB1_3:
	bx	lr
.Lfunc_end1:
	.size	pat_alg_quicksort_001, .Lfunc_end1-pat_alg_quicksort_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
