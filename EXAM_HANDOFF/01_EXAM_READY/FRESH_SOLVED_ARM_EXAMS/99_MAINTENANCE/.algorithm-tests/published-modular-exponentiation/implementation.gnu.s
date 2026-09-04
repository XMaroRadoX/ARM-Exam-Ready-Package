.syntax unified
.cpu cortex-m3
.thumb
.text
.global modular_power
modular_power:
        cmp r3,#0
        beq mp_bad
        cmp r2,#0
        beq mp_bad
        push {r4-r6,lr}
        ldr r4,=65535
        cmp r2,r4
        bhi mp_fail
        udiv r4,r0,r2
        mls r0,r4,r2,r0
        movs r4,#1
        udiv r5,r4,r2
        mls r4,r5,r2,r4
mp_loop:
        cmp r1,#0
        beq mp_done
        tst r1,#1
        beq mp_square
        mul r4,r0,r4
        udiv r5,r4,r2
        mls r4,r5,r2,r4
mp_square:
        lsrs r1,#1
        mul r0,r0,r0
        udiv r5,r0,r2
        mls r0,r5,r2,r0
        b mp_loop
mp_done:
        str r4,[r3]
        movs r0,#1
        pop {r4-r6,pc}
mp_fail:
        pop {r4-r6,lr}
mp_bad:
        movs r0,#0
        bx lr
.balign 4
