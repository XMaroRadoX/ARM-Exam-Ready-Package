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
	.globl	pat_alg_edit_distance_001       @ -- Begin function pat_alg_edit_distance_001
	.p2align	2
	.type	pat_alg_edit_distance_001,%function
	.code	16                              @ @pat_alg_edit_distance_001
	.thumb_func
pat_alg_edit_distance_001:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r10, r11}
	push.w	{r8, r9, r10, r11}
	.pad	#20
	sub	sp, #20
	cmp	r0, #0
	mov.w	r12, #-1
	str	r3, [sp, #16]                   @ 4-byte Spill
	str	r2, [sp, #4]                    @ 4-byte Spill
	it	ne
	cmpne	r1, #0
	bne	.LBB0_2
.LBB0_1:
	mov	r0, r12
	add	sp, #20
	pop.w	{r8, r9, r10, r11}
	pop	{r4, r5, r6, r7, pc}
.LBB0_2:
	ldr	r6, [r7, #8]
	cmp	r6, #0
	beq	.LBB0_1
@ %bb.3:
	ldr	r2, [r7, #12]
	cmp	r2, #0
	beq	.LBB0_1
@ %bb.4:
	movw	r3, #65534
	ldr	r2, [sp, #16]                   @ 4-byte Reload
	movt	r3, #16383
	cmp	r2, r3
	bhi	.LBB0_1
@ %bb.5:
	ldr	r2, [sp, #4]                    @ 4-byte Reload
	adds	r3, r2, #1
	beq	.LBB0_1
@ %bb.6:
	ldr	r2, [r7, #12]
	cmp	r2, r6
	beq	.LBB0_1
@ %bb.7:
	ldr	r2, [sp, #16]                   @ 4-byte Reload
	movs	r3, #0
	add.w	r11, r2, #1
	.p2align	2
.LBB0_8:                                @ =>This Inner Loop Header: Depth=1
	str.w	r3, [r6, r3, lsl #2]
	adds	r3, #1
	cmp	r11, r3
	bne	.LBB0_8
@ %bb.9:
	ldr	r2, [sp, #4]                    @ 4-byte Reload
	cmp	r2, #0
	beq	.LBB0_17
@ %bb.10:
	sub.w	r12, r0, #1
	ldr	r0, [r7, #12]
	mov.w	r10, #1
	subs	r0, #4
	str	r0, [sp, #12]                   @ 4-byte Spill
	ldr	r0, [r7, #8]
	subs	r0, #4
	str	r0, [sp, #8]                    @ 4-byte Spill
	subs	r0, r1, #1
	str	r0, [sp]                        @ 4-byte Spill
	.p2align	2
.LBB0_11:                               @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_13 Depth 2
                                        @     Child Loop BB0_15 Depth 2
	ldr	r0, [sp, #16]                   @ 4-byte Reload
	cmp	r0, #0
	ldr	r0, [r7, #12]
	str.w	r10, [r0]
	beq	.LBB0_14
@ %bb.12:                               @   in Loop: Header=BB0_11 Depth=1
	ldr	r5, [r0]
	ldr	r6, [sp]                        @ 4-byte Reload
	ldrd	r4, r9, [sp, #8]                @ 8-byte Folded Reload
	ldr	r3, [sp, #16]                   @ 4-byte Reload
	.p2align	2
.LBB0_13:                               @   Parent Loop BB0_11 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldr	lr, [r4, #4]!
	ldrb.w	r2, [r12, r10]
	ldr.w	r8, [r4, #4]
	ldrb	r1, [r6, #1]!
	add.w	r0, r8, #1
	adds	r5, #1
	cmp	r2, r1
	it	ne
	addne.w	lr, lr, #1
	cmp	r0, r5
	it	lo
	movlo	r5, r0
	cmp	r5, lr
	it	hs
	movhs	r5, lr
	str.w	r5, [r9, #8]
	subs	r3, #1
	add.w	r9, r9, #4
	bne	.LBB0_13
.LBB0_14:                               @   in Loop: Header=BB0_11 Depth=1
	ldrd	r4, r3, [sp, #8]                @ 8-byte Folded Reload
	mov	r5, r11
	.p2align	2
.LBB0_15:                               @   Parent Loop BB0_11 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldr	r0, [r3, #4]!
	subs	r5, #1
	str	r0, [r4, #4]!
	bne	.LBB0_15
@ %bb.16:                               @   in Loop: Header=BB0_11 Depth=1
	ldr	r0, [sp, #4]                    @ 4-byte Reload
	cmp	r10, r0
	add.w	r10, r10, #1
	bne	.LBB0_11
.LBB0_17:
	ldr	r0, [sp, #16]                   @ 4-byte Reload
	ldr	r1, [r7, #8]
	ldr.w	r12, [r1, r0, lsl #2]
	b	.LBB0_1
.Lfunc_end0:
	.size	pat_alg_edit_distance_001, .Lfunc_end0-pat_alg_edit_distance_001
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_edit_distance_001_full  @ -- Begin function pat_alg_edit_distance_001_full
	.p2align	2
	.type	pat_alg_edit_distance_001_full,%function
	.code	16                              @ @pat_alg_edit_distance_001_full
	.thumb_func
pat_alg_edit_distance_001_full:
	.fnstart
@ %bb.0:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r10, r11}
	push.w	{r8, r9, r10, r11}
	.pad	#28
	sub	sp, #28
	str	r3, [sp, #16]                   @ 4-byte Spill
	adds.w	lr, r3, #1
	mov.w	r3, #0
	mov	r6, r2
	adc	r3, r3, #0
	adds	r4, r2, #1
	mov.w	r12, #-1
	str	r6, [sp, #8]                    @ 4-byte Spill
	beq.w	.LBB1_18
@ %bb.1:
	cmp	r3, #0
	bne.w	.LBB1_18
@ %bb.2:
	cmp	r0, #0
	beq.w	.LBB1_18
@ %bb.3:
	cmp	r1, #0
	beq.w	.LBB1_18
@ %bb.4:
	ldr.w	r8, [r7, #8]
	cmp.w	r8, #0
	beq	.LBB1_18
@ %bb.5:
	ldr	r3, [r7, #12]
	mul	r6, lr, r4
	cmp	r6, r3
	bhi	.LBB1_18
@ %bb.6:
	mvn	r3, #-1073741824
	udiv	r3, r3, lr
	cmp	r4, r3
	bhi	.LBB1_18
@ %bb.7:
	ldr	r2, [sp, #16]                   @ 4-byte Reload
	movs	r3, #4
	add.w	r3, r3, r2, lsl #2
	movs	r6, #0
	mov	r5, r8
	.p2align	2
.LBB1_8:                                @ =>This Inner Loop Header: Depth=1
	str	r6, [r5]
	adds	r6, #1
	cmp	r4, r6
	add	r5, r3
	bne	.LBB1_8
@ %bb.9:
	ldr	r2, [sp, #16]                   @ 4-byte Reload
	movs	r6, #0
	adds	r3, r2, #1
	str.w	lr, [sp]                        @ 4-byte Spill
	.p2align	2
.LBB1_10:                               @ =>This Inner Loop Header: Depth=1
	str.w	r6, [r8, r6, lsl #2]
	adds	r6, #1
	cmp	r3, r6
	bne	.LBB1_10
@ %bb.11:
	ldr	r2, [sp, #8]                    @ 4-byte Reload
	cmp	r2, #0
	beq	.LBB1_17
@ %bb.12:
	subs	r1, #1
	ldr	r2, [sp, #16]                   @ 4-byte Reload
	str	r1, [sp, #4]                    @ 4-byte Spill
	movs	r1, #4
	add.w	r1, r1, r2, lsl #2
	str	r1, [sp, #12]                   @ 4-byte Spill
	ldr	r1, [r7, #8]
	mov.w	r9, #0
	subs	r1, #4
	str	r1, [sp, #24]                   @ 4-byte Spill
	movs	r1, #8
	add.w	r10, r1, r2, lsl #2
	movs	r1, #1
	str	r1, [sp, #20]                   @ 4-byte Spill
	b	.LBB1_14
	.p2align	2
.LBB1_13:                               @   in Loop: Header=BB1_14 Depth=1
	ldr	r1, [sp, #8]                    @ 4-byte Reload
	ldr	r2, [sp, #20]                   @ 4-byte Reload
	ldr	r3, [sp, #24]                   @ 4-byte Reload
	cmp	r2, r1
	add.w	r1, r2, #1
	ldr	r2, [sp, #12]                   @ 4-byte Reload
	add.w	r9, r9, #1
	add	r3, r2
	strd	r1, r3, [sp, #20]               @ 8-byte Folded Spill
	beq	.LBB1_17
.LBB1_14:                               @ =>This Loop Header: Depth=1
                                        @     Child Loop BB1_16 Depth 2
	ldr	r1, [sp, #16]                   @ 4-byte Reload
	cmp	r1, #0
	beq	.LBB1_13
@ %bb.15:                               @   in Loop: Header=BB1_14 Depth=1
	ldr	r2, [sp, #12]                   @ 4-byte Reload
	add.w	r1, r9, #1
	mul	r3, r2, r1
	ldr	r1, [sp, #20]                   @ 4-byte Reload
	ldr.w	r12, [sp, #4]                   @ 4-byte Reload
	sub.w	lr, r1, #1
	ldr	r1, [r7, #8]
	ldr.w	r11, [sp, #24]                  @ 4-byte Reload
	ldr	r5, [r1, r3]
	ldr	r3, [sp, #16]                   @ 4-byte Reload
	.p2align	2
.LBB1_16:                               @   Parent Loop BB1_14 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldr.w	r8, [r11, #8]
	ldrb.w	r6, [r0, lr]
	ldrb	r1, [r12, #1]!
	add.w	r4, r8, #1
	add.w	r8, r11, r10
	adds	r5, #1
	ldr	r2, [r11, #4]!
	cmp	r6, r1
	it	ne
	addne	r2, #1
	cmp	r4, r5
	it	lo
	movlo	r5, r4
	cmp	r5, r2
	it	hs
	movhs	r5, r2
	subs	r3, #1
	str.w	r5, [r8, #4]
	bne	.LBB1_16
	b	.LBB1_13
.LBB1_17:
	ldr	r0, [sp, #8]                    @ 4-byte Reload
	ldr	r1, [sp]                        @ 4-byte Reload
	muls	r0, r1, r0
	ldr	r1, [r7, #8]
	add.w	r0, r1, r0, lsl #2
	ldr	r1, [sp, #16]                   @ 4-byte Reload
	ldr.w	r12, [r0, r1, lsl #2]
.LBB1_18:
	mov	r0, r12
	add	sp, #28
	pop.w	{r8, r9, r10, r11}
	pop	{r4, r5, r6, r7, pc}
.Lfunc_end1:
	.size	pat_alg_edit_distance_001_full, .Lfunc_end1-pat_alg_edit_distance_001_full
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
