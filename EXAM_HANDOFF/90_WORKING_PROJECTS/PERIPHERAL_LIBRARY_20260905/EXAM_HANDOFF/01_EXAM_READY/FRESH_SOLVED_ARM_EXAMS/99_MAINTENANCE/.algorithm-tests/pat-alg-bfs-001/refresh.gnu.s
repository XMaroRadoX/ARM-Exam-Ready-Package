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
	.globl	pat_alg_bfs_001                 @ -- Begin function pat_alg_bfs_001
	.p2align	2
	.type	pat_alg_bfs_001,%function
	.code	16                              @ @pat_alg_bfs_001
	.thumb_func
pat_alg_bfs_001:
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
	.save	{r8}
	str	r8, [sp, #-4]!
	ldr.w	lr, [r7, #8]
	cmp.w	lr, #0
	beq	.LBB0_12
@ %bb.3:
	mov.w	r12, #0
	cmp.w	r12, r1, lsr #16
	bne	.LBB0_12
@ %bb.4:
	cmp	r2, r1
	bhs	.LBB0_12
@ %bb.5:
	mov.w	r8, #1
	strb.w	r8, [r3, r2]
	str.w	r2, [lr]
	movs	r2, #1
	b	.LBB0_7
	.p2align	2
.LBB0_6:                                @   in Loop: Header=BB0_7 Depth=1
	cmp	r12, r2
	bhs	.LBB0_12
.LBB0_7:                                @ =>This Loop Header: Depth=1
                                        @     Child Loop BB0_9 Depth 2
	ldr.w	r5, [lr, r12, lsl #2]
	add.w	r12, r12, #1
	mla	r5, r5, r1, r0
	movs	r6, #0
	b	.LBB0_9
	.p2align	2
.LBB0_8:                                @   in Loop: Header=BB0_9 Depth=2
	adds	r6, #1
	cmp	r1, r6
	beq	.LBB0_6
.LBB0_9:                                @   Parent Loop BB0_7 Depth=1
                                        @ =>  This Inner Loop Header: Depth=2
	ldrb	r4, [r5, r6]
	cmp	r4, #0
	beq	.LBB0_8
@ %bb.10:                               @   in Loop: Header=BB0_9 Depth=2
	ldrb	r4, [r3, r6]
	cmp	r4, #0
	bne	.LBB0_8
@ %bb.11:                               @   in Loop: Header=BB0_9 Depth=2
	strb.w	r8, [r3, r6]
	str.w	r6, [lr, r2, lsl #2]
	adds	r2, #1
	b	.LBB0_8
.LBB0_12:
	ldr	r8, [sp], #4
	pop.w	{r4, r5, r6, r7, lr}
	mov	r0, r12
	bx	lr
.Lfunc_end0:
	.size	pat_alg_bfs_001, .Lfunc_end0-pat_alg_bfs_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
