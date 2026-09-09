; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT qs
        EXPORT pat_alg_quicksort_001
        ALIGN 2
qs
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10, r11}
        sub	sp, #4
        mov	r9, r2
        mov	r8, r0
        sub.w	r10, r0, #8
        mov	r11, r1
        b	_LBB0_2
        ALIGN 2
_LBB0_1
        cmp	r11, r9
        mov	r1, r11
        bge	_LBB0_13
_LBB0_2
        subs.w	r0, r9, r1
        mov	r2, r9
        bge	_LBB0_5
_LBB0_3
        cmp	r2, r1
        ble	_LBB0_1
        mov	r0, r8
        bl	qs
        b	_LBB0_1
        ALIGN 2
_LBB0_5
        add.w	r0, r0, r0, lsr #31
        mvn	r2, #2
        and.w	r0, r2, r0, lsl #1
        add	r0, r8
        ldr.w	r12, [r0, r1, lsl #2]
        mov	r11, r1
        mov	r3, r9
        b	_LBB0_7
        ALIGN 2
_LBB0_6
        cmp	r11, r2
        mov	r3, r2
        bgt	_LBB0_3
_LBB0_7
        add.w	r6, r10, r11, lsl #2
        mov	r4, r11
        ALIGN 2
_LBB0_8
        ldr	r5, [r6, #8]
        adds	r4, #1
        cmp	r5, r12
        add.w	r6, r6, #4
        blt	_LBB0_8
        sub.w	r11, r4, #1
        ALIGN 2
_LBB0_10
        ldr.w	r0, [r8, r3, lsl #2]
        subs	r3, #1
        cmp	r0, r12
        bgt	_LBB0_10
        adds	r2, r3, #1
        cmp	r11, r2
        bgt	_LBB0_6
        add.w	r2, r8, r3, lsl #2
        str	r0, [r6, #4]
        str	r5, [r2, #4]
        mov	r2, r3
        mov	r11, r4
        b	_LBB0_6
_LBB0_13
        add	sp, #4
        pop.w	{r8, r9, r10, r11}
        pop	{r4, r5, r6, r7, pc}
_Lfunc_end0
        ALIGN 2
pat_alg_quicksort_001
        cmp	r0, #0
        it	eq
        bxeq	lr
_LBB1_1
        cmp	r1, #1
        blt	_LBB1_3
        subs	r2, r1, #1
        movs	r1, #0
        b	qs
_LBB1_3
        bx	lr
_Lfunc_end1
        ALIGN
        END
