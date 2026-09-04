; Stable threshold filtering
; uint32_t threshold_filter(const int32_t *a, uint32_t n, int32_t threshold, int32_t *out, uint32_t capacity)
; Copy values strictly greater than threshold in input order. Output capacity must be at least n; exact in-place filtering is allowed, other overlap is not. Return count or UINT32_MAX on invalid input before writing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT threshold_filter
threshold_filter
        ldr r12,[sp]
        cmp r12,r1
        blo tf_bad
        cmp r1,#0
        beq tf_zero
        cmp r0,#0
        beq tf_bad
        cmp r3,#0
        beq tf_bad
        push {r4-r6,lr}
        movs r4,#0
tf_loop
        cmp r1,#0
        beq tf_done
        ldr r5,[r0],#4
        cmp r5,r2
        ble tf_next
        str r5,[r3,r4,lsl #2]
        adds r4,#1
tf_next
        subs r1,#1
        b tf_loop
tf_done
        mov r0,r4
        pop {r4-r6,pc}
tf_zero
        movs r0,#0
        bx lr
tf_bad
        mvn r0,#0
        bx lr

        ALIGN
        END
