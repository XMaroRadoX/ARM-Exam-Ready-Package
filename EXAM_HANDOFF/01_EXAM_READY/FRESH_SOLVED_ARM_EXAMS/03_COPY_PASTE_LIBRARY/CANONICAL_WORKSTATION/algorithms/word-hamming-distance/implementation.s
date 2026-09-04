; Word Hamming distance
; uint32_t word_hamming(uint32_t a, uint32_t b)
; Count differing positions in two 32-bit words; result 0..32.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT word_hamming
word_hamming
        eor r0,r0,r1
        movs r1,#0
wh_loop
        cmp r0,#0
        beq wh_done
        sub r2,r0,#1
        and r0,r0,r2
        adds r1,#1
        b wh_loop
wh_done
        mov r0,r1
        bx lr

        ALIGN
        END
