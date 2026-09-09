.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_trace_i32
matrix_trace_i32:
        cmp r2,#0
        beq mtr_bad
        cmp r1,#256
        bhi mtr_bad
        cmp r1,#0
        beq mtr_empty
        cmp r0,#0
        beq mtr_bad
        push {r4-r7,lr}
        movs r3,#0
        movs r4,#0
        movs r5,#0
        add r7,r1,#1
mtr_loop:
        ldr r6,[r0,r3,lsl #2]
        asr r12,r6,#31
        adds r4,r4,r6
        adc r5,r5,r12
        add r3,r3,r7
        subs r1,#1
        bne mtr_loop
        str r4,[r2]
        str r5,[r2,#4]
        movs r0,#1
        pop {r4-r7,pc}
mtr_empty:
        movs r3,#0
        str r3,[r2]
        str r3,[r2,#4]
        movs r0,#1
        bx lr
mtr_bad:
        movs r0,#0
        bx lr
.balign 4
