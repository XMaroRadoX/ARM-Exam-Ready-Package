.syntax unified
.cpu cortex-m3
.thumb
.text
.global parse_u32
parse_u32:
        cmp r0,#0
        beq pa_bad
        cmp r1,#0
        beq pa_bad
        cmp r2,#0
        beq pa_bad
        push {r4-r8,lr}
        movs r3,#0
        movs r6,#10
pa_loop:
        ldrb r4,[r0],#1
        subs r4,#48
        cmp r4,#9
        bhi pa_fail
        umull r5,r8,r3,r6
        cmp r8,#0
        bne pa_fail
        adds r3,r5,r4
        bcs pa_fail
        subs r1,#1
        bne pa_loop
        str r3,[r2]
        movs r0,#1
        pop {r4-r8,pc}
pa_fail:
        movs r0,#0
        pop {r4-r8,pc}
pa_bad:
        movs r0,#0
        bx lr
.balign 4
