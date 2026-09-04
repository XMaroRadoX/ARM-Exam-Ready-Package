.syntax unified
.cpu cortex-m3
.thumb
.text
.global format_i32
format_i32:
        cmp r1,#0
        beq fm_bad
        push {r4-r8,lr}
        sub sp,sp,#16
        movs r4,#0
        cmp r0,#0
        bge fm_start
        movs r4,#1
        rsb r0,r0,#0
fm_start:
        movs r5,#0
        movs r6,#10
fm_digits:
        udiv r7,r0,r6
        mls r8,r7,r6,r0
        adds r8,#48
        strb r8,[sp,r5]
        adds r5,#1
        mov r0,r7
        cmp r0,#0
        bne fm_digits
        add r7,r5,r4
        cmp r2,r7
        bls fm_fail
        movs r3,#0
        cmp r4,#0
        beq fm_copy
        movs r0,#45
        strb r0,[r1],#1
        movs r3,#1
fm_copy:
        subs r5,#1
        ldrb r0,[sp,r5]
        strb r0,[r1],#1
        adds r3,#1
        cmp r5,#0
        bne fm_copy
        movs r0,#0
        strb r0,[r1]
        mov r0,r3
        b fm_done
fm_fail:
        movs r0,#0
fm_done:
        add sp,sp,#16
        pop {r4-r8,pc}
fm_bad:
        movs r0,#0
        bx lr
.balign 4
