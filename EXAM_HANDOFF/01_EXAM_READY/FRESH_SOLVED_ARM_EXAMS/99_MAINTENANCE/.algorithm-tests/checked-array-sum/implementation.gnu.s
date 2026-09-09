.syntax unified
.cpu cortex-m3
.thumb
.text
.global checked_array_sum
checked_array_sum:
        cmp r2,#0
        beq cas_bad
        cmp r1,#0
        bmi cas_bad
        cmp r1,#0
        beq cas_empty
        cmp r0,#0
        beq cas_bad
        push {r4-r7,lr}
        movs r3,#0
        movs r4,#0
cas_loop:
        ldr r5,[r0],#4
        asr r6,r5,#31
        adds r3,r3,r5
        adc r4,r4,r6
        subs r1,#1
        bne cas_loop
        str r3,[r2]
        str r4,[r2,#4]
        movs r0,#1
        pop {r4-r7,pc}
cas_empty:
        movs r3,#0
        str r3,[r2]
        str r3,[r2,#4]
        movs r0,#1
        bx lr
cas_bad:
        movs r0,#0
        bx lr
.balign 4
