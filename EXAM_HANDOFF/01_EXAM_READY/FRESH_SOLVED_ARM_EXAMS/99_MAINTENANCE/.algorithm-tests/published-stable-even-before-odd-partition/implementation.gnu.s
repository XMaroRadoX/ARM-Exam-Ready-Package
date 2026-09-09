.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_stable_even_first
array_stable_even_first:
        cmp r1,#0
        beq aep_yes
        cmp r0,#0
        beq aep_bad
        push {r4-r6,lr}
        movs r2,#1
aep_outer:
        cmp r2,r1
        bhs aep_done
        ldr r4,[r0,r2,lsl #2]
        tst r4,#1
        bne aep_next
        mov r3,r2
aep_shift:
        cmp r3,#0
        beq aep_place
        sub r5,r3,#1
        ldr r6,[r0,r5,lsl #2]
        tst r6,#1
        beq aep_place
        str r6,[r0,r3,lsl #2]
        mov r3,r5
        b aep_shift
aep_place:
        str r4,[r0,r3,lsl #2]
aep_next:
        adds r2,#1
        b aep_outer
aep_done:
        pop {r4-r6,lr}
aep_yes:
        movs r0,#1
        bx lr
aep_bad:
        movs r0,#0
        bx lr
.balign 4
