; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_algorithm_pat_alg_bubble_sort_001_assembly
        ALIGN 2
algorithm_algorithm_pat_alg_bubble_sort_001_assembly
        cbz	r0, _LBB0_7
        cmp	r1, #2
        it	lo
        bxlo	lr
_LBB0_2
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        ALIGN 2
_LBB0_3
        subs	r1, #1
        movs	r2, #0
        mov.w	r12, #0
        ALIGN 2
_LBB0_4
        add.w	lr, r0, r2, lsl #2
        ldr.w	r3, [r0, r2, lsl #2]
        ldr.w	r4, [lr, #4]
        adds	r2, #1
        cmp	r3, r4
        itt	gt
        strdgt	r4, r3, [lr]
        movgt.w	r12, #1
        cmp	r1, r2
        bne	_LBB0_4
        cmp.w	r12, #0
        it	ne
        cmpne	r1, #1
        bhi	_LBB0_3
        pop.w	{r4, r6, r7, lr}
_LBB0_7
        bx	lr
_Lfunc_end0
        ALIGN
        END
