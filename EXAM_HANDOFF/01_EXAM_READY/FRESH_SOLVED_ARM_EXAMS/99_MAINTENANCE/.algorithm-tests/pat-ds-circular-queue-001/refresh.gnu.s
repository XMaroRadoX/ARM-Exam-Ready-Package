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
	.globl	pat_ds_circular_queue_001       @ -- Begin function pat_ds_circular_queue_001
	.p2align	2
	.type	pat_ds_circular_queue_001,%function
	.code	16                              @ @pat_ds_circular_queue_001
	.thumb_func
pat_ds_circular_queue_001:
	.fnstart
@ %bb.0:
	cbz	r0, .LBB0_10
@ %bb.1:
	ldr.w	r12, [r0]
	cmp.w	r12, #0
	beq	.LBB0_10
@ %bb.2:
	mov.w	r3, #0
	cbz	r2, .LBB0_11
@ %bb.3:
	.save	{r4, r5, r6, r7, lr}
	push	{r4, r5, r6, r7, lr}
	.setfp	r7, sp, #12
	add	r7, sp, #12
	.save	{r8}
	str	r8, [sp, #-4]!
	ldr	r4, [r0, #4]
	cbz	r4, .LBB0_16
@ %bb.4:
	mov	r3, r0
	ldr	r5, [r3, #8]!
	cmp	r5, r4
	bhs	.LBB0_15
@ %bb.5:
	mov	lr, r0
	ldr	r6, [lr, #12]!
	cmp	r6, r4
	bhs	.LBB0_15
@ %bb.6:
	ldr.w	r8, [r0, #16]
	cmp	r8, r4
	bhi	.LBB0_15
@ %bb.7:
	cbz	r1, .LBB0_12
@ %bb.8:
	cmp	r8, r4
	beq	.LBB0_15
@ %bb.9:
	ldr	r1, [r2]
	str.w	r1, [r12, r6, lsl #2]
	movs	r1, #1
	b	.LBB0_14
.LBB0_10:
	movs	r3, #0
.LBB0_11:
	mov	r0, r3
	bx	lr
.LBB0_12:
	cmp.w	r8, #0
	beq	.LBB0_15
@ %bb.13:
	ldr.w	r1, [r12, r5, lsl #2]
	mov	lr, r3
	str	r1, [r2]
	mov.w	r1, #-1
.LBB0_14:
	ldr.w	r2, [lr]
	ldr	r3, [r0, #4]
	adds	r2, #1
	udiv	r6, r2, r3
	mls	r2, r6, r3, r2
	ldr	r3, [r0, #16]
	str.w	r2, [lr]
	add	r1, r3
	movs	r3, #1
	str	r1, [r0, #16]
	b	.LBB0_16
.LBB0_15:
	movs	r3, #0
.LBB0_16:
	ldr	r8, [sp], #4
	pop.w	{r4, r5, r6, r7, lr}
	mov	r0, r3
	bx	lr
.Lfunc_end0:
	.size	pat_ds_circular_queue_001, .Lfunc_end0-pat_ds_circular_queue_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
