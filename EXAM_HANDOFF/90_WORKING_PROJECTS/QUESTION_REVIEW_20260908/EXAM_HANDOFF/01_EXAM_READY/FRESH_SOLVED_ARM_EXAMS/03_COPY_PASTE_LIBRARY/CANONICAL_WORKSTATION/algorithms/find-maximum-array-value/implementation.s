; Find the maximum array value
; int array_maximum(const int32_t *values, uint32_t count, int32_t *value_out)
; Return the maximum signed value. Empty input or a null required pointer returns 0 without writing. Equal values keep the first candidate.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_maximum
array_maximum
        ; R0=values, R1=count, R2=value_out, R3=current best.
        cmp r0,#0
        beq axe_bad
        cmp r2,#0
        beq axe_bad
        cmp r1,#0
        beq axe_bad
        push {r4,lr}
        ldr r3,[r0],#4
        subs r1,#1
axe_loop
        cmp r1,#0
        beq axe_done
        ldr r4,[r0],#4
        cmp r4,r3
        ble axe_next
        mov r3,r4
axe_next
        subs r1,#1
        b axe_loop
axe_done
        str r3,[r2]
        movs r0,#1
        pop {r4,pc}
axe_bad
        movs r0,#0
        bx lr

        ALIGN
        END
