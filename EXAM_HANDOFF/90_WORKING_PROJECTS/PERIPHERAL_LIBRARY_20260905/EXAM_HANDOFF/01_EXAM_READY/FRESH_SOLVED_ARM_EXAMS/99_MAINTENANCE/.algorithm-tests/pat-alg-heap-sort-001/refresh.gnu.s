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
	.globl	down                            @ -- Begin function down
	.p2align	2
	.type	down,%function
	.code	16                              @ @down
	.thumb_func
down:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	it	eq
	bxeq	lr
.LBB0_1:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r11}
	str	r11, [sp, #-4]!
	lsr.w	lr, r1, #1
	mov.w	r12, #2
	b	.LBB0_3
	.p2align	2
.LBB0_2:                                @   in Loop: Header=BB0_3 Depth=1
	cmp	r3, r2
	mov	r2, r4
	beq	.LBB0_10
.LBB0_3:                                @ =>This Inner Loop Header: Depth=1
	cmp	r2, lr
	bhs	.LBB0_10
@ %bb.4:                                @   in Loop: Header=BB0_3 Depth=1
	lsls	r3, r2, #1
	adds	r4, r3, #1
	cmp	r4, r1
	mov	r3, r2
	bhs	.LBB0_6
@ %bb.5:                                @   in Loop: Header=BB0_3 Depth=1
	ldr.w	r3, [r0, r4, lsl #2]
	ldr.w	r5, [r0, r2, lsl #2]
	cmp	r3, r5
	it	le
	movle	r4, r2
	mov	r3, r4
.LBB0_6:                                @   in Loop: Header=BB0_3 Depth=1
	add.w	r4, r12, r2, lsl #1
	cmp	r4, r1
	bhs	.LBB0_8
@ %bb.7:                                @   in Loop: Header=BB0_3 Depth=1
	ldr.w	r5, [r0, r4, lsl #2]
	ldr.w	r6, [r0, r3, lsl #2]
	cmp	r5, r6
	it	gt
	movgt	r3, r4
.LBB0_8:                                @   in Loop: Header=BB0_3 Depth=1
	cmp	r3, r2
	mov	r4, r2
	beq	.LBB0_2
@ %bb.9:                                @   in Loop: Header=BB0_3 Depth=1
	ldr.w	r4, [r0, r3, lsl #2]
	ldr.w	r5, [r0, r2, lsl #2]
	str.w	r4, [r0, r2, lsl #2]
	mov	r4, r3
	str.w	r5, [r0, r3, lsl #2]
	b	.LBB0_2
.LBB0_10:
	ldr	r11, [sp], #4
	pop.w	{r4, r5, r6, r7, lr}
	bx	lr
.Lfunc_end0:
	.size	down, .Lfunc_end0-down
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_heap_sort_001           @ -- Begin function pat_alg_heap_sort_001
	.p2align	2
	.type	pat_alg_heap_sort_001,%function
	.code	16                              @ @pat_alg_heap_sort_001
	.thumb_func
pat_alg_heap_sort_001:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	it	eq
	bxeq	lr
.LBB1_1:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8}
	str	r8, [sp, #-4]!
	lsrs.w	r8, r1, #1
	beq	.LBB1_13
@ %bb.2:
	mov.w	lr, #2
	mov	r12, r8
	b	.LBB1_4
	.p2align	2
.LBB1_3:                                @   in Loop: Header=BB1_4 Depth=1
	cmp.w	r12, #0
	beq	.LBB1_13
.LBB1_4:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB1_6 Depth 2
	sub.w	r12, r12, #1
	mov	r3, r12
	b	.LBB1_6
	.p2align	2
.LBB1_5:                                @   in Loop: Header=BB1_6 Depth=2
	cmp	r4, r3
	mov	r3, r5
	beq	.LBB1_3
.LBB1_6:                                @   Parent Loop BB1_4 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	cmp	r3, r8
	bhs	.LBB1_3
@ %bb.7:                                @   in Loop: Header=BB1_6 Depth=2
	lsls	r4, r3, #1
	adds	r5, r4, #1
	cmp	r5, r1
	mov	r4, r3
	bhs	.LBB1_9
@ %bb.8:                                @   in Loop: Header=BB1_6 Depth=2
	ldr.w	r4, [r0, r5, lsl #2]
	ldr.w	r6, [r0, r3, lsl #2]
	cmp	r4, r6
	it	le
	movle	r5, r3
	mov	r4, r5
.LBB1_9:                                @   in Loop: Header=BB1_6 Depth=2
	add.w	r5, lr, r3, lsl #1
	cmp	r5, r1
	bhs	.LBB1_11
@ %bb.10:                               @   in Loop: Header=BB1_6 Depth=2
	ldr.w	r6, [r0, r5, lsl #2]
	ldr.w	r2, [r0, r4, lsl #2]
	cmp	r6, r2
	it	gt
	movgt	r4, r5
.LBB1_11:                               @   in Loop: Header=BB1_6 Depth=2
	cmp	r4, r3
	mov	r5, r3
	beq	.LBB1_5
@ %bb.12:                               @   in Loop: Header=BB1_6 Depth=2
	ldr.w	r2, [r0, r4, lsl #2]
	ldr.w	r5, [r0, r3, lsl #2]
	str.w	r2, [r0, r3, lsl #2]
	str.w	r5, [r0, r4, lsl #2]
	mov	r5, r4
	b	.LBB1_5
.LBB1_13:
	cmp	r1, #2
	blo	.LBB1_25
@ %bb.14:
	mov.w	r12, #2
	b	.LBB1_16
	.p2align	2
.LBB1_15:                               @   in Loop: Header=BB1_16 Depth=1
	cmp	r1, #1
	bls	.LBB1_25
.LBB1_16:                               @ =>This Loop Header: Depth=1
                                        @     Child Loop BB1_18 Depth 2
	subs	r1, #1
	ldr.w	r2, [r0, r1, lsl #2]
	ldr	r3, [r0]
	str	r2, [r0]
	lsr.w	lr, r1, #1
	movs	r2, #0
	str.w	r3, [r0, r1, lsl #2]
	b	.LBB1_18
	.p2align	2
.LBB1_17:                               @   in Loop: Header=BB1_18 Depth=2
	cmp	r4, r2
	mov	r2, r5
	beq	.LBB1_15
.LBB1_18:                               @   Parent Loop BB1_16 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	cmp	r2, lr
	bhs	.LBB1_15
@ %bb.19:                               @   in Loop: Header=BB1_18 Depth=2
	lsls	r6, r2, #1
	adds	r5, r6, #1
	cmp	r5, r1
	mov	r4, r2
	bhs	.LBB1_21
@ %bb.20:                               @   in Loop: Header=BB1_18 Depth=2
	ldr.w	r6, [r0, r5, lsl #2]
	ldr.w	r4, [r0, r2, lsl #2]
	cmp	r6, r4
	it	le
	movle	r5, r2
	mov	r4, r5
.LBB1_21:                               @   in Loop: Header=BB1_18 Depth=2
	add.w	r5, r12, r2, lsl #1
	cmp	r5, r1
	bhs	.LBB1_23
@ %bb.22:                               @   in Loop: Header=BB1_18 Depth=2
	ldr.w	r6, [r0, r5, lsl #2]
	ldr.w	r3, [r0, r4, lsl #2]
	cmp	r6, r3
	it	gt
	movgt	r4, r5
.LBB1_23:                               @   in Loop: Header=BB1_18 Depth=2
	cmp	r4, r2
	mov	r5, r2
	beq	.LBB1_17
@ %bb.24:                               @   in Loop: Header=BB1_18 Depth=2
	ldr.w	r3, [r0, r4, lsl #2]
	ldr.w	r5, [r0, r2, lsl #2]
	str.w	r3, [r0, r2, lsl #2]
	str.w	r5, [r0, r4, lsl #2]
	mov	r5, r4
	b	.LBB1_17
.LBB1_25:
	ldr	r8, [sp], #4
	pop.w	{r4, r5, r6, r7, lr}
	bx	lr
.Lfunc_end1:
	.size	pat_alg_heap_sort_001, .Lfunc_end1-pat_alg_heap_sort_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
