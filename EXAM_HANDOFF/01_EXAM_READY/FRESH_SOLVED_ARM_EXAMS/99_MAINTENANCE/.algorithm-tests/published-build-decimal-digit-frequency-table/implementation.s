; Build a decimal digit-frequency table
; int decimal_digit_frequency_i32(int32_t value, uint32_t counts[10])
; Clear and fill ten counters for the magnitude digits of value. Zero contributes one zero digit. The unsigned-magnitude conversion handles INT32_MIN. A null table fails.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT decimal_digit_frequency_i32
decimal_digit_frequency_i32
        ; R0=value,R1=counts. R2=magnitude,R3=quotient,R12=digit.
        cmp r1,#0
        beq ddf_bad
        push {r4,lr}
        movs r2,#0
        movs r3,#0
ddf_clear
        str r3,[r1,r2,lsl #2]
        adds r2,#1
        cmp r2,#10
        blo ddf_clear
        mov r2,r0
        cmp r0,#0
        bge ddf_ready
        rsb r2,r0,#0
ddf_ready
        cmp r2,#0
        bne ddf_loop
        movs r3,#1
        str r3,[r1]
        b ddf_done
ddf_loop
        movs r4,#10
        udiv r3,r2,r4
        mls r12,r3,r4,r2
        ldr r0,[r1,r12,lsl #2]
        adds r0,#1
        str r0,[r1,r12,lsl #2]
        mov r2,r3
        cmp r2,#0
        bne ddf_loop
ddf_done
        movs r0,#1
        pop {r4,pc}
ddf_bad
        movs r0,#0
        bx lr

        ALIGN
        END
