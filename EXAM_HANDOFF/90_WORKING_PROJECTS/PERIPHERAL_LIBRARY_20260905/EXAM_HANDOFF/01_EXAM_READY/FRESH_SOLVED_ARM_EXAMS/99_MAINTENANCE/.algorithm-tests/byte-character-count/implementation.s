; Character count in a byte span
; uint32_t byte_count(const uint8_t *text, uint32_t length, uint8_t key)
; Count every occurrence, including zero bytes, within the explicit span. Null input returns zero.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT byte_count
byte_count
        movs r3,#0
        cmp r0,#0
        beq cc_done
        push {r4,r5}
        uxtb r2,r2
cc_loop
        cmp r1,#0
        beq cc_pop
        ldrb r4,[r0],#1
        cmp r4,r2
        bne cc_next
        adds r3,#1
cc_next
        subs r1,#1
        b cc_loop
cc_pop
        pop {r4,r5}
cc_done
        mov r0,r3
        bx lr

        ALIGN
        END
