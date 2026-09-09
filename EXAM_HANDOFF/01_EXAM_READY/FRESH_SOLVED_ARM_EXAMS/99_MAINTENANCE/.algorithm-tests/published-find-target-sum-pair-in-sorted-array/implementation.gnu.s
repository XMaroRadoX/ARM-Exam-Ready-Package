.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_pair_sum_sorted
array_pair_sum_sorted:
        ldr r12,[sp]
        cmp r0,#0
        beq aps_bad
        cmp r3,#0
        beq aps_bad
        cmp r12,#0
        beq aps_bad
        cmp r3,r12
        beq aps_bad
        cmp r1,#2
        blo aps_bad
        push {r4-r10,lr}
        mov r4,r12
        movs r5,#0
        sub r6,r1,#1
aps_loop:
        cmp r5,r6
        bhs aps_fail
        ldr r7,[r0,r5,lsl #2]
        ldr r8,[r0,r6,lsl #2]
        asr r9,r7,#31
        asr r10,r8,#31
        adds r7,r7,r8
        adc r9,r9,r10
        asr r8,r2,#31
        cmp r9,r8
        blt aps_less
        bgt aps_more
        cmp r7,r2
        beq aps_found
        blo aps_less
aps_more:
        subs r6,#1
        b aps_loop
aps_less:
        adds r5,#1
        b aps_loop
aps_found:
        str r5,[r3]
        str r6,[r4]
        movs r0,#1
        pop {r4-r10,pc}
aps_fail:
        movs r0,#0
        pop {r4-r10,pc}
aps_bad:
        movs r0,#0
        bx lr
.balign 4
