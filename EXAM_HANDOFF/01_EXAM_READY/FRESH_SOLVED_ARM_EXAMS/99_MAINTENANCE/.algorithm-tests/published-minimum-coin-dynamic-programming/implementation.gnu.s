.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_minimum_coin_dynamic_programming
.balign 4
algorithm_minimum_coin_dynamic_programming:
        cmp	r3, #0
        itt	eq
        moveq.w	r0, #-1
        bxeq	lr
_LBB0_1:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r11, [sp, #-4]!
        clz	r5, r0
        lsrs	r5, r5, #5
        cmp	r1, #0
        mov	r4, r1
        it	ne
        movne	r4, #1
        tst	r5, r4
        mov.w	r12, #-1
        bne	_LBB0_15
        movw	r5, #65534
        movt	r5, #16383
        cmp	r2, r5
        bhi	_LBB0_15
        add.w	r12, r2, #1
        movs	r4, #0
        mov.w	lr, #-1
.balign 4
_LBB0_4:
        str.w	lr, [r3, r4, lsl #2]
        adds	r4, #1
        cmp	r12, r4
        bne	_LBB0_4
        movs	r5, #0
        str	r5, [r3]
        cbz	r2, _LBB0_14
        mov.w	r12, #1
        b	_LBB0_8
.balign 4
_LBB0_7:
        cmp	r12, r2
        add.w	r12, r12, #1
        beq	_LBB0_14
_LBB0_8:
        cmp	r1, #0
        beq	_LBB0_7
        mov	lr, r0
        mov	r4, r1
        b	_LBB0_11
.balign 4
_LBB0_10:
        subs	r4, #1
        beq	_LBB0_7
_LBB0_11:
        ldrh	r5, [lr], #2
        cmp	r12, r5
        blo	_LBB0_10
        sub.w	r5, r12, r5
        ldr.w	r5, [r3, r5, lsl #2]
        adds	r5, #1
        bhs	_LBB0_10
        ldr.w	r6, [r3, r12, lsl #2]
        cmp	r5, r6
        it	lo
        strlo.w	r5, [r3, r12, lsl #2]
        b	_LBB0_10
_LBB0_14:
        ldr.w	r12, [r3, r2, lsl #2]
_LBB0_15:
        ldr	r11, [sp], #4
        pop.w	{r4, r5, r6, r7, lr}
        mov	r0, r12
        bx	lr
_Lfunc_end0:
.balign 4
