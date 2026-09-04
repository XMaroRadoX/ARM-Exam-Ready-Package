.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_frequency_table_and_deterministic_mode
.balign 4
algorithm_frequency_table_and_deterministic_mode:
        cmp	r3, #0
        itt	eq
        moveq	r0, #0
        bxeq	lr
_LBB0_1:
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        clz	r4, r0
        lsr.w	r12, r4, #5
        cmp	r1, #0
        mov	r4, r1
        it	ne
        movne	r4, #1
        tst.w	r12, r4
        mov.w	r12, #0
        bne	_LBB0_14
        subw	r4, r2, #257
        cmn.w	r4, #256
        blo	_LBB0_14
        cbz	r2, _LBB0_6
        sub.w	r12, r3, #4
        mov.w	lr, #0
        mov	r4, r2
.balign 4
_LBB0_5:
        subs	r4, #1
        str	lr, [r12, #4]!
        bne	_LBB0_5
_LBB0_6:
        cbnz	r1, _LBB0_11
_LBB0_7:
        cmp	r2, #2
        blo	_LBB0_13
        rsb.w	lr, r2, #0
        adds	r1, r3, #4
        movs	r2, #0
        mov.w	r12, #0
.balign 4
_LBB0_9:
        ldr.w	r4, [r1, r2, lsl #2]
        ldr.w	r0, [r3, r12, lsl #2]
        adds	r2, #1
        cmp	r4, r0
        add.w	r0, lr, r2
        it	hi
        movhi	r12, r2
        adds	r0, #1
        bne	_LBB0_9
        b	_LBB0_14
.balign 4
_LBB0_10:
        subs	r1, #1
        beq	_LBB0_7
_LBB0_11:
        ldrb	r12, [r0], #1
        cmp	r12, r2
        bhs	_LBB0_10
        ldr.w	r4, [r3, r12, lsl #2]
        adds	r4, #1
        str.w	r4, [r3, r12, lsl #2]
        b	_LBB0_10
_LBB0_13:
        mov.w	r12, #0
_LBB0_14:
        pop.w	{r4, r6, r7, lr}
        mov	r0, r12
        bx	lr
_Lfunc_end0:
.balign 4
