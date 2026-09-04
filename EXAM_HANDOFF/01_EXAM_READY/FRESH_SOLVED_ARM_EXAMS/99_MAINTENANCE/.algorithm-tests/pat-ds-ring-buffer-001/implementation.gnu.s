.syntax unified
.cpu cortex-m3
.thumb
.text
.global pat_ds_ring_buffer_001
.balign 4
pat_ds_ring_buffer_001:
        cbz	r0, _LBB0_10
        ldr.w	r12, [r0]
        cmp.w	r12, #0
        beq	_LBB0_10
        mov.w	r3, #0
        cbz	r2, _LBB0_11
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        str	r8, [sp, #-4]!
        ldr.w	lr, [r0, #4]
        cmp.w	lr, #0
        beq	_LBB0_16
        mov	r3, r0
        ldr	r4, [r3, #8]!
        cmp	r4, lr
        bhs	_LBB0_15
        mov	r5, r0
        ldr	r6, [r5, #12]!
        cmp	r6, lr
        bhs	_LBB0_15
        ldr.w	r8, [r0, #16]
        cmp	r8, lr
        bhi	_LBB0_15
        cbz	r1, _LBB0_12
        cmp	r8, lr
        beq	_LBB0_15
        ldr	r1, [r2]
        str.w	r1, [r12, r4, lsl #2]
        movs	r1, #1
        b	_LBB0_14
_LBB0_10:
        movs	r3, #0
_LBB0_11:
        mov	r0, r3
        bx	lr
_LBB0_12:
        cmp.w	r8, #0
        beq	_LBB0_15
        ldr.w	r1, [r12, r6, lsl #2]
        mov	r3, r5
        str	r1, [r2]
        mov.w	r1, #-1
_LBB0_14:
        ldr	r2, [r3]
        ldr	r6, [r0, #4]
        adds	r2, #1
        udiv	r5, r2, r6
        mls	r2, r5, r6, r2
        ldr	r6, [r0, #16]
        str	r2, [r3]
        add	r1, r6
        movs	r3, #1
        str	r1, [r0, #16]
        b	_LBB0_16
_LBB0_15:
        movs	r3, #0
_LBB0_16:
        ldr	r8, [sp], #4
        pop.w	{r4, r5, r6, r7, lr}
        mov	r0, r3
        bx	lr
_Lfunc_end0:
.balign 4
