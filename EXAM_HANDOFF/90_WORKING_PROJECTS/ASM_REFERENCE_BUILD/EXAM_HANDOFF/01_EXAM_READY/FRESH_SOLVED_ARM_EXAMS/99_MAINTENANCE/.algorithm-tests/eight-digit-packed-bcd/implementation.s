; Eight-digit packed BCD encoding
; int packed_bcd(uint32_t value, uint32_t *out)
; Accept 0..99999999. Write eight decimal nibbles in a 32-bit result, with leading zero nibbles. Return 1, or 0 without writing on invalid input.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT packed_bcd
packed_bcd
        cmp r1,#0
        beq bd_bad
        ldr r2,=99999999
        cmp r0,r2
        bhi bd_bad
        push {r4-r6,lr}
        movs r2,#0
        movs r3,#0
        movs r4,#10
bd_loop
        udiv r5,r0,r4
        mls r6,r5,r4,r0
        lsl r6,r6,r3
        orr r2,r2,r6
        mov r0,r5
        adds r3,#4
        cmp r3,#32
        blo bd_loop
        str r2,[r1]
        movs r0,#1
        pop {r4-r6,pc}
bd_bad
        movs r0,#0
        bx lr

        ALIGN
        END
