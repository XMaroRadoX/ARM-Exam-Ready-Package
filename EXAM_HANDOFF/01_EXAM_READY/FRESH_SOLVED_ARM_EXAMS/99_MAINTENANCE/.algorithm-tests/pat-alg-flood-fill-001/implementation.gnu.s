.syntax unified
.cpu cortex-m3
.thumb
.text
.global pat_alg_flood_fill_001
.balign 4
pat_alg_flood_fill_001:
        cmp	r2, #0
        itt	eq
        moveq	r0, #0
        bxeq	lr
_LBB0_1:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10}
        mov	r12, r0
        umull	r0, r6, r2, r1
        cbz	r6, _LBB0_4
        movs	r0, #0
_LBB0_3:
        pop.w	{r8, r9, r10}
        pop	{r4, r5, r6, r7, pc}
_LBB0_4:
        ldrd	r8, lr, [r7, #8]
        movs	r0, #0
        cmp	r8, lr
        beq	_LBB0_3
        mul	r4, r2, r1
        cmp	r4, r3
        bls	_LBB0_3
        cmp.w	r12, #0
        beq	_LBB0_3
        ldr.w	r9, [r7, #16]
        cmp.w	r9, #0
        beq	_LBB0_3
        ldrb.w	r0, [r12, r3]
        cmp	r0, r8
        bne	_LBB0_19
        mov.w	r10, #1
        movs	r0, #0
        strb.w	lr, [r12, r3]
        str.w	r3, [r9]
        b	_LBB0_11
.balign 4
_LBB0_10:
        adds	r0, #1
        cmp	r0, r10
        bhs	_LBB0_3
_LBB0_11:
        ldr.w	r6, [r9, r0, lsl #2]
        cmp	r6, r2
        blo	_LBB0_13
        subs	r4, r6, r2
        ldrb.w	r5, [r12, r4]
        cmp	r5, r8
        ittt	eq
        strbeq.w	lr, [r12, r4]
        streq.w	r4, [r9, r10, lsl #2]
        addeq.w	r10, r10, #1
_LBB0_13:
        udiv	r4, r6, r2
        adds	r5, r4, #1
        cmp	r5, r1
        bhs	_LBB0_15
        adds	r5, r6, r2
        ldrb.w	r3, [r12, r5]
        cmp	r3, r8
        ittt	eq
        strbeq.w	lr, [r12, r5]
        streq.w	r5, [r9, r10, lsl #2]
        addeq.w	r10, r10, #1
_LBB0_15:
        mls	r4, r4, r2, r6
        cbz	r4, _LBB0_17
        subs	r5, r6, #1
        ldrb.w	r3, [r12, r5]
        cmp	r3, r8
        ittt	eq
        strbeq.w	lr, [r12, r5]
        streq.w	r5, [r9, r10, lsl #2]
        addeq.w	r10, r10, #1
_LBB0_17:
        adds	r3, r4, #1
        cmp	r3, r2
        bhs	_LBB0_10
        adds	r4, r6, #1
        ldrb.w	r3, [r12, r4]
        cmp	r3, r8
        ittt	eq
        strbeq.w	lr, [r12, r4]
        streq.w	r4, [r9, r10, lsl #2]
        addeq.w	r10, r10, #1
        b	_LBB0_10
_LBB0_19:
        movs	r0, #0
        pop.w	{r8, r9, r10}
        pop	{r4, r5, r6, r7, pc}
_Lfunc_end0:
.balign 4
