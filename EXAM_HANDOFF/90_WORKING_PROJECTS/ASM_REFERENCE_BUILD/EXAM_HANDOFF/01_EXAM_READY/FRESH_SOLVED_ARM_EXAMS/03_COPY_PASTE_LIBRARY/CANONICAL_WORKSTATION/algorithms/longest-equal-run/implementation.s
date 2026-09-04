; Longest equal-value contiguous run
; uint32_t longest_equal_run(const int32_t *a, uint32_t n)
; Return the longest contiguous run; null or empty input returns zero. Signed comparisons apply.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT longest_equal_run
longest_equal_run
        cmp r0,#0
        beq lr_bad
        cmp r1,#0
        beq lr_bad
        push {r4-r6,lr}
        ldr r2,[r0],#4
        movs r3,#1
        movs r4,#1
        subs r1,#1
lr_loop
        cmp r1,#0
        beq lr_done
        ldr r5,[r0],#4
        cmp r5,r2
        bne lr_reset
        adds r3,#1
        b lr_max
lr_reset
        movs r3,#1
lr_max
        cmp r3,r4
        bls lr_next
        mov r4,r3
lr_next
        mov r2,r5
        subs r1,#1
        b lr_loop
lr_done
        mov r0,r4
        pop {r4-r6,pc}
lr_bad
        movs r0,#0
        bx lr

        ALIGN
        END
