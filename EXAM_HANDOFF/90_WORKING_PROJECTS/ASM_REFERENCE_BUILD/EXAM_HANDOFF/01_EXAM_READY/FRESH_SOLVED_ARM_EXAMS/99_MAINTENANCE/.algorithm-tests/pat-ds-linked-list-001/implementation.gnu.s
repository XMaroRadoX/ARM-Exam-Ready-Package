.syntax unified
.cpu cortex-m3
.thumb
.text
.global pat_ds_linked_list_001
.global pat_ds_linked_list_001_insert_after
.global pat_ds_linked_list_001_remove_first
.balign 4
pat_ds_linked_list_001:
        b	_LBB0_3
.balign 4
_LBB0_1:
        ldr	r2, [r0]
        cmp	r2, r1
        it	eq
        bxeq	lr
_LBB0_2:
        ldr	r0, [r0, #4]
_LBB0_3:
        cmp	r0, #0
        bne	_LBB0_1
        bx	lr
_Lfunc_end0:
.balign 4
pat_ds_linked_list_001_insert_after:
        mov	r2, r0
        cmp	r0, r1
        mov.w	r0, #0
        it	ne
        cmpne	r2, #0
        bne	_LBB1_2
        bx	lr
_LBB1_2:
        cmp	r1, #0
        itttt	ne
        ldrne	r0, [r2, #4]
        strne	r0, [r1, #4]
        strne	r1, [r2, #4]
        movne	r0, #1
        bx	lr
_Lfunc_end1:
.balign 4
pat_ds_linked_list_001_remove_first:
        cbz	r0, _LBB2_9
        ldr	r2, [r0]
        cbz	r2, _LBB2_9
        ldr	r3, [r2]
        cmp	r3, r1
        bne	_LBB2_4
        clz	r1, r2
        lsrs	r1, r1, #5
        b	_LBB2_7
.balign 4
_LBB2_4:
        mov	r0, r2
        ldr	r2, [r2, #4]
        cbz	r2, _LBB2_9
        ldr	r3, [r2]
        cmp	r3, r1
        bne	_LBB2_4
        clz	r1, r2
        lsrs	r1, r1, #5
        adds	r0, #4
_LBB2_7:
        cmp	r1, #0
        mov.w	r1, #0
        bne	_LBB2_10
        ldr	r3, [r2, #4]
        str	r3, [r0]
        mov	r0, r2
        str	r1, [r2, #4]
        bx	lr
_LBB2_9:
        movs	r1, #0
_LBB2_10:
        mov	r0, r1
        bx	lr
_Lfunc_end2:
.balign 4
