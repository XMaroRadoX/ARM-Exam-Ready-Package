.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_dijkstra_shortest_path
.balign 4
algorithm_dijkstra_shortest_path:
        cmp	r0, #0
        mov.w	r12, #0
        it	ne
        cmpne	r3, #0
        bne	_LBB0_2
        mov	r0, r12
        bx	lr
_LBB0_2:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10, r11}
        ldr.w	lr, [r7, #8]
        cmp.w	lr, #0
        beq	_LBB0_22
        mov.w	r12, #0
        cmp.w	r12, r1, lsr #15
        bne	_LBB0_22
        cmp	r2, r1
        bhs	_LBB0_22
        movs	r6, #0
        mov.w	r5, #-1
        movs	r4, #0
.balign 4
_LBB0_6:
        str.w	r5, [r3, r4, lsl #2]
        strb.w	r6, [lr, r4]
        adds	r4, #1
        cmp	r1, r4
        bne	_LBB0_6
        mov.w	r10, #0
        mov.w	r9, #0
        str.w	r10, [r3, r2, lsl #2]
.balign 4
_LBB0_8:
        movs	r6, #0
        mov.w	r5, #-1
        mov	r12, r1
        b	_LBB0_10
.balign 4
_LBB0_9:
        adds	r6, #1
        cmp	r1, r6
        beq	_LBB0_12
_LBB0_10:
        ldrb.w	r2, [lr, r6]
        cmp	r2, #0
        bne	_LBB0_9
        ldr.w	r2, [r3, r6, lsl #2]
        cmp	r2, r5
        itt	lo
        movlo	r12, r6
        movlo	r5, r2
        b	_LBB0_9
.balign 4
_LBB0_12:
        cmp	r12, r1
        beq	_LBB0_21
        movs	r2, #1
        strb.w	r2, [lr, r12]
        mul	r2, r12, r1
        add.w	r11, r0, r2, lsl #2
        movs	r5, #0
        b	_LBB0_15
.balign 4
_LBB0_14:
        adds	r5, #1
        cmp	r1, r5
        beq	_LBB0_19
_LBB0_15:
        ldr.w	r4, [r11, r5, lsl #2]
        cmp	r4, #0
        beq	_LBB0_14
        ldr.w	r2, [r3, r12, lsl #2]
        adds	r6, r4, r2
        adc	r6, r10, #0
        adds.w	r8, r2, #1
        beq	_LBB0_14
        cmp	r6, #0
        bne	_LBB0_14
        ldr.w	r6, [r3, r5, lsl #2]
        add	r2, r4
        cmp	r2, r6
        it	lo
        strlo.w	r2, [r3, r5, lsl #2]
        b	_LBB0_14
.balign 4
_LBB0_19:
        cmp	r12, r1
        mov.w	r12, #1
        beq	_LBB0_22
        add.w	r9, r9, #1
        cmp	r9, r1
        bne	_LBB0_8
        b	_LBB0_22
_LBB0_21:
        mov.w	r12, #1
_LBB0_22:
        pop.w	{r8, r9, r10, r11}
        pop.w	{r4, r5, r6, r7, lr}
        mov	r0, r12
        bx	lr
_Lfunc_end0:
.balign 4
