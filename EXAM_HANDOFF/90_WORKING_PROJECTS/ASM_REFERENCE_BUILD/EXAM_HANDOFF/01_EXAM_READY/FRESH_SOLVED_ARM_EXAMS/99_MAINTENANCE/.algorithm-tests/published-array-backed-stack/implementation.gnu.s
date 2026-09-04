.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_array_backed_stack
.balign 4
algorithm_array_backed_stack:
        mov	r12, r0
        cmp	r0, #0
        mov.w	r0, #0
        it	ne
        cmpne	r2, #0
        bne	_LBB0_2
        bx	lr
_LBB0_2:
        push	{r7, lr}
        mov	r7, sp
        ldr.w	lr, [r7, #8]
        cmp.w	lr, #0
        beq	_LBB0_5
        ldr	r0, [r2]
        cmp	r0, r1
        bls	_LBB0_6
        movs	r0, #0
_LBB0_5:
        pop.w	{r7, lr}
        bx	lr
_LBB0_6:
        cbz	r3, _LBB0_9
        cmp	r0, r1
        bhs	_LBB0_12
        ldr.w	r1, [lr]
        adds	r3, r0, #1
        str	r3, [r2]
        str.w	r1, [r12, r0, lsl #2]
        b	_LBB0_11
_LBB0_9:
        cbz	r0, _LBB0_12
        subs	r0, #1
        str	r0, [r2]
        ldr.w	r0, [r12, r0, lsl #2]
        str.w	r0, [lr]
_LBB0_11:
        movs	r0, #1
        pop.w	{r7, lr}
        bx	lr
_LBB0_12:
        movs	r0, #0
        pop.w	{r7, lr}
        bx	lr
_Lfunc_end0:
.balign 4
