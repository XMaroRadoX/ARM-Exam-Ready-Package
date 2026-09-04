.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_in_place_array_reversal
.balign 4
algorithm_in_place_array_reversal:
        cmp	r0, #0
        it	ne
        lsrsne.w	r2, r1, #1
        beq	_LBB0_3
        subs	r0, #4
        add.w	r1, r0, r1, lsl #2
.balign 4
_LBB0_2:
        ldr	r12, [r0, #4]!
        ldr	r3, [r1]
        subs	r2, #1
        str	r3, [r0]
        str	r12, [r1], #-4
        bne	_LBB0_2
_LBB0_3:
        bx	lr
_Lfunc_end0:
.balign 4
