.syntax unified
.cpu cortex-m3
.thumb
.text
.global visit
.global algorithm_recursive_dfs_with_depth_contract
.balign 4
visit:
        push	{r4, r5, r6, r7, lr}
        add	r7, sp, #12
        push.w	{r8, r9, r10, r11}
        sub	sp, #4
        mov.w	r6, #0
        cbz	r0, _LBB0_5
        mov	r9, r3
        cbz	r3, _LBB0_5
        mov	r5, r1
        cmp	r2, r1
        bhs	_LBB0_5
        mov	r8, r0
        ldr	r0, [r7, #8]
        subs	r1, r0, #1
        cmp	r1, r5
        bhs	_LBB0_5
        ldrb.w	r1, [r9, r2]
        cbz	r1, _LBB0_6
_LBB0_5:
        mov	r0, r6
        add	sp, #4
        pop.w	{r8, r9, r10, r11}
        pop	{r4, r5, r6, r7, pc}
_LBB0_6:
        movs	r6, #1
        cmp	r5, #0
        strb.w	r6, [r9, r2]
        beq	_LBB0_5
        mla	r10, r2, r5, r8
        add.w	r11, r0, #1
        movs	r4, #0
        b	_LBB0_9
.balign 4
_LBB0_8:
        adds	r4, #1
        cmp	r5, r4
        beq	_LBB0_5
_LBB0_9:
        ldrb.w	r0, [r10, r4]
        cmp	r0, #0
        beq	_LBB0_8
        ldrb.w	r0, [r9, r4]
        cmp	r0, #0
        bne	_LBB0_8
        mov	r0, r8
        mov	r1, r5
        mov	r2, r4
        mov	r3, r9
        str.w	r11, [sp]
        bl	visit
        add	r6, r0
        b	_LBB0_8
_Lfunc_end0:
.balign 4
algorithm_recursive_dfs_with_depth_contract:
        cmp	r0, #0
        it	ne
        cmpne	r3, #0
        beq	_LBB1_2
        cmp.w	r1, #256
        it	ls
        cmpls	r2, r1
        blo	_LBB1_3
_LBB1_2:
        movs	r0, #0
        bx	lr
_LBB1_3:
        push	{r7, lr}
        mov	r7, sp
        sub	sp, #8
        mov.w	r12, #1
        str.w	r12, [sp]
        bl	visit
        add	sp, #8
        pop	{r7, pc}
_Lfunc_end1:
.balign 4
