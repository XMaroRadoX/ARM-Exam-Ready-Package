; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_singly_linked_list_operations
        EXPORT algorithm_singly_linked_list_operations_insert_after
        EXPORT algorithm_singly_linked_list_operations_remove_first
        ALIGN 2
algorithm_singly_linked_list_operations
        b	_LBB0_3
        ALIGN 2
_LBB0_1
        ldr	r2, [r0]
        cmp	r2, r1
        it	eq
        bxeq	lr
_LBB0_2
        ldr	r0, [r0, #4]
_LBB0_3
        cmp	r0, #0
        bne	_LBB0_1
        bx	lr
_Lfunc_end0
        ALIGN 2
algorithm_singly_linked_list_operations_insert_after
        mov	r2, r0
        cmp	r0, r1
        mov.w	r0, #0
        it	ne
        cmpne	r2, #0
        bne	_LBB1_2
        bx	lr
_LBB1_2
        cmp	r1, #0
        itttt	ne
        ldrne	r0, [r2, #4]
        strne	r0, [r1, #4]
        strne	r1, [r2, #4]
        movne	r0, #1
        bx	lr
_Lfunc_end1
        ALIGN 2
algorithm_singly_linked_list_operations_remove_first
        cbz	r0, _LBB2_9
        ldr	r2, [r0]
        cbz	r2, _LBB2_9
        ldr	r3, [r2]
        cmp	r3, r1
        bne	_LBB2_4
        clz	r1, r2
        lsrs	r1, r1, #5
        b	_LBB2_7
        ALIGN 2
_LBB2_4
        mov	r0, r2
        ldr	r2, [r2, #4]
        cbz	r2, _LBB2_9
        ldr	r3, [r2]
        cmp	r3, r1
        bne	_LBB2_4
        clz	r1, r2
        lsrs	r1, r1, #5
        adds	r0, #4
_LBB2_7
        cmp	r1, #0
        mov.w	r1, #0
        bne	_LBB2_10
        ldr	r3, [r2, #4]
        str	r3, [r0]
        mov	r0, r2
        str	r1, [r2, #4]
        bx	lr
_LBB2_9
        movs	r1, #0
_LBB2_10
        mov	r0, r1
        bx	lr
_Lfunc_end2
        ALIGN
        END
