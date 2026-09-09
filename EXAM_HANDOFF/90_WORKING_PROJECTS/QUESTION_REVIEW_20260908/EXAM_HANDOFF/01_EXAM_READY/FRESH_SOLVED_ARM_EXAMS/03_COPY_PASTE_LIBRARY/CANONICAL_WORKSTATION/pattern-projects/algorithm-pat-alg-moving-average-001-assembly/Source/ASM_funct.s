; Matching Cortex-M3 Thumb implementation generated from the repaired reference.c.
        AREA |.text.patterns|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT algorithm_algorithm_pat_alg_moving_average_001_assembly
        IMPORT __aeabi_ldivmod
        ALIGN 2
algorithm_algorithm_pat_alg_moving_average_001_assembly
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10, r11}
        sub	sp, #12
        mov.w	r11, #0
        str	r3, [sp, #8]
        cbz	r2, _LBB0_11
        mov	r9, r0
        cbz	r0, _LBB0_11
        ldr	r0, [sp, #8]
        cbz	r0, _LBB0_11
        mov	r5, r2
        mov	r10, r1
        cmp	r2, r1
        bhi	_LBB0_11
        cmp	r5, #0
        bmi	_LBB0_11
        sub.w	r0, r9, r5, lsl #2
        movs	r6, #0
        movs	r4, #0
        mov.w	r8, #0
        cmp.w	r10, #1
        it	ls
        movls.w	r10, #1
        str	r0, [sp, #4]
        b	_LBB0_7
        ALIGN 2
_LBB0_6
        cmp	r10, r8
        beq	_LBB0_11
_LBB0_7
        ldr.w	r0, [r9, r8, lsl #2]
        adds	r6, r6, r0
        adc.w	r4, r4, r0, asr #31
        cmp	r8, r5
        blo	_LBB0_9
        ldr	r0, [sp, #4]
        ldr.w	r0, [r0, r8, lsl #2]
        subs	r6, r6, r0
        sbc.w	r4, r4, r0, asr #31
_LBB0_9
        add.w	r8, r8, #1
        cmp	r8, r5
        blo	_LBB0_6
        mov	r0, r6
        mov	r1, r4
        mov	r2, r5
        movs	r3, #0
        bl	__aeabi_ldivmod
        ldr	r1, [sp, #8]
        str.w	r0, [r1, r11, lsl #2]
        add.w	r11, r11, #1
        b	_LBB0_6
_LBB0_11
        mov	r0, r11
        add	sp, #12
        pop.w	{r8, r9, r10, r11}
        pop	{r4, r5, r6, r7, pc}
_Lfunc_end0
        ALIGN
        END
