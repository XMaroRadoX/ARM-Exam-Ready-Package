; Shift an array left with a fill value
; int array_shift_left(int32_t *values, uint32_t count, uint32_t amount, int32_t fill_value)
; Shift by amount positions and fill vacated positions. An amount at least count fills the array. Empty input succeeds; null nonempty input fails.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_shift_left
array_shift_left
        ; R0=values, R1=count, R2=amount, R3=fill_value.
        cmp r1,#0
        beq ash_yes
        cmp r0,#0
        beq ash_bad
        cmp r2,r1
        bls ash_amount_ok
        mov r2,r1
ash_amount_ok
        push {r4,r5}
        sub r4,r1,r2
        movs r5,#0
ash_copy
        cmp r5,r4
        bhs ash_fill
        add r12,r5,r2
        ldr r12,[r0,r12,lsl #2]
        str r12,[r0,r5,lsl #2]
        adds r5,#1
        b ash_copy
ash_fill
        cmp r5,r1
        bhs ash_done
        str r3,[r0,r5,lsl #2]
        adds r5,#1
        b ash_fill
ash_done
        pop {r4,r5}
        b ash_yes
ash_yes
        movs r0,#1
        bx lr
ash_bad
        movs r0,#0
        bx lr

        ALIGN
        END
