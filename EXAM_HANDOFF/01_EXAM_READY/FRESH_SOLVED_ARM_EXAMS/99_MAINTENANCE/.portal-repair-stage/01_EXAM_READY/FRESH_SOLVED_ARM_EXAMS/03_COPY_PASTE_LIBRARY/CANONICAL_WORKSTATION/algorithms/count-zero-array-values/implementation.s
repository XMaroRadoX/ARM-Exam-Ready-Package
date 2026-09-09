; Count zero array values
; uint32_t count_array_zero(const int32_t *values, uint32_t count)
; Count matching signed words. A null pointer returns zero; the routine never writes memory.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT count_array_zero
count_array_zero
        ; R0=values, R1=count. R4 is the count.
        cmp r0,#0
        beq ack_zero
        push {r4,lr}
        movs r4,#0
ack_loop
        cmp r1,#0
        beq ack_done
        ldr r3,[r0],#4
        cmp r3,#0
        bne ack_next
        adds r4,#1
ack_next
        subs r1,#1
        b ack_loop
ack_done
        mov r0,r4
        pop {r4,pc}
ack_zero
        movs r0,#0
        bx lr

        ALIGN
        END
