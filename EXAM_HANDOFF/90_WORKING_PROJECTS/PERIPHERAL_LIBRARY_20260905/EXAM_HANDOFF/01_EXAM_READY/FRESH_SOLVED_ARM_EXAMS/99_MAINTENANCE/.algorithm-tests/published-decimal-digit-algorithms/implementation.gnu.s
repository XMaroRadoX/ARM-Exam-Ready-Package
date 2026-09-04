.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_decimal_digit_algorithms
.global algorithm_decimal_digit_algorithms_extract
.global algorithm_decimal_digit_algorithms_reconstruct
.global algorithm_decimal_digit_algorithms_is_palindrome
.global algorithm_decimal_digit_algorithms_kaprekar_4
.balign 4
algorithm_decimal_digit_algorithms:
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        movw	r12, #52429
        movs	r1, #0
        movt	r12, #52428
        mov.w	lr, #0
.balign 4
_LBB0_1:
        umull	r2, r3, r0, r12
        lsrs	r4, r3, #3
        add.w	r3, r4, r4, lsl #2
        sub.w	r3, r0, r3, lsl #1
        add.w	r2, lr, lr, lsl #2
        add	r1, r3
        add.w	lr, r3, r2, lsl #1
        cmp	r0, #9
        mov	r0, r4
        bhi	_LBB0_1
        uxth.w	r0, lr
        orr.w	r0, r0, r1, lsl #16
        pop	{r4, r6, r7, pc}
_Lfunc_end0:
.balign 4
algorithm_decimal_digit_algorithms_extract:
        push	{r4, r5, r7, lr}
        add	r7, sp, #8
        cmp	r1, #0
        mov.w	lr, #0
        it	ne
        cmpne	r2, #0
        bne	_LBB1_2
_LBB1_1:
        mov	r0, lr
        pop	{r4, r5, r7, pc}
_LBB1_2:
        movw	r12, #52429
        movs	r5, #0
        movt	r12, #52428
.balign 4
_LBB1_3:
        cmp	r2, r5
        beq	_LBB1_5
        umull	r3, r4, r0, r12
        lsrs	r3, r4, #3
        add.w	r4, r3, r3, lsl #2
        sub.w	r4, r0, r4, lsl #1
        add.w	lr, r5, #1
        strb	r4, [r1, r5]
        cmp	r0, #9
        mov	r0, r3
        mov	r5, lr
        bhi	_LBB1_3
        b	_LBB1_1
_LBB1_5:
        movs	r0, #0
        pop	{r4, r5, r7, pc}
_Lfunc_end1:
.balign 4
algorithm_decimal_digit_algorithms_reconstruct:
        cmp	r0, #0
        mov.w	r2, #0
        it	ne
        cmpne	r1, #0
        bne	_LBB2_2
        mov	r0, r2
        bx	lr
_LBB2_2:
        push	{r7, lr}
        mov	r7, sp
        subs	r1, #1
        mov.w	r12, #0
        movs	r2, #0
.balign 4
_LBB2_3:
        add.w	lr, r2, r2, lsl #2
        ldrb	r2, [r0, r1]
        subs	r1, #1
        adc	r3, r12, #0
        cmp	r0, #0
        add.w	r2, r2, lr, lsl #1
        it	ne
        cmpne	r3, #0
        bne	_LBB2_3
        pop.w	{r7, lr}
        mov	r0, r2
        bx	lr
_Lfunc_end2:
.balign 4
algorithm_decimal_digit_algorithms_is_palindrome:
        push	{r4, r5, r7, lr}
        add	r7, sp, #8
        movw	r12, #52429
        movs	r2, #0
        movt	r12, #52428
        mov.w	lr, #10
        mov	r1, r0
        movs	r3, #0
.balign 4
_LBB3_1:
        umull	r4, r5, r1, r12
        lsrs	r5, r5, #3
        add.w	r3, r3, r3, lsl #2
        add.w	r4, r5, r5, lsl #2
        lsls	r3, r3, #1
        sub.w	r4, r1, r4, lsl #1
        umlal	r4, r3, r2, lr
        cmp	r1, #9
        mov	r1, r5
        mov	r2, r4
        bhi	_LBB3_1
        eors	r0, r4
        orrs	r0, r3
        clz	r0, r0
        lsrs	r0, r0, #5
        pop	{r4, r5, r7, pc}
_Lfunc_end3:
.balign 4
algorithm_decimal_digit_algorithms_kaprekar_4:
        push	{r4, r6, r7, lr}
        add	r7, sp, #8
        sub	sp, #4
        movw	r12, #52429
        movs	r2, #0
        movt	r12, #52428
        mov	lr, sp
.balign 4
_LBB4_1:
        umull	r1, r3, r0, r12
        lsrs	r1, r3, #3
        add.w	r3, r1, r1, lsl #2
        sub.w	r0, r0, r3, lsl #1
        strb.w	r0, [lr, r2]
        adds	r2, #1
        cmp	r2, #4
        mov	r0, r1
        bne	_LBB4_1
        mov.w	r12, #0
        b	_LBB4_4
.balign 4
_LBB4_3:
        cmp.w	r12, #4
        beq	_LBB4_7
_LBB4_4:
        mov	r2, r12
        cmp.w	r12, #2
        add.w	r12, r12, #1
        bhi	_LBB4_3
        mov	r3, r12
.balign 4
_LBB4_6:
        ldrb.w	r0, [lr, r3]
        ldrb.w	r1, [lr, r2]
        cmp	r0, r1
        itt	lo
        strblo.w	r0, [lr, r2]
        strblo.w	r1, [lr, r3]
        adds	r3, #1
        cmp	r3, #4
        bne	_LBB4_6
        b	_LBB4_3
_LBB4_7:
        mov.w	r12, #0
        movs	r2, #3
        mov.w	r3, #-1
        movs	r4, #0
.balign 4
_LBB4_8:
        add.w	r1, lr, r3
        ldrb	r1, [r1, #1]
        add.w	r0, r4, r4, lsl #2
        add.w	r4, r1, r0, lsl #1
        ldrb.w	r1, [lr, r2]
        add.w	r0, r12, r12, lsl #2
        subs	r2, #1
        add.w	r12, r1, r0, lsl #1
        adds	r0, r2, #1
        add.w	r3, r3, #1
        bne	_LBB4_8
        sub.w	r0, r12, r4
        add	sp, #4
        pop	{r4, r6, r7, pc}
_Lfunc_end4:
.balign 4
