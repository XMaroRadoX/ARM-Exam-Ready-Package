; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT pat_alg_array_reversal_001
        ALIGN 2
pat_alg_array_reversal_001
        cmp	r0, #0
        it	ne
        lsrsne.w	r2, r1, #1
        beq	_LBB0_3
        subs	r0, #4
        add.w	r1, r0, r1, lsl #2
        ALIGN 2
_LBB0_2
        ldr	r12, [r0, #4]!
        ldr	r3, [r1]
        subs	r2, #1
        str	r3, [r0]
        str	r12, [r1], #-4
        bne	_LBB0_2
_LBB0_3
        bx	lr
_Lfunc_end0
        ALIGN
        END
