.syntax unified
.cpu cortex-m3
.thumb
.text
.global pat_alg_horner_001
.global pat_alg_horner_001_checked
.extern __aeabi_ldivmod
.extern __aeabi_uldivmod
.balign 4
pat_alg_horner_001:
        mov	r12, r0
        cmp	r0, #0
        mov.w	r0, #0
        beq	_LBB0_5
        mov.w	r3, #0
        cbz	r1, _LBB0_6
        push	{r4, r5, r7, lr}
        add	r7, sp, #8
        sub.w	r12, r12, #4
        movs	r0, #0
        asr.w	lr, r2, #31
        movs	r3, #0
.balign 4
_LBB0_3:
        umull	r4, r5, r0, r2
        mla	r0, r0, lr, r5
        ldr.w	r5, [r12, r1, lsl #2]
        mla	r3, r3, r2, r0
        subs	r1, #1
        adds	r0, r4, r5
        adc.w	r3, r3, r5, asr #31
        cmp	r1, #0
        bne	_LBB0_3
        pop.w	{r4, r5, r7, lr}
        mov	r1, r3
        bx	lr
_LBB0_5:
        movs	r3, #0
_LBB0_6:
        mov	r1, r3
        bx	lr
_Lfunc_end0:
.balign 4
pat_alg_horner_001_checked:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10, r11}
        sub	sp, #4
        cmp	r3, #0
        beq.w	_LBB1_24
        mov	r6, r2
        mov	r5, r1
        mov.w	r10, #0
        cbnz	r0, _LBB1_3
        cmp	r5, #0
        bne.w	_LBB1_25
_LBB1_3:
        sub.w	r11, r0, #4
        adds	r4, r6, #1
        mov.w	r8, #0
        mov.w	r9, #0
        str	r3, [sp]
        b	_LBB1_6
.balign 4
_LBB1_4:
        movs	r0, #0
_LBB1_5:
        cmp	r0, #0
        sub.w	r5, r5, #1
        beq	_LBB1_24
_LBB1_6:
        cmp	r5, #0
        beq	_LBB1_26
        cmp	r4, #0
        beq	_LBB1_17
        cmp	r6, #1
        blt	_LBB1_11
        mov.w	r0, #-1
        mvn	r1, #-2147483648
        mov	r2, r6
        movs	r3, #0
        bl	__aeabi_uldivmod
        subs.w	r0, r0, r8
        sbcs.w	r0, r1, r9
        blt	_LBB1_24
        movs	r0, #0
        mov.w	r1, #-2147483648
        mov	r2, r6
        movs	r3, #0
        bl	__aeabi_ldivmod
        subs.w	r0, r8, r0
        sbcs.w	r0, r9, r1
        blt	_LBB1_24
_LBB1_11:
        cmn.w	r6, #2
        bgt	_LBB1_16
        subs.w	r0, r8, #1
        sbcs	r0, r9, #0
        blt	_LBB1_14
        asrs	r3, r6, #31
        movs	r0, #0
        mov.w	r1, #-2147483648
        mov	r2, r6
        bl	__aeabi_ldivmod
        subs.w	r0, r0, r8
        sbcs.w	r0, r1, r9
        blt	_LBB1_24
_LBB1_14:
        cmp.w	r9, #-1
        bgt	_LBB1_16
        asrs	r3, r6, #31
        mov.w	r0, #-1
        mvn	r1, #-2147483648
        mov	r2, r6
        bl	__aeabi_ldivmod
        subs.w	r0, r8, r0
        sbcs.w	r0, r9, r1
        blt	_LBB1_24
.balign 4
_LBB1_16:
        umull	r0, r1, r8, r6
        asrs	r2, r6, #31
        mla	r1, r8, r2, r1
        mov	r8, r0
        mla	r9, r9, r6, r1
        b	_LBB1_19
.balign 4
_LBB1_17:
        mov.w	r0, #-2147483648
        eor.w	r0, r0, r9
        orrs.w	r0, r0, r8
        beq	_LBB1_24
        rsbs.w	r8, r8, #0
        sbc.w	r9, r10, r9
_LBB1_19:
        ldr.w	r0, [r11, r5, lsl #2]
        cmp	r0, #1
        blt	_LBB1_21
        mvns	r1, r0
        subs.w	r1, r1, r8
        mvn	r1, #-2147483648
        sbcs.w	r1, r1, r9
        blt	_LBB1_4
_LBB1_21:
        cmp.w	r0, #-1
        bgt	_LBB1_23
        rsbs	r1, r0, #0
        mov.w	r2, #-2147483648
        sbc.w	r2, r2, r0, asr #31
        subs.w	r1, r8, r1
        sbcs.w	r1, r9, r2
        blt.w	_LBB1_4
_LBB1_23:
        adds.w	r8, r8, r0
        adc.w	r9, r9, r0, asr #31
        movs	r0, #1
        b	_LBB1_5
_LBB1_24:
        mov.w	r10, #0
_LBB1_25:
        mov	r0, r10
        add	sp, #4
        pop.w	{r8, r9, r10, r11}
        pop	{r4, r5, r6, r7, pc}
_LBB1_26:
        ldr	r0, [sp]
        mov.w	r10, #1
        strd	r8, r9, [r0]
        b	_LBB1_25
_Lfunc_end1:
.balign 4
