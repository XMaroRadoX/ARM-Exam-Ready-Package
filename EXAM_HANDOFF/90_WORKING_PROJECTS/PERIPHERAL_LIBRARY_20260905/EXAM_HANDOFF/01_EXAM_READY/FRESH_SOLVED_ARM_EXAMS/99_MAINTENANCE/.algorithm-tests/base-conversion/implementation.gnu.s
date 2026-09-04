.syntax unified
.cpu cortex-m3
.thumb
.text
.global u32_to_base
u32_to_base:
        cmp r2,#0
        beq cv_bad
        cmp r1,#2
        blo cv_bad
        cmp r1,#16
        bhi cv_bad
        push {r4-r8,lr}
        sub sp,sp,#32
        movs r4,#0
cv_digits:
        udiv r5,r0,r1
        mls r6,r5,r1,r0
        cmp r6,#10
        blo cv_decimal
        adds r6,#55
        b cv_put
cv_decimal:
        adds r6,#48
cv_put:
        strb r6,[sp,r4]
        adds r4,#1
        mov r0,r5
        cmp r0,#0
        bne cv_digits
        cmp r3,r4
        bls cv_fail
        mov r5,r4
        movs r6,#0
cv_copy:
        subs r5,#1
        ldrb r7,[sp,r5]
        strb r7,[r2,r6]
        adds r6,#1
        cmp r5,#0
        bne cv_copy
        movs r7,#0
        strb r7,[r2,r6]
        mov r0,r4
        b cv_done
cv_fail:
        movs r0,#0
cv_done:
        add sp,sp,#32
        pop {r4-r8,pc}
cv_bad:
        movs r0,#0
        bx lr
.balign 4
