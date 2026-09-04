.syntax unified
.cpu cortex-m3
.thumb
.text
.global reverse_decimal
reverse_decimal:
        cmp r1,#0
        beq rd_bad
        push {r4-r6,lr}
        movs r2,#0
        movs r3,#10
rd_loop:
        udiv r4,r0,r3
        mls r5,r4,r3,r0
        umull r0,r6,r2,r3
        adds r2,r0,r5
        bcs rd_fail
        cmp r6,#0
        bne rd_fail
        mov r0,r4
        cmp r0,#0
        bne rd_loop
        str r2,[r1]
        movs r0,#1
        pop {r4-r6,pc}
rd_fail:
        pop {r4-r6,lr}
rd_bad:
        movs r0,#0
        bx lr
.balign 4
