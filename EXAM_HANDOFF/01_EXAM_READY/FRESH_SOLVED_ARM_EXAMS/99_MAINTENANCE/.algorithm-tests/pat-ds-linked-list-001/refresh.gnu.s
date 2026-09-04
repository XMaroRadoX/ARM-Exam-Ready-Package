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
	.globl	pat_ds_linked_list_001          @ -- Begin function pat_ds_linked_list_001
	.p2align	2
	.type	pat_ds_linked_list_001,%function
	.code	16                              @ @pat_ds_linked_list_001
	.thumb_func
pat_ds_linked_list_001:
	.fnstart
@ %bb.0:
	b	.LBB0_3
	.p2align	2
.LBB0_1:                                @   in Loop: Header=BB0_3 Depth=1
	ldr	r2, [r0]
	cmp	r2, r1
	it	eq
	bxeq	lr
.LBB0_2:                                @   in Loop: Header=BB0_3 Depth=1
	ldr	r0, [r0, #4]
.LBB0_3:                                @ =>This Inner Loop Header: Depth=1
	cmp	r0, #0
	bne	.LBB0_1
@ %bb.4:
	bx	lr
.Lfunc_end0:
	.size	pat_ds_linked_list_001, .Lfunc_end0-pat_ds_linked_list_001
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_ds_linked_list_001_insert_after @ -- Begin function pat_ds_linked_list_001_insert_after
	.p2align	2
	.type	pat_ds_linked_list_001_insert_after,%function
	.code	16                              @ @pat_ds_linked_list_001_insert_after
	.thumb_func
pat_ds_linked_list_001_insert_after:
	.fnstart
@ %bb.0:
	mov	r2, r0
	cmp	r0, r1
	mov.w	r0, #0
	it	ne
	cmpne	r2, #0
	bne	.LBB1_2
@ %bb.1:
	bx	lr
.LBB1_2:
	cmp	r1, #0
	itttt	ne
	ldrne	r0, [r2, #4]
	strne	r0, [r1, #4]
	strne	r1, [r2, #4]
	movne	r0, #1
	bx	lr
.Lfunc_end1:
	.size	pat_ds_linked_list_001_insert_after, .Lfunc_end1-pat_ds_linked_list_001_insert_after
	.cantunwind
	.fnend
                                        @ -- End function
	.globl	pat_ds_linked_list_001_remove_first @ -- Begin function pat_ds_linked_list_001_remove_first
	.p2align	2
	.type	pat_ds_linked_list_001_remove_first,%function
	.code	16                              @ @pat_ds_linked_list_001_remove_first
	.thumb_func
pat_ds_linked_list_001_remove_first:
	.fnstart
@ %bb.0:
	cbz	r0, .LBB2_9
@ %bb.1:
	ldr	r2, [r0]
	cbz	r2, .LBB2_9
@ %bb.2:
	ldr	r3, [r2]
	cmp	r3, r1
	bne	.LBB2_4
@ %bb.3:
	clz	r1, r2
	lsrs	r1, r1, #5
	b	.LBB2_7
	.p2align	2
.LBB2_4:                                @ =>This Inner Loop Header: Depth=1
	mov	r0, r2
	ldr	r2, [r2, #4]
	cbz	r2, .LBB2_9
@ %bb.5:                                @   in Loop: Header=BB2_4 Depth=1
	ldr	r3, [r2]
	cmp	r3, r1
	bne	.LBB2_4
@ %bb.6:
	clz	r1, r2
	lsrs	r1, r1, #5
	adds	r0, #4
.LBB2_7:
	cmp	r1, #0
	mov.w	r1, #0
	bne	.LBB2_10
@ %bb.8:
	ldr	r3, [r2, #4]
	str	r3, [r0]
	mov	r0, r2
	str	r1, [r2, #4]
	bx	lr
.LBB2_9:
	movs	r1, #0
.LBB2_10:
	mov	r0, r1
	bx	lr
.Lfunc_end2:
	.size	pat_ds_linked_list_001_remove_first, .Lfunc_end2-pat_ds_linked_list_001_remove_first
	.cantunwind
	.fnend
                                        @ -- End function
	.ident	"clang version 19.1.3"
	.section	".note.GNU-stack","",%progbits
	.addrsig
	.eabi_attribute	30, 1	@ Tag_ABI_optimization_goals
