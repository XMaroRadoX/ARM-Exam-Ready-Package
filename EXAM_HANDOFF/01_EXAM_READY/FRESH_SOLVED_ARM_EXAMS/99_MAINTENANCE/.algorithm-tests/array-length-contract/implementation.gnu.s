.syntax unified
.cpu cortex-m3
.thumb
.text
.global bounded_word_length
bounded_word_length:
        cmp r0,#0
        beq al_bad
        cmp r3,#0
        beq al_bad
        push {r4,lr}
        movs r4,#0
al_loop:
        cmp r4,r1
        bhs al_missing
        ldr r12,[r0,r4,lsl #2]
        cmp r12,r2
        beq al_found
        adds r4,#1
        b al_loop
al_found:
        str r4,[r3]
        movs r0,#1
        pop {r4,pc}
al_missing:
        movs r0,#0
        pop {r4,pc}
al_bad:
        movs r0,#0
        bx lr
.balign 4
