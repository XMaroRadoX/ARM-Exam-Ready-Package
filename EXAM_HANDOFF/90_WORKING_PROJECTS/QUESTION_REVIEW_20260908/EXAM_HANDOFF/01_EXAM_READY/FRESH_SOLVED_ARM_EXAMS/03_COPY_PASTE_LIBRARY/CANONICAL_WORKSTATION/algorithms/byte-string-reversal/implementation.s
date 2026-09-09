; In-place byte-string reversal
; int bytes_reverse(uint8_t *text, uint32_t length)
; Reverse exactly length bytes in place; do not include a terminator unless deliberately part of the span. Return 1, or 0 for null with nonzero length.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT bytes_reverse
bytes_reverse
        cmp r1,#0
        beq sr_yes
        cmp r0,#0
        beq sr_no
        push {r4,r5}
        movs r2,#0
        subs r1,#1
sr_loop
        cmp r2,r1
        bhs sr_done
        ldrb r3,[r0,r2]
        ldrb r4,[r0,r1]
        strb r4,[r0,r2]
        strb r3,[r0,r1]
        adds r2,#1
        subs r1,#1
        b sr_loop
sr_done
        pop {r4,r5}
sr_yes
        movs r0,#1
        bx lr
sr_no
        movs r0,#0
        bx lr

        ALIGN
        END
