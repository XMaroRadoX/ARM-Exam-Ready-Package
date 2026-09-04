; Matching Cortex-M3 Thumb implementation generated from reference.c.
; Verification status: COMPILE_ONLY until executed in a simulator/board.
                AREA    |.text.patterns|, CODE, READONLY
                PRESERVE8
                THUMB

                EXPORT  pat_alg_bitfield_001
                EXPORT  pat_alg_bitfield_001_extract
                EXPORT  pat_alg_bitfield_001_pack_u16

                ALIGN   2
pat_alg_bitfield_001
; %bb.0:
	cmp	r2, #31
	bhi	LBB0_4
; %bb.1:
	cbz	r3, LBB0_4
; %bb.2:
	rsb.w	r12, r2, #32
	cmp	r12, r3
	it	lo
	bxlo	lr
LBB0_3
	mov.w	r12, #-1
	lsl.w	r12, r12, r3
	mvn.w	r12, r12
	cmp	r3, #31
	it	hi
	movhi.w	r12, #-1
	lsl.w	r3, r12, r2
	and.w	r1, r1, r12
	bics	r0, r3
	lsls	r1, r2
	orrs	r0, r1
LBB0_4
	bx	lr
Lfunc_end0
                                        ; -- End function
                ALIGN   2
pat_alg_bitfield_001_extract
; %bb.0:
	mov	r12, r0
	cmp	r1, #31
	mov.w	r0, #0
	bhi	LBB1_4
; %bb.1:
	cbz	r2, LBB1_4
; %bb.2:
	rsb.w	r3, r1, #32
	cmp	r3, r2
	it	lo
	bxlo	lr
LBB1_3
	lsr.w	r0, r12, r1
	mov.w	r1, #-1
	lsls	r1, r2
	cmp	r2, #31
	it	ls
	bicls	r0, r1
LBB1_4
	bx	lr
Lfunc_end1
                                        ; -- End function
                ALIGN   2
pat_alg_bitfield_001_pack_u16
; %bb.0:
	orr.w	r0, r1, r0, lsl #16
	bx	lr
Lfunc_end2
                                        ; -- End function

                END
