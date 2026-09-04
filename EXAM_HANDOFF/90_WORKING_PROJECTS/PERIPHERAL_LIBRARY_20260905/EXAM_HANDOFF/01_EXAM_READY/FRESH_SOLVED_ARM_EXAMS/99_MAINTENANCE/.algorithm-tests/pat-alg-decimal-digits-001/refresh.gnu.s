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
	.globl	pat_alg_decimal_digits_001      @ -- Begin function pat_alg_decimal_digits_001
	.p2align	2
	.type	pat_alg_decimal_digits_001,%function
	.code	16                              @ @pat_alg_decimal_digits_001
	.thumb_func
pat_alg_decimal_digits_001:
	.fnstart
@ %bb.0:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	movw	r12, #52429
	movs	r1, #0
	movt	r12, #52428
	mov.w	lr, #0
	.p2align	2
.LBB0_1:                                @ =>This Inner Loop Header: Depth=1
	umull	r2, r3, r0, r12
	lsrs	r4, r3, #3
	add.w	r3, r4, r4, lsl #2
	sub.w	r3, r0, r3, lsl #1
	add.w	r2, lr, lr, lsl #2
	add	r1, r3
	add.w	lr, r3, r2, lsl #1
	cmp	r0, #9
	mov	r0, r4
	bhi	.LBB0_1
@ %bb.2:
	uxth.w	r0, lr
	orr.w	r0, r0, r1, lsl #16
	pop	{r4, r6, r7, pc}
.Lfunc_end0:
	.size	pat_alg_decimal_digits_001, .Lfunc_end0-pat_alg_decimal_digits_001
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_decimal_digits_001_extract @ -- Begin function pat_alg_decimal_digits_001_extract
	.p2align	2
	.type	pat_alg_decimal_digits_001_extract,%function
	.code	16                              @ @pat_alg_decimal_digits_001_extract
	.thumb_func
pat_alg_decimal_digits_001_extract:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r7, lr}
	push	{r4, r5, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	cmp	r1, #0
	mov.w	lr, #0
	it	ne
	cmpne	r2, #0
	bne	.LBB1_2
.LBB1_1:
	mov	r0, lr
	pop	{r4, r5, r7, pc}
.LBB1_2:
	movw	r12, #52429
	movs	r5, #0
	movt	r12, #52428
	.p2align	2
.LBB1_3:                                @ =>This Inner Loop Header: Depth=1
	cmp	r2, r5
	beq	.LBB1_5
@ %bb.4:                                @   in Loop: Header=BB1_3 Depth=1
	umull	r3, r4, r0, r12
	lsrs	r3, r4, #3
	add.w	r4, r3, r3, lsl #2
	sub.w	r4, r0, r4, lsl #1
	add.w	lr, r5, #1
	strb	r4, [r1, r5]
	cmp	r0, #9
	mov	r0, r3
	mov	r5, lr
	bhi	.LBB1_3
	b	.LBB1_1
.LBB1_5:
	movs	r0, #0
	pop	{r4, r5, r7, pc}
.Lfunc_end1:
	.size	pat_alg_decimal_digits_001_extract, .Lfunc_end1-pat_alg_decimal_digits_001_extract
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_decimal_digits_001_reconstruct @ -- Begin function pat_alg_decimal_digits_001_reconstruct
	.p2align	2
	.type	pat_alg_decimal_digits_001_reconstruct,%function
	.code	16                              @ @pat_alg_decimal_digits_001_reconstruct
	.thumb_func
pat_alg_decimal_digits_001_reconstruct:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	mov.w	r2, #0
	it	ne
	cmpne	r1, #0
	bne	.LBB2_2
@ %bb.1:
	mov	r0, r2
	bx	lr
.LBB2_2:
	.save	{r7, lr}
	push	{r7, lr}
	.setfp	r7, sp
	mov	r7, sp
	subs	r1, #1
	mov.w	r12, #0
	movs	r2, #0
	.p2align	2
.LBB2_3:                                @ =>This Inner Loop Header: Depth=1
	add.w	lr, r2, r2, lsl #2
	ldrb	r2, [r0, r1]
	subs	r1, #1
	adc	r3, r12, #0
	cmp	r0, #0
	add.w	r2, r2, lr, lsl #1
	it	ne
	cmpne	r3, #0
	bne	.LBB2_3
@ %bb.4:
	pop.w	{r7, lr}
	mov	r0, r2
	bx	lr
.Lfunc_end2:
	.size	pat_alg_decimal_digits_001_reconstruct, .Lfunc_end2-pat_alg_decimal_digits_001_reconstruct
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_decimal_digits_001_is_palindrome @ -- Begin function pat_alg_decimal_digits_001_is_palindrome
	.p2align	2
	.type	pat_alg_decimal_digits_001_is_palindrome,%function
	.code	16                              @ @pat_alg_decimal_digits_001_is_palindrome
	.thumb_func
pat_alg_decimal_digits_001_is_palindrome:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r7, lr}
	push	{r4, r5, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	movw	r12, #52429
	movs	r2, #0
	movt	r12, #52428
	mov.w	lr, #10
	mov	r1, r0
	movs	r3, #0
	.p2align	2
.LBB3_1:                                @ =>This Inner Loop Header: Depth=1
	umull	r4, r5, r1, r12
	lsrs	r5, r5, #3
	add.w	r3, r3, r3, lsl #2
	add.w	r4, r5, r5, lsl #2
	lsls	r3, r3, #1
	sub.w	r4, r1, r4, lsl #1
	umlal	r4, r3, r2, lr
	cmp	r1, #9
	mov	r1, r5
	mov	r2, r4
	bhi	.LBB3_1
@ %bb.2:
	eors	r0, r4
	orrs	r0, r3
	clz	r0, r0
	lsrs	r0, r0, #5
	pop	{r4, r5, r7, pc}
.Lfunc_end3:
	.size	pat_alg_decimal_digits_001_is_palindrome, .Lfunc_end3-pat_alg_decimal_digits_001_is_palindrome
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_decimal_digits_001_kaprekar_4 @ -- Begin function pat_alg_decimal_digits_001_kaprekar_4
	.p2align	2
	.type	pat_alg_decimal_digits_001_kaprekar_4,%function
	.code	16                              @ @pat_alg_decimal_digits_001_kaprekar_4
	.thumb_func
pat_alg_decimal_digits_001_kaprekar_4:
	.fnstart
@ %bb.0:
	.save	{r4, r6, r7, lr}
	push	{r4, r6, r7, lr}
	.setfp	r7, sp, #8
	add	r7, sp, #8
	.pad	#4
	sub	sp, #4
	movw	r12, #52429
	movs	r2, #0
	movt	r12, #52428
	mov	lr, sp
	.p2align	2
.LBB4_1:                                @ =>This Inner Loop Header: Depth=1
	umull	r1, r3, r0, r12
	lsrs	r1, r3, #3
	add.w	r3, r1, r1, lsl #2
	sub.w	r0, r0, r3, lsl #1
	strb.w	r0, [lr, r2]
	adds	r2, #1
	cmp	r2, #4
	mov	r0, r1
	bne	.LBB4_1
@ %bb.2:
	mov.w	r12, #0
	b	.LBB4_4
	.p2align	2
.LBB4_3:                                @   in Loop: Header=BB4_4 Depth=1
	cmp.w	r12, #4
	beq	.LBB4_7
.LBB4_4:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB4_6 Depth 2
	mov	r2, r12
	cmp.w	r12, #2
	add.w	r12, r12, #1
	bhi	.LBB4_3
@ %bb.5:                                @   in Loop: Header=BB4_4 Depth=1
	mov	r3, r12
	.p2align	2
.LBB4_6:                                @   Parent Loop BB4_4 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldrb.w	r0, [lr, r3]
	ldrb.w	r1, [lr, r2]
	cmp	r0, r1
	itt	lo
	strblo.w	r0, [lr, r2]
	strblo.w	r1, [lr, r3]
	adds	r3, #1
	cmp	r3, #4
	bne	.LBB4_6
	b	.LBB4_3
.LBB4_7:
	mov.w	r12, #0
	movs	r2, #3
	mov.w	r3, #-1
	movs	r4, #0
	.p2align	2
.LBB4_8:                                @ =>This Inner Loop Header: Depth=1
	add.w	r1, lr, r3
	ldrb	r1, [r1, #1]
	add.w	r0, r4, r4, lsl #2
	add.w	r4, r1, r0, lsl #1
	ldrb.w	r1, [lr, r2]
	add.w	r0, r12, r12, lsl #2
	subs	r2, #1
	add.w	r12, r1, r0, lsl #1
	adds	r0, r2, #1
	add.w	r3, r3, #1
	bne	.LBB4_8
@ %bb.9:
	sub.w	r0, r12, r4
	add	sp, #4
	pop	{r4, r6, r7, pc}
.Lfunc_end4:
	.size	pat_alg_decimal_digits_001_kaprekar_4, .Lfunc_end4-pat_alg_decimal_digits_001_kaprekar_4
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
