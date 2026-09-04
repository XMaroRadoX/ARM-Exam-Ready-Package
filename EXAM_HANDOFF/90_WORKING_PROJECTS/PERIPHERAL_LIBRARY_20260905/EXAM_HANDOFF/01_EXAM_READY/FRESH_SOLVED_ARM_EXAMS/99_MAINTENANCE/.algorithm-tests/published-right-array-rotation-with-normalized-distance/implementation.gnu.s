.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_right_array_rotation_with_normalized_distance
.global algorithm_right_array_rotation_with_normalized_distance_right
.global algorithm_right_array_rotation_with_normalized_distance_with_scratch
.balign 4
algorithm_right_array_rotation_with_normalized_distance:
        cmp	r0, #0
        beq	_LBB0_13
        cmp	r1, #2
        it	lo
        bxlo	lr
_LBB0_2:
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        udiv	r3, r2, r1
        mls	lr, r3, r1, r2
        cmp.w	lr, #0
        beq	_LBB0_12
        subs.w	r3, lr, #1
        beq	_LBB0_6
        movs	r2, #0
.balign 4
_LBB0_5:
        ldr.w	r12, [r0, r3, lsl #2]
        ldr.w	r4, [r0, r2, lsl #2]
        str.w	r12, [r0, r2, lsl #2]
        str.w	r4, [r0, r3, lsl #2]
        adds	r2, #1
        subs	r3, #1
        cmp	r2, r3
        blo	_LBB0_5
_LBB0_6:
        subs	r3, r1, #1
        cmp	lr, r3
        bhs	_LBB0_9
        sub.w	r12, r0, #4
.balign 4
_LBB0_8:
        ldr.w	r2, [r12, r1, lsl #2]
        ldr.w	r4, [r0, lr, lsl #2]
        str.w	r2, [r0, lr, lsl #2]
        add.w	lr, lr, #1
        subs	r2, r1, #2
        str.w	r4, [r12, r1, lsl #2]
        subs	r1, #1
        cmp	lr, r2
        blo	_LBB0_8
_LBB0_9:
        cbz	r3, _LBB0_12
        movs	r1, #0
.balign 4
_LBB0_11:
        ldr.w	r2, [r0, r3, lsl #2]
        ldr.w	r4, [r0, r1, lsl #2]
        str.w	r2, [r0, r1, lsl #2]
        str.w	r4, [r0, r3, lsl #2]
        adds	r1, #1
        subs	r3, #1
        cmp	r1, r3
        blo	_LBB0_11
_LBB0_12:
        pop.w	{r4, r6, r7, lr}
_LBB0_13:
        bx	lr
_Lfunc_end0:
.balign 4
algorithm_right_array_rotation_with_normalized_distance_right:
        cmp	r1, #0
        it	eq
        bxeq	lr
_LBB1_1:
        cmp	r0, #0
        it	ne
        cmpne	r1, #1
        bne	_LBB1_3
        bx	lr
_LBB1_3:
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        udiv	r3, r2, r1
        muls	r3, r1, r3
        subs	r2, r3, r2
        add	r2, r1
        udiv	r3, r2, r1
        mls	lr, r3, r1, r2
        cmp.w	lr, #0
        beq	_LBB1_13
        subs.w	r3, lr, #1
        beq	_LBB1_7
        movs	r2, #0
.balign 4
_LBB1_6:
        ldr.w	r12, [r0, r3, lsl #2]
        ldr.w	r4, [r0, r2, lsl #2]
        str.w	r12, [r0, r2, lsl #2]
        str.w	r4, [r0, r3, lsl #2]
        adds	r2, #1
        subs	r3, #1
        cmp	r2, r3
        blo	_LBB1_6
_LBB1_7:
        subs	r3, r1, #1
        cmp	lr, r3
        bhs	_LBB1_10
        sub.w	r12, r0, #4
.balign 4
_LBB1_9:
        ldr.w	r2, [r12, r1, lsl #2]
        ldr.w	r4, [r0, lr, lsl #2]
        str.w	r2, [r0, lr, lsl #2]
        add.w	lr, lr, #1
        subs	r2, r1, #2
        str.w	r4, [r12, r1, lsl #2]
        subs	r1, #1
        cmp	lr, r2
        blo	_LBB1_9
_LBB1_10:
        cbz	r3, _LBB1_13
        movs	r1, #0
.balign 4
_LBB1_12:
        ldr.w	r2, [r0, r3, lsl #2]
        ldr.w	r4, [r0, r1, lsl #2]
        str.w	r2, [r0, r1, lsl #2]
        str.w	r4, [r0, r3, lsl #2]
        adds	r1, #1
        subs	r3, #1
        cmp	r1, r3
        blo	_LBB1_12
_LBB1_13:
        pop.w	{r4, r6, r7, lr}
        bx	lr
_Lfunc_end1:
.balign 4
algorithm_right_array_rotation_with_normalized_distance_with_scratch:
        cmp	r0, r3
        mov.w	r12, #0
        it	ne
        cmpne	r0, #0
        bne	_LBB2_2
_LBB2_1:
        mov	r0, r12
        bx	lr
_LBB2_2:
        cmp	r3, #0
        beq	_LBB2_1
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        ldr.w	lr, [r7, #8]
        cmp	lr, r1
        blo	_LBB2_10
        cbz	r1, _LBB2_9
        udiv	r12, r2, r1
        mls	r12, r12, r1, r2
        movs	r2, #0
        sub.w	lr, r1, r12
.balign 4
_LBB2_6:
        mov	r4, r12
        cmp	r2, lr
        it	hs
        rsbhs.w	r4, lr, #0
        add.w	r4, r0, r4, lsl #2
        ldr.w	r4, [r4, r2, lsl #2]
        str.w	r4, [r3, r2, lsl #2]
        adds	r2, #1
        cmp	r1, r2
        bne	_LBB2_6
        subs	r0, #4
        subs	r2, r3, #4
.balign 4
_LBB2_8:
        ldr	r3, [r2, #4]!
        subs	r1, #1
        str	r3, [r0, #4]!
        bne	_LBB2_8
_LBB2_9:
        mov.w	r12, #1
_LBB2_10:
        pop.w	{r4, r6, r7, lr}
        mov	r0, r12
        bx	lr
_Lfunc_end2:
.balign 4
