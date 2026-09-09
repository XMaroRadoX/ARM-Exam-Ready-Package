.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_total_sum_i32
matrix_total_sum_i32:
        cmp r3,#0
        beq mts_bad
        cmp r1,#256
        bhi mts_bad
        cmp r2,#256
        bhi mts_bad
        mul r1,r1,r2
        cmp r1,#0
        beq mts_empty
        cmp r0,#0
        beq mts_bad
        push {r4-r7,lr}
        movs r4,#0
        movs r5,#0
mts_loop:
        ldr r6,[r0],#4
        asr r7,r6,#31
        adds r4,r4,r6
        adc r5,r5,r7
        subs r1,#1
        bne mts_loop
        str r4,[r3]
        str r5,[r3,#4]
        movs r0,#1
        pop {r4-r7,pc}
mts_empty:
        movs r1,#0
        str r1,[r3]
        str r1,[r3,#4]
        movs r0,#1
        bx lr
mts_bad:
        movs r0,#0
        bx lr
.balign 4
