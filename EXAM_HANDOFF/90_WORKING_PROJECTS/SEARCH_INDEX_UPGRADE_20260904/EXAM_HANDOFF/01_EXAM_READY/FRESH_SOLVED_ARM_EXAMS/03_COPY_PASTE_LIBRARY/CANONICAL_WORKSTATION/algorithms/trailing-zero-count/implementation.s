; Trailing zero count
; uint32_t trailing_zero_count(uint32_t value)
; Count zeros from the named end; zero has a count of 32.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT trailing_zero_count
trailing_zero_count
        cmp r0,#0
        beq z_all
        movs r1,#0
z_loop
        tst r0,#1
        bne z_done
        adds r1,#1
        lsrs r0,#1
        b z_loop
z_done
        mov r0,r1
        bx lr
z_all
        movs r0,#32
        bx lr

        ALIGN
        END
