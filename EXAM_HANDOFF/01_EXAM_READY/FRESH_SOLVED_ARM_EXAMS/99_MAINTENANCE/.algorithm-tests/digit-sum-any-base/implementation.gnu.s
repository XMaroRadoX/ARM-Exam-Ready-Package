.syntax unified
.cpu cortex-m3
.thumb
.text
.global digit_sum_base
digit_sum_base:
        cmp r1,#2
        blo ds_bad
        cmp r1,#36
        bhi ds_bad
        cmp r2,#0
        beq ds_bad
        push {r4,r5}
        movs r3,#0
ds_loop:
        udiv r4,r0,r1
        mls r5,r4,r1,r0
        add r3,r5
        mov r0,r4
        cmp r0,#0
        bne ds_loop
        str r3,[r2]
        pop {r4,r5}
        movs r0,#1
        bx lr
ds_bad:
        movs r0,#0
        bx lr
.balign 4
