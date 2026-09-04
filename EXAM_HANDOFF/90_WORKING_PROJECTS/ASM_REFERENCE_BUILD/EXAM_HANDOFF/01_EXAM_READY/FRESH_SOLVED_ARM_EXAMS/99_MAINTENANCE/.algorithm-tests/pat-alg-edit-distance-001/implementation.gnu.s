.syntax unified
.cpu cortex-m3
.thumb
.text
.global pat_alg_edit_distance_001
.global pat_alg_edit_distance_001_full
.balign 4
pat_alg_edit_distance_001:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10, r11}
        sub	sp, #20
        cmp	r0, #0
        mov.w	r12, #-1
        str	r3, [sp, #16]
        str	r2, [sp, #4]
        it	ne
        cmpne	r1, #0
        bne	_LBB0_2
_LBB0_1:
        mov	r0, r12
        add	sp, #20
        pop.w	{r8, r9, r10, r11}
        pop	{r4, r5, r6, r7, pc}
_LBB0_2:
        ldr	r6, [r7, #8]
        cmp	r6, #0
        beq	_LBB0_1
        ldr	r2, [r7, #12]
        cmp	r2, #0
        beq	_LBB0_1
        movw	r3, #65534
        ldr	r2, [sp, #16]
        movt	r3, #16383
        cmp	r2, r3
        bhi	_LBB0_1
        ldr	r2, [sp, #4]
        adds	r3, r2, #1
        beq	_LBB0_1
        ldr	r2, [r7, #12]
        cmp	r2, r6
        beq	_LBB0_1
        ldr	r2, [sp, #16]
        movs	r3, #0
        add.w	r11, r2, #1
.balign 4
_LBB0_8:
        str.w	r3, [r6, r3, lsl #2]
        adds	r3, #1
        cmp	r11, r3
        bne	_LBB0_8
        ldr	r2, [sp, #4]
        cmp	r2, #0
        beq	_LBB0_17
        sub.w	r12, r0, #1
        ldr	r0, [r7, #12]
        mov.w	r10, #1
        subs	r0, #4
        str	r0, [sp, #12]
        ldr	r0, [r7, #8]
        subs	r0, #4
        str	r0, [sp, #8]
        subs	r0, r1, #1
        str	r0, [sp]
.balign 4
_LBB0_11:
        ldr	r0, [sp, #16]
        cmp	r0, #0
        ldr	r0, [r7, #12]
        str.w	r10, [r0]
        beq	_LBB0_14
        ldr	r5, [r0]
        ldr	r6, [sp]
        ldrd	r4, r9, [sp, #8]
        ldr	r3, [sp, #16]
.balign 4
_LBB0_13:
        ldr	lr, [r4, #4]!
        ldrb.w	r2, [r12, r10]
        ldr.w	r8, [r4, #4]
        ldrb	r1, [r6, #1]!
        add.w	r0, r8, #1
        adds	r5, #1
        cmp	r2, r1
        it	ne
        addne.w	lr, lr, #1
        cmp	r0, r5
        it	lo
        movlo	r5, r0
        cmp	r5, lr
        it	hs
        movhs	r5, lr
        str.w	r5, [r9, #8]
        subs	r3, #1
        add.w	r9, r9, #4
        bne	_LBB0_13
_LBB0_14:
        ldrd	r4, r3, [sp, #8]
        mov	r5, r11
.balign 4
_LBB0_15:
        ldr	r0, [r3, #4]!
        subs	r5, #1
        str	r0, [r4, #4]!
        bne	_LBB0_15
        ldr	r0, [sp, #4]
        cmp	r10, r0
        add.w	r10, r10, #1
        bne	_LBB0_11
_LBB0_17:
        ldr	r0, [sp, #16]
        ldr	r1, [r7, #8]
        ldr.w	r12, [r1, r0, lsl #2]
        b	_LBB0_1
_Lfunc_end0:
.balign 4
pat_alg_edit_distance_001_full:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10, r11}
        sub	sp, #28
        str	r3, [sp, #16]
        adds.w	lr, r3, #1
        mov.w	r3, #0
        mov	r6, r2
        adc	r3, r3, #0
        adds	r4, r2, #1
        mov.w	r12, #-1
        str	r6, [sp, #8]
        beq.w	_LBB1_18
        cmp	r3, #0
        bne.w	_LBB1_18
        cmp	r0, #0
        beq.w	_LBB1_18
        cmp	r1, #0
        beq.w	_LBB1_18
        ldr.w	r8, [r7, #8]
        cmp.w	r8, #0
        beq	_LBB1_18
        ldr	r3, [r7, #12]
        mul	r6, lr, r4
        cmp	r6, r3
        bhi	_LBB1_18
        mvn	r3, #-1073741824
        udiv	r3, r3, lr
        cmp	r4, r3
        bhi	_LBB1_18
        ldr	r2, [sp, #16]
        movs	r3, #4
        add.w	r3, r3, r2, lsl #2
        movs	r6, #0
        mov	r5, r8
.balign 4
_LBB1_8:
        str	r6, [r5]
        adds	r6, #1
        cmp	r4, r6
        add	r5, r3
        bne	_LBB1_8
        ldr	r2, [sp, #16]
        movs	r6, #0
        adds	r3, r2, #1
        str.w	lr, [sp]
.balign 4
_LBB1_10:
        str.w	r6, [r8, r6, lsl #2]
        adds	r6, #1
        cmp	r3, r6
        bne	_LBB1_10
        ldr	r2, [sp, #8]
        cmp	r2, #0
        beq	_LBB1_17
        subs	r1, #1
        ldr	r2, [sp, #16]
        str	r1, [sp, #4]
        movs	r1, #4
        add.w	r1, r1, r2, lsl #2
        str	r1, [sp, #12]
        ldr	r1, [r7, #8]
        mov.w	r9, #0
        subs	r1, #4
        str	r1, [sp, #24]
        movs	r1, #8
        add.w	r10, r1, r2, lsl #2
        movs	r1, #1
        str	r1, [sp, #20]
        b	_LBB1_14
.balign 4
_LBB1_13:
        ldr	r1, [sp, #8]
        ldr	r2, [sp, #20]
        ldr	r3, [sp, #24]
        cmp	r2, r1
        add.w	r1, r2, #1
        ldr	r2, [sp, #12]
        add.w	r9, r9, #1
        add	r3, r2
        strd	r1, r3, [sp, #20]
        beq	_LBB1_17
_LBB1_14:
        ldr	r1, [sp, #16]
        cmp	r1, #0
        beq	_LBB1_13
        ldr	r2, [sp, #12]
        add.w	r1, r9, #1
        mul	r3, r2, r1
        ldr	r1, [sp, #20]
        ldr.w	r12, [sp, #4]
        sub.w	lr, r1, #1
        ldr	r1, [r7, #8]
        ldr.w	r11, [sp, #24]
        ldr	r5, [r1, r3]
        ldr	r3, [sp, #16]
.balign 4
_LBB1_16:
        ldr.w	r8, [r11, #8]
        ldrb.w	r6, [r0, lr]
        ldrb	r1, [r12, #1]!
        add.w	r4, r8, #1
        add.w	r8, r11, r10
        adds	r5, #1
        ldr	r2, [r11, #4]!
        cmp	r6, r1
        it	ne
        addne	r2, #1
        cmp	r4, r5
        it	lo
        movlo	r5, r4
        cmp	r5, r2
        it	hs
        movhs	r5, r2
        subs	r3, #1
        str.w	r5, [r8, #4]
        bne	_LBB1_16
        b	_LBB1_13
_LBB1_17:
        ldr	r0, [sp, #8]
        ldr	r1, [sp]
        muls	r0, r1, r0
        ldr	r1, [r7, #8]
        add.w	r0, r1, r0, lsl #2
        ldr	r1, [sp, #16]
        ldr.w	r12, [r0, r1, lsl #2]
_LBB1_18:
        mov	r0, r12
        add	sp, #28
        pop.w	{r8, r9, r10, r11}
        pop	{r4, r5, r6, r7, pc}
_Lfunc_end1:
.balign 4
