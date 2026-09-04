.syntax unified
.cpu cortex-m3
.thumb
.text
.global down
.global pat_alg_heap_sort_001
.balign 4
down:
        cmp	r0, #0
        it	eq
        bxeq	lr
_LBB0_1:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r11, [sp, #-4]!
        lsr.w	lr, r1, #1
        mov.w	r12, #2
        b	_LBB0_3
.balign 4
_LBB0_2:
        cmp	r3, r2
        mov	r2, r4
        beq	_LBB0_10
_LBB0_3:
        cmp	r2, lr
        bhs	_LBB0_10
        lsls	r3, r2, #1
        adds	r4, r3, #1
        cmp	r4, r1
        mov	r3, r2
        bhs	_LBB0_6
        ldr.w	r3, [r0, r4, lsl #2]
        ldr.w	r5, [r0, r2, lsl #2]
        cmp	r3, r5
        it	le
        movle	r4, r2
        mov	r3, r4
_LBB0_6:
        add.w	r4, r12, r2, lsl #1
        cmp	r4, r1
        bhs	_LBB0_8
        ldr.w	r5, [r0, r4, lsl #2]
        ldr.w	r6, [r0, r3, lsl #2]
        cmp	r5, r6
        it	gt
        movgt	r3, r4
_LBB0_8:
        cmp	r3, r2
        mov	r4, r2
        beq	_LBB0_2
        ldr.w	r4, [r0, r3, lsl #2]
        ldr.w	r5, [r0, r2, lsl #2]
        str.w	r4, [r0, r2, lsl #2]
        mov	r4, r3
        str.w	r5, [r0, r3, lsl #2]
        b	_LBB0_2
_LBB0_10:
        ldr	r11, [sp], #4
        pop.w	{r4, r5, r6, r7, lr}
        bx	lr
_Lfunc_end0:
.balign 4
pat_alg_heap_sort_001:
        cmp	r0, #0
        it	eq
        bxeq	lr
_LBB1_1:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r8, [sp, #-4]!
        lsrs.w	r8, r1, #1
        beq	_LBB1_13
        mov.w	lr, #2
        mov	r12, r8
        b	_LBB1_4
.balign 4
_LBB1_3:
        cmp.w	r12, #0
        beq	_LBB1_13
_LBB1_4:
        sub.w	r12, r12, #1
        mov	r3, r12
        b	_LBB1_6
.balign 4
_LBB1_5:
        cmp	r4, r3
        mov	r3, r5
        beq	_LBB1_3
_LBB1_6:
        cmp	r3, r8
        bhs	_LBB1_3
        lsls	r4, r3, #1
        adds	r5, r4, #1
        cmp	r5, r1
        mov	r4, r3
        bhs	_LBB1_9
        ldr.w	r4, [r0, r5, lsl #2]
        ldr.w	r6, [r0, r3, lsl #2]
        cmp	r4, r6
        it	le
        movle	r5, r3
        mov	r4, r5
_LBB1_9:
        add.w	r5, lr, r3, lsl #1
        cmp	r5, r1
        bhs	_LBB1_11
        ldr.w	r6, [r0, r5, lsl #2]
        ldr.w	r2, [r0, r4, lsl #2]
        cmp	r6, r2
        it	gt
        movgt	r4, r5
_LBB1_11:
        cmp	r4, r3
        mov	r5, r3
        beq	_LBB1_5
        ldr.w	r2, [r0, r4, lsl #2]
        ldr.w	r5, [r0, r3, lsl #2]
        str.w	r2, [r0, r3, lsl #2]
        str.w	r5, [r0, r4, lsl #2]
        mov	r5, r4
        b	_LBB1_5
_LBB1_13:
        cmp	r1, #2
        blo	_LBB1_25
        mov.w	r12, #2
        b	_LBB1_16
.balign 4
_LBB1_15:
        cmp	r1, #1
        bls	_LBB1_25
_LBB1_16:
        subs	r1, #1
        ldr.w	r2, [r0, r1, lsl #2]
        ldr	r3, [r0]
        str	r2, [r0]
        lsr.w	lr, r1, #1
        movs	r2, #0
        str.w	r3, [r0, r1, lsl #2]
        b	_LBB1_18
.balign 4
_LBB1_17:
        cmp	r4, r2
        mov	r2, r5
        beq	_LBB1_15
_LBB1_18:
        cmp	r2, lr
        bhs	_LBB1_15
        lsls	r6, r2, #1
        adds	r5, r6, #1
        cmp	r5, r1
        mov	r4, r2
        bhs	_LBB1_21
        ldr.w	r6, [r0, r5, lsl #2]
        ldr.w	r4, [r0, r2, lsl #2]
        cmp	r6, r4
        it	le
        movle	r5, r2
        mov	r4, r5
_LBB1_21:
        add.w	r5, r12, r2, lsl #1
        cmp	r5, r1
        bhs	_LBB1_23
        ldr.w	r6, [r0, r5, lsl #2]
        ldr.w	r3, [r0, r4, lsl #2]
        cmp	r6, r3
        it	gt
        movgt	r4, r5
_LBB1_23:
        cmp	r4, r2
        mov	r5, r2
        beq	_LBB1_17
        ldr.w	r3, [r0, r4, lsl #2]
        ldr.w	r5, [r0, r2, lsl #2]
        str.w	r3, [r0, r2, lsl #2]
        str.w	r5, [r0, r4, lsl #2]
        mov	r5, r4
        b	_LBB1_17
_LBB1_25:
        ldr	r8, [sp], #4
        pop.w	{r4, r5, r6, r7, lr}
        bx	lr
_Lfunc_end1:
.balign 4
