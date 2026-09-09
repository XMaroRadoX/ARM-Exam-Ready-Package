.syntax unified
.cpu cortex-m3
.thumb
.text
.global checked_array_product
checked_array_product:
        cmp r2,#0
        beq cap_bad
        cmp r1,#0
        beq cap_empty
        cmp r0,#0
        beq cap_bad
        push {r4-r7,lr}
        movs r3,#1
cap_loop:
        ldr r4,[r0],#4
        smull r5,r6,r3,r4
        asr r7,r5,#31
        cmp r6,r7
        bne cap_fail
        mov r3,r5
        subs r1,#1
        bne cap_loop
        str r3,[r2]
        movs r0,#1
        pop {r4-r7,pc}
cap_fail:
        movs r0,#0
        pop {r4-r7,pc}
cap_empty:
        movs r3,#1
        str r3,[r2]
        movs r0,#1
        bx lr
cap_bad:
        movs r0,#0
        bx lr
.balign 4
