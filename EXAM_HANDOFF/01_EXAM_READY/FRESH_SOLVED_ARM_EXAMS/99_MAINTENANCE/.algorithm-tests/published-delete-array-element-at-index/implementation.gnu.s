.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_delete_at
array_delete_at:
        cmp r0,#0
        beq adel_bad
        cmp r1,#0
        beq adel_bad
        cmp r3,#0
        beq adel_bad
        ldr r12,[r1]
        cmp r2,r12
        bhs adel_bad
        push {r4-r6,lr}
        ldr r4,[r0,r2,lsl #2]
        mov r5,r2
adel_shift:
        add r6,r5,#1
        cmp r6,r12
        bhs adel_done
        ldr r2,[r0,r6,lsl #2]
        str r2,[r0,r5,lsl #2]
        mov r5,r6
        b adel_shift
adel_done:
        subs r12,#1
        str r12,[r1]
        str r4,[r3]
        movs r0,#1
        pop {r4-r6,pc}
adel_bad:
        movs r0,#0
        bx lr
.balign 4
