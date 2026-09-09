.syntax unified
.cpu cortex-m3
.thumb
.text
.global decimal_digit_frequency_i32
decimal_digit_frequency_i32:
        cmp r1,#0
        beq ddf_bad
        push {r4,lr}
        movs r2,#0
        movs r3,#0
ddf_clear:
        str r3,[r1,r2,lsl #2]
        adds r2,#1
        cmp r2,#10
        blo ddf_clear
        mov r2,r0
        cmp r0,#0
        bge ddf_ready
        rsb r2,r0,#0
ddf_ready:
        cmp r2,#0
        bne ddf_loop
        movs r3,#1
        str r3,[r1]
        b ddf_done
ddf_loop:
        movs r4,#10
        udiv r3,r2,r4
        mls r12,r3,r4,r2
        ldr r0,[r1,r12,lsl #2]
        adds r0,#1
        str r0,[r1,r12,lsl #2]
        mov r2,r3
        cmp r2,#0
        bne ddf_loop
ddf_done:
        movs r0,#1
        pop {r4,pc}
ddf_bad:
        movs r0,#0
        bx lr
.balign 4
