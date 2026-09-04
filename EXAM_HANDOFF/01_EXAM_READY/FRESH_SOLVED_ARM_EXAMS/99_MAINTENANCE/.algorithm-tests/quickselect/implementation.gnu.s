.syntax unified
.cpu cortex-m3
.thumb
.text
.global quickselect
quickselect:
        cmp r0,#0
        beq qs_bad
        cmp r3,#0
        beq qs_bad
        cmp r2,r1
        bhs qs_bad
        push {r4-r10,lr}
        movs r4,#0
        sub r5,r1,#1
qs_outer:
        mov r6,r4
        mov r7,r4
        ldr r8,[r0,r5,lsl #2]
qs_scan:
        cmp r6,r5
        bhs qs_pivot
        ldr r9,[r0,r6,lsl #2]
        cmp r9,r8
        bge qs_next
        ldr r10,[r0,r7,lsl #2]
        str r10,[r0,r6,lsl #2]
        str r9,[r0,r7,lsl #2]
        adds r7,#1
qs_next:
        adds r6,#1
        b qs_scan
qs_pivot:
        ldr r9,[r0,r7,lsl #2]
        str r9,[r0,r5,lsl #2]
        str r8,[r0,r7,lsl #2]
        cmp r7,r2
        beq qs_found
        bhi qs_left
        add r4,r7,#1
        b qs_outer
qs_left:
        sub r5,r7,#1
        b qs_outer
qs_found:
        str r8,[r3]
        movs r0,#1
        pop {r4-r10,pc}
qs_bad:
        movs r0,#0
        bx lr
.balign 4
