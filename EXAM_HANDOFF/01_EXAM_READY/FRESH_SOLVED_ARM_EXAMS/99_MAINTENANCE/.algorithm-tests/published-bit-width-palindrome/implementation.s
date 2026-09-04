; Palindrome within a bit width
; int bit_palindrome(uint32_t value, uint32_t width)
; Compare the low width bits for width=0..32. Ignore higher bits. Width zero is a palindrome; width>32 returns 0.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT bit_palindrome
bit_palindrome
        cmp r1,#32
        bhi bp_bad
        push {r4,r5}
        mov r4,r0
        movs r2,#0
        movs r3,#0
bp_loop
        cmp r1,#0
        beq bp_check
        lsrs r0,#1
        adc r2,r2,r2
        lsls r3,#1
        adds r3,#1
        subs r1,#1
        b bp_loop
bp_check
        and r4,r4,r3
        movs r0,#0
        cmp r4,r2
        bne bp_done
        movs r0,#1
bp_done
        pop {r4,r5}
        bx lr
bp_bad
        movs r0,#0
        bx lr

        ALIGN
        END
