.syntax unified
.cpu cortex-m3
.thumb
.text
.global fibonacci_array
fibonacci_array:
        cmp r1,#48
        bhi seq_bad
        cmp r1,r2
        bhi seq_bad
        cmp r1,#0
        beq seq_ok
        cmp r0,#0
        beq seq_bad
        push {r4,r5}
        movs r2,#0
seq_loop:
        cmp r2,#2
        bhs seq_sum
        mov r3,r2
        b seq_write
seq_sum:
        sub r3,r2,#1
        ldr r4,[r0,r3,lsl #2]
        subs r3,#1
        ldr r5,[r0,r3,lsl #2]
        add r3,r4,r5
seq_write:
        str r3,[r0,r2,lsl #2]
        adds r2,#1
        cmp r2,r1
        blo seq_loop
        pop {r4,r5}
seq_ok:
        movs r0,#1
        bx lr
seq_bad:
        movs r0,#0
        bx lr
.balign 4
