; First strict interior peak
; int32_t first_peak(const int32_t *a, uint32_t n)
; Return the first interior index i with a[i]>a[i-1] and a[i]>a[i+1], or -1. Require n<=INT32_MAX; endpoints are not peaks.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT first_peak
first_peak
        cmp r0,#0
        beq pk_bad
        cmp r1,#3
        blo pk_bad
        cmp r1,#0
        bmi pk_bad
        push {r4-r6,lr}
        movs r2,#1
        subs r1,#1
pk_loop
        cmp r2,r1
        bhs pk_fail
        sub r3,r2,#1
        ldr r4,[r0,r3,lsl #2]
        ldr r5,[r0,r2,lsl #2]
        cmp r5,r4
        ble pk_next
        add r3,r2,#1
        ldr r6,[r0,r3,lsl #2]
        cmp r5,r6
        ble pk_next
        mov r0,r2
        pop {r4-r6,pc}
pk_next
        adds r2,#1
        b pk_loop
pk_fail
        pop {r4-r6,lr}
pk_bad
        mvn r0,#0
        bx lr

        ALIGN
        END
