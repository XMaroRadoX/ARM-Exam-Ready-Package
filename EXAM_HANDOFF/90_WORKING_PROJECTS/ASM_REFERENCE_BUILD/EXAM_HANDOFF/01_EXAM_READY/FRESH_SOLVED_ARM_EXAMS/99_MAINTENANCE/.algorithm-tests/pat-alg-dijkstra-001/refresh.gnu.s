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
	.globl	pat_alg_dijkstra_001            @ -- Begin function pat_alg_dijkstra_001
	.p2align	2
	.type	pat_alg_dijkstra_001,%function
	.code	16                              @ @pat_alg_dijkstra_001
	.thumb_func
pat_alg_dijkstra_001:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	mov.w	r12, #0
	it	ne
	cmpne	r3, #0
	bne	.LBB0_2
@ %bb.1:
	mov	r0, r12
	bx	lr
.LBB0_2:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8, r9, r10, r11}
	push.w	{r8, r9, r10, r11}
	ldr.w	lr, [r7, #8]
	cmp.w	lr, #0
	beq	.LBB0_22
@ %bb.3:
	mov.w	r12, #0
	cmp.w	r12, r1, lsr #15
	bne	.LBB0_22
@ %bb.4:
	cmp	r2, r1
	bhs	.LBB0_22
@ %bb.5:
	movs	r6, #0
	mov.w	r5, #-1
	movs	r4, #0
	.p2align	2
.LBB0_6:                                @ =>This Inner Loop Header: Depth=1
	str.w	r5, [r3, r4, lsl #2]
	strb.w	r6, [lr, r4]
	adds	r4, #1
	cmp	r1, r4
	bne	.LBB0_6
@ %bb.7:
	mov.w	r10, #0
	mov.w	r9, #0
	str.w	r10, [r3, r2, lsl #2]
	.p2align	2
.LBB0_8:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_10 Depth 2
                                        @     Child Loop BB0_15 Depth 2
	movs	r6, #0
	mov.w	r5, #-1
	mov	r12, r1
	b	.LBB0_10
	.p2align	2
.LBB0_9:                                @   in Loop: Header=BB0_10 Depth=2
	adds	r6, #1
	cmp	r1, r6
	beq	.LBB0_12
.LBB0_10:                               @   Parent Loop BB0_8 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldrb.w	r2, [lr, r6]
	cmp	r2, #0
	bne	.LBB0_9
@ %bb.11:                               @   in Loop: Header=BB0_10 Depth=2
	ldr.w	r2, [r3, r6, lsl #2]
	cmp	r2, r5
	itt	lo
	movlo	r12, r6
	movlo	r5, r2
	b	.LBB0_9
	.p2align	2
.LBB0_12:                               @   in Loop: Header=BB0_8 Depth=1
	cmp	r12, r1
	beq	.LBB0_21
@ %bb.13:                               @   in Loop: Header=BB0_8 Depth=1
	movs	r2, #1
	strb.w	r2, [lr, r12]
	mul	r2, r12, r1
	add.w	r11, r0, r2, lsl #2
	movs	r5, #0
	b	.LBB0_15
	.p2align	2
.LBB0_14:                               @   in Loop: Header=BB0_15 Depth=2
	adds	r5, #1
	cmp	r1, r5
	beq	.LBB0_19
.LBB0_15:                               @   Parent Loop BB0_8 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldr.w	r4, [r11, r5, lsl #2]
	cmp	r4, #0
	beq	.LBB0_14
@ %bb.16:                               @   in Loop: Header=BB0_15 Depth=2
	ldr.w	r2, [r3, r12, lsl #2]
	adds	r6, r4, r2
	adc	r6, r10, #0
	adds.w	r8, r2, #1
	beq	.LBB0_14
@ %bb.17:                               @   in Loop: Header=BB0_15 Depth=2
	cmp	r6, #0
	bne	.LBB0_14
@ %bb.18:                               @   in Loop: Header=BB0_15 Depth=2
	ldr.w	r6, [r3, r5, lsl #2]
	add	r2, r4
	cmp	r2, r6
	it	lo
	strlo.w	r2, [r3, r5, lsl #2]
	b	.LBB0_14
	.p2align	2
.LBB0_19:                               @   in Loop: Header=BB0_8 Depth=1
	cmp	r12, r1
	mov.w	r12, #1
	beq	.LBB0_22
@ %bb.20:                               @   in Loop: Header=BB0_8 Depth=1
	add.w	r9, r9, #1
	cmp	r9, r1
	bne	.LBB0_8
	b	.LBB0_22
.LBB0_21:
	mov.w	r12, #1
.LBB0_22:
	pop.w	{r8, r9, r10, r11}
	pop.w	{r4, r5, r6, r7, lr}
	mov	r0, r12
	bx	lr
.Lfunc_end0:
	.size	pat_alg_dijkstra_001, .Lfunc_end0-pat_alg_dijkstra_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
