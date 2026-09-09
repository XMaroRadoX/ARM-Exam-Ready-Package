; Matching Cortex-M3 Thumb implementation generated from reference.c.
; Verification status: COMPILE_ONLY until executed in a simulator/board.
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  pat_alg_checksum_crc_001
                EXPORT  pat_alg_checksum_crc_001_crc32_table

                ALIGN   2
pat_alg_checksum_crc_001
; %bb.0:
	mov	r2, r0
	cmp	r0, #0
	mov.w	r0, #0
	it	ne
	cmpne	r1, #0
	bne	LBB0_2
; %bb.1:
	bx	lr
LBB0_2
	subs	r2, #1
	movs	r3, #0
                ALIGN   2
LBB0_3                                ; =>This Inner Loop Header: Depth=1
	ldrb	r12, [r2, #1]!
	subs	r1, #1
	eor.w	r3, r3, r12
	add	r0, r12
	bne	LBB0_3
; %bb.4:
	uxth	r0, r0
	orr.w	r0, r0, r3, lsl #16
	bx	lr
Lfunc_end0
                                        ; -- End function
                ALIGN   2
pat_alg_checksum_crc_001_crc32_table
; %bb.0:
	cmp	r2, #0
	itt	eq
	moveq	r0, #0
	bxeq	lr
LBB1_1
	mov	r3, r0
	cmp	r0, #0
	mov.w	r0, #0
	it	ne
	cmpne	r1, #0
	bne	LBB1_3
; %bb.2:
	bx	lr
LBB1_3
	sub.w	r12, r3, #1
	mov.w	r0, #-1
                ALIGN   2
LBB1_4                                ; =>This Inner Loop Header: Depth=1
	ldrb	r3, [r12, #1]!
	subs	r1, #1
	eor.w	r3, r3, r0
	uxtb	r3, r3
	ldr.w	r3, [r2, r3, lsl #2]
	eor.w	r0, r3, r0, lsr #8
	bne	LBB1_4
; %bb.5:
	mvns	r0, r0
	bx	lr
Lfunc_end1
                                        ; -- End function

                END
