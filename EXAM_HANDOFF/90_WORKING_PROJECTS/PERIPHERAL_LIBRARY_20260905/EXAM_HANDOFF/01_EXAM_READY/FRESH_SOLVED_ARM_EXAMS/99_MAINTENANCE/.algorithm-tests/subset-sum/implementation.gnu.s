.syntax unified
.cpu cortex-m3
.thumb
.text
.global subset_sum
subset_sum:
        cmp r0,#0
        beq su_bad
        cmp r3,#0
        beq su_bad
        cmn r2,#1
        beq su_bad
        push {r4-r8,lr}
        movs r4,#0
        movs r5,#0
su_init:
        strb r5,[r3,r4]
        cmp r4,r2
        beq su_start
        adds r4,#1
        b su_init
su_start:
        movs r5,#1
        strb r5,[r3]
        movs r4,#0
su_outer:
        cmp r4,r1
        bhs su_done
        ldrh r5,[r0,r4,lsl #1]
        cmp r5,#0
        beq su_next
        add r6,r2,#1
su_inner:
        cmp r6,r5
        bls su_next
        subs r6,#1
        sub r7,r6,r5
        ldrb r8,[r3,r7]
        cmp r8,#0
        beq su_inner
        movs r8,#1
        strb r8,[r3,r6]
        b su_inner
su_next:
        adds r4,#1
        b su_outer
su_done:
        ldrb r0,[r3,r2]
        pop {r4-r8,pc}
su_bad:
        movs r0,#0
        bx lr
.balign 4
