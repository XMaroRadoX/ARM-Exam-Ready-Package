; Count above a signed threshold
; uint32_t count_above(const int32_t *a, uint32_t n, int32_t threshold)
; Count elements strictly greater than threshold. Empty input or a null input pointer returns zero.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT count_above
count_above
        movs r3,#0
        cmp r0,#0
        beq ca_done
        push {r4,r5}
ca_loop
        cmp r1,#0
        beq ca_pop
        ldr r4,[r0],#4
        cmp r4,r2
        ble ca_next
        adds r3,#1
ca_next
        subs r1,#1
        b ca_loop
ca_pop
        pop {r4,r5}
ca_done
        mov r0,r3
        bx lr

        ALIGN
        END
