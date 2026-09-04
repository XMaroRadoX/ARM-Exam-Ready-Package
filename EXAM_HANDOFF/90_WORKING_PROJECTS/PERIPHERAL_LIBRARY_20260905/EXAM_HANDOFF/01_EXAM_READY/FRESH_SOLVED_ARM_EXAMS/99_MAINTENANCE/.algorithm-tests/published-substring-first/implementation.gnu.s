.syntax unified
.cpu cortex-m3
.thumb
.text
.global substring_first
substring_first:
        cmp r1,#0
        bmi ss_bad
        cmp r1,#0
        beq ss_pcheck
        cmp r0,#0
        beq ss_bad
ss_pcheck:
        cmp r3,#0
        beq ss_empty
        cmp r2,#0
        beq ss_bad
        cmp r3,r1
        bhi ss_absent
        push {r4-r10,lr}
        sub r4,r1,r3
        movs r5,#0
        movs r6,#0
ss_outer:
        cmp r5,r4
        bhi ss_done
        movs r7,#0
ss_inner:
        cmp r7,r3
        beq ss_found
        add r8,r5,r7
        ldrb r9,[r0,r8]
        ldrb r10,[r2,r7]
        cmp r9,r10
        bne ss_next
        adds r7,#1
        b ss_inner
ss_found:
        mov r0,r5
        pop {r4-r10,pc}
ss_next:
        adds r5,#1
        b ss_outer
ss_done:
        mvn r0,#0
        pop {r4-r10,pc}
ss_empty:
        movs r0,#0
        bx lr
ss_absent:
        mvn r0,#0
        bx lr
ss_bad:
        mvn r0,#0
        bx lr
.balign 4
