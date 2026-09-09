; Second largest distinct value
; int second_largest(const int32_t *a, uint32_t n, int32_t *out)
; Return 1 and store the second distinct extremum. Return 0 without writing for null storage, empty input, or fewer than two distinct values.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT second_largest
second_largest
        cmp r0,#0
        beq sx_bad
        cmp r2,#0
        beq sx_bad
        cmp r1,#0
        beq sx_bad
        push {r4-r8,lr}
        ldr r4,[r0]
        movs r5,#0
        movs r6,#0
        movs r3,#1
sx_loop
        cmp r3,r1
        bhs sx_done
        ldr r7,[r0,r3,lsl #2]
        cmp r7,r4
        bgt sx_best
        beq sx_next
        cmp r6,#0
        beq sx_second
        cmp r7,r5
        ble sx_next
sx_second
        mov r5,r7
        movs r6,#1
        b sx_next
sx_best
        mov r5,r4
        mov r4,r7
        movs r6,#1
sx_next
        adds r3,#1
        b sx_loop
sx_done
        cmp r6,#0
        beq sx_no
        str r5,[r2]
sx_no
        mov r0,r6
        pop {r4-r8,pc}
sx_bad
        movs r0,#0
        bx lr

        ALIGN
        END
