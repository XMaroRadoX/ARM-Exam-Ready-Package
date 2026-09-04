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
	.globl	visit                           @ -- Begin function visit
	.p2align	2
	.type	visit,%function
	.code	16                              @ @visit
	.thumb_func
visit:
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
	mov.w	r6, #0
	cbz	r0, .LBB0_5
@ %bb.1:
	mov	r9, r3
	cbz	r3, .LBB0_5
@ %bb.2:
	mov	r5, r1
	cmp	r2, r1
	bhs	.LBB0_5
@ %bb.3:
	mov	r8, r0
	ldr	r0, [r7, #8]
	subs	r1, r0, #1
	cmp	r1, r5
	bhs	.LBB0_5
@ %bb.4:
	ldrb.w	r1, [r9, r2]
	cbz	r1, .LBB0_6
.LBB0_5:
	mov	r0, r6
	add	sp, #4
	pop.w	{r8, r9, r10, r11}
	pop	{r4, r5, r6, r7, pc}
.LBB0_6:
	movs	r6, #1
	cmp	r5, #0
	strb.w	r6, [r9, r2]
	beq	.LBB0_5
@ %bb.7:
	mla	r10, r2, r5, r8
	add.w	r11, r0, #1
	movs	r4, #0
	b	.LBB0_9
	.p2align	2
.LBB0_8:                                @   in Loop: Header=BB0_9 Depth=1
	adds	r4, #1
	cmp	r5, r4
	beq	.LBB0_5
.LBB0_9:                                @ =>This Inner Loop Header: Depth=1
	ldrb.w	r0, [r10, r4]
	cmp	r0, #0
	beq	.LBB0_8
@ %bb.10:                               @   in Loop: Header=BB0_9 Depth=1
	ldrb.w	r0, [r9, r4]
	cmp	r0, #0
	bne	.LBB0_8
@ %bb.11:                               @   in Loop: Header=BB0_9 Depth=1
	mov	r0, r8
	mov	r1, r5
	mov	r2, r4
	mov	r3, r9
	str.w	r11, [sp]
	bl	visit
	add	r6, r0
	b	.LBB0_8
.Lfunc_end0:
	.size	visit, .Lfunc_end0-visit
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_alg_recursive_dfs_001       @ -- Begin function pat_alg_recursive_dfs_001
	.p2align	2
	.type	pat_alg_recursive_dfs_001,%function
	.code	16                              @ @pat_alg_recursive_dfs_001
	.thumb_func
pat_alg_recursive_dfs_001:
	.fnstart
@ %bb.0:
	cmp	r0, #0
	it	ne
	cmpne	r3, #0
	beq	.LBB1_2
@ %bb.1:
	cmp.w	r1, #256
	it	ls
	cmpls	r2, r1
	blo	.LBB1_3
.LBB1_2:
	movs	r0, #0
	bx	lr
.LBB1_3:
	.save	{r7, lr}
	push	{r7, lr}
	.setfp	r7, sp
	mov	r7, sp
	.pad	#8
	sub	sp, #8
	mov.w	r12, #1
	str.w	r12, [sp]
	bl	visit
	add	sp, #8
	pop	{r7, pc}
.Lfunc_end1:
	.size	pat_alg_recursive_dfs_001, .Lfunc_end1-pat_alg_recursive_dfs_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
