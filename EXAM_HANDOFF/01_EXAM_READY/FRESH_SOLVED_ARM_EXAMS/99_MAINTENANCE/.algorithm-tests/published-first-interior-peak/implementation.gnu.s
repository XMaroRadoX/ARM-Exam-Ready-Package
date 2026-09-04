.syntax unified
.cpu cortex-m3
.thumb
.text
.global first_peak
first_peak:
        cmp r0,#0
        beq pk_bad
        cmp r1,#3
        blo pk_bad
        cmp r1,#0
        bmi pk_bad
        push {r4-r6,lr}
        movs r2,#1
        subs r1,#1
pk_loop:
        cmp r2,r1
        bhs pk_fail
        sub r3,r2,#1
        ldr r4,[r0,r3,lsl #2]
        ldr r5,[r0,r2,lsl #2]
        cmp r5,r4
        ble pk_next
        add r3,r2,#1
        ldr r6,[r0,r3,lsl #2]
        cmp r5,r6
        ble pk_next
        mov r0,r2
        pop {r4-r6,pc}
pk_next:
        adds r2,#1
        b pk_loop
pk_fail:
        pop {r4-r6,lr}
pk_bad:
        mvn r0,#0
        bx lr
.balign 4
