; Longest consecutive-one bit run
; uint32_t longest_one_run(uint32_t value)
; Return longest adjacent set-bit run within 32 bits.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT longest_one_run
longest_one_run
        movs r1,#0
        movs r2,#0
        movs r3,#32
lo_loop
        tst r0,#1
        beq lo_zero
        adds r1,#1
        cmp r1,r2
        bls lo_next
        mov r2,r1
        b lo_next
lo_zero
        movs r1,#0
lo_next
        lsrs r0,#1
        subs r3,#1
        bne lo_loop
        mov r0,r2
        bx lr

        ALIGN
        END
