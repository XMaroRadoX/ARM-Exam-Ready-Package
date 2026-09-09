; Produce adjacent differences
; int array_adjacent_differences(const int32_t *values, uint32_t count,
;                                int64_t *output, uint32_t capacity)
; Write values[i+1]-values[i] as signed 64-bit results. Output length is count-1 for nonempty input and zero for empty input. Validate all inputs before writing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_adjacent_differences
array_adjacent_differences
        ; R0=values, R1=count, R2=output, R3=capacity.
        cmp r1,#0
        beq aad_yes
        cmp r0,#0
        beq aad_bad
        subs r1,#1
        cmp r3,r1
        blo aad_bad
        cmp r1,#0
        beq aad_yes
        cmp r2,#0
        beq aad_bad
        push {r4-r7,lr}
        ldr r4,[r0],#4
aad_loop
        ldr r5,[r0],#4
        mov r7,r5
        asr r6,r5,#31
        subs r5,r5,r4
        sbc r6,r6,r4,asr #31
        str r5,[r2],#4
        str r6,[r2],#4
        mov r4,r7
        subs r1,#1
        bne aad_loop
        pop {r4-r7,lr}
aad_yes
        movs r0,#1
        bx lr
aad_bad
        movs r0,#0
        bx lr

        ALIGN
        END
