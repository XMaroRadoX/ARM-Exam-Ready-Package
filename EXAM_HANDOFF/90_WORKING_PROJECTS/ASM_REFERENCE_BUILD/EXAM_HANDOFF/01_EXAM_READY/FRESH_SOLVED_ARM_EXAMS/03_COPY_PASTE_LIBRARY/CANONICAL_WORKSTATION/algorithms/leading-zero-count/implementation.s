; Leading zero count
; uint32_t leading_zero_count(uint32_t value)
; Count zeros from the named end; zero has a count of 32.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT leading_zero_count
leading_zero_count
        cmp r0,#0
        beq z_all
        movs r1,#0
z_loop
        tst r0,#0x80000000
        bne z_done
        adds r1,#1
        lsls r0,#1
        b z_loop
z_done
        mov r0,r1
        bx lr
z_all
        movs r0,#32
        bx lr

        ALIGN
        END
