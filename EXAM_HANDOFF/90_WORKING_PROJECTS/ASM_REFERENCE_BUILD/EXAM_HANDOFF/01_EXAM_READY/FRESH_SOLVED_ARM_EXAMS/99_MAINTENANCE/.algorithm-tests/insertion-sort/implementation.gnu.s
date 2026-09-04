.syntax unified
.cpu cortex-m3
.thumb
.text
.global insertion_sort
insertion_sort:
        cmp r0,#0
        beq ins_done
        push {r4-r8,lr}
        movs r4,#1
ins_outer:
        cmp r4,r1
        bhs ins_pop
        ldr r5,[r0,r4,lsl #2]
        mov r6,r4
ins_inner:
        cmp r6,#0
        beq ins_store
        sub r7,r6,#1
        ldr r8,[r0,r7,lsl #2]
        cmp r8,r5
        ble ins_store
        str r8,[r0,r6,lsl #2]
        subs r6,#1
        b ins_inner
ins_store:
        str r5,[r0,r6,lsl #2]
        adds r4,#1
        b ins_outer
ins_pop:
        pop {r4-r8,lr}
ins_done:
        bx lr
.balign 4
