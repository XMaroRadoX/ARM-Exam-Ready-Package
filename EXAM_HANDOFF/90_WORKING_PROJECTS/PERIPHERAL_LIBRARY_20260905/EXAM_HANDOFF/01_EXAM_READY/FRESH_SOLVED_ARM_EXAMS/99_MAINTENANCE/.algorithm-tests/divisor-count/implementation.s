; Number of positive divisors
; uint32_t divisor_count(uint32_t n)
; Count positive divisors; divisor_count(0)=0.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT divisor_count
divisor_count
        push {r4,r5}
        movs r1,#1
        movs r2,#0
        cmp r0,#0
        beq dc_done
dc_loop
        udiv r3,r0,r1
        cmp r1,r3
        bhi dc_done
        mls r4,r3,r1,r0
        cmp r4,#0
        bne dc_next
        adds r2,#1
        cmp r1,r3
        beq dc_next
        adds r2,#1
dc_next
        adds r1,#1
        b dc_loop
dc_done
        mov r0,r2
        pop {r4,r5}
        bx lr

        ALIGN
        END
