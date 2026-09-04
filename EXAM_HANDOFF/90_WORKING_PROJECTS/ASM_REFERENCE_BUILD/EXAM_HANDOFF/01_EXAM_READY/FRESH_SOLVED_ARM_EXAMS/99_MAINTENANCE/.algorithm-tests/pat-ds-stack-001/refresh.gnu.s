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
	.globl	pat_ds_stack_001                @ -- Begin function pat_ds_stack_001
	.p2align	2
	.type	pat_ds_stack_001,%function
	.code	16                              @ @pat_ds_stack_001
	.thumb_func
pat_ds_stack_001:
	.fnstart
@ %bb.0:
	mov	r12, r0
	cmp	r0, #0
	mov.w	r0, #0
	it	ne
	cmpne	r2, #0
	bne	.LBB0_2
@ %bb.1:
	bx	lr
.LBB0_2:
	.save	{r7, lr}
	push	{r7, lr}
	.setfp	r7, sp
	mov	r7, sp
	ldr.w	lr, [r7, #8]
	cmp.w	lr, #0
	beq	.LBB0_5
@ %bb.3:
	ldr	r0, [r2]
	cmp	r0, r1
	bls	.LBB0_6
@ %bb.4:
	movs	r0, #0
.LBB0_5:
	pop.w	{r7, lr}
	bx	lr
.LBB0_6:
	cbz	r3, .LBB0_9
@ %bb.7:
	cmp	r0, r1
	bhs	.LBB0_12
@ %bb.8:
	ldr.w	r1, [lr]
	adds	r3, r0, #1
	str	r3, [r2]
	str.w	r1, [r12, r0, lsl #2]
	b	.LBB0_11
.LBB0_9:
	cbz	r0, .LBB0_12
@ %bb.10:
	subs	r0, #1
	str	r0, [r2]
	ldr.w	r0, [r12, r0, lsl #2]
	str.w	r0, [lr]
.LBB0_11:
	movs	r0, #1
	pop.w	{r7, lr}
	bx	lr
.LBB0_12:
	movs	r0, #0
	pop.w	{r7, lr}
	bx	lr
.Lfunc_end0:
	.size	pat_ds_stack_001, .Lfunc_end0-pat_ds_stack_001
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
