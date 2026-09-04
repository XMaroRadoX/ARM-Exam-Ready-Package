; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_overlap_safe_memory_movement
        ALIGN 2
algorithm_overlap_safe_memory_movement
        cmp	r0, #0
        it	ne
        cmpne	r1, #0
        bne	_LBB0_2
_LBB0_1
        bx	lr
_LBB0_2
        cmp	r0, r1
        bhs	_LBB0_6
        cmp	r2, #0
        beq	_LBB0_1
        subs	r3, r0, #1
        subs	r1, #1
        ALIGN 2
_LBB0_5
        ldrb	r12, [r1, #1]!
        subs	r2, #1
        strb	r12, [r3, #1]!
        bne	_LBB0_5
        b	_LBB0_1
_LBB0_6
        bls	_LBB0_1
        cmp	r2, #0
        it	eq
        bxeq	lr
_LBB0_8
        sub.w	r12, r0, #1
        subs	r1, #1
        ALIGN 2
_LBB0_9
        ldrb	r3, [r1, r2]
        strb.w	r3, [r12, r2]
        subs	r2, #1
        bne	_LBB0_9
        b	_LBB0_1
_Lfunc_end0
        ALIGN
        END
