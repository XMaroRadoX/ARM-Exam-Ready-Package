.syntax unified
.cpu cortex-m3
.thumb
.text
.global extrema_indexes
extrema_indexes:
        cmp r0,#0
        beq ei_bad
        cmp r1,#0
        beq ei_bad
        cmp r2,#0
        beq ei_bad
        cmp r3,#0
        beq ei_bad
        cmp r2,r3
        beq ei_bad
        push {r4-r10,lr}
        movs r4,#0
        movs r5,#0
        movs r6,#1
        ldr r8,[r0]
        mov r9,r8
ei_loop:
        cmp r6,r1
        bhs ei_done
        ldr r7,[r0,r6,lsl #2]
        cmp r7,r8
        bge ei_max
        mov r8,r7
        mov r4,r6
ei_max:
        cmp r7,r9
        ble ei_next
        mov r9,r7
        mov r5,r6
ei_next:
        adds r6,#1
        b ei_loop
ei_done:
        str r4,[r2]
        str r5,[r3]
        movs r0,#1
        pop {r4-r10,pc}
ei_bad:
        movs r0,#0
        bx lr
.balign 4
