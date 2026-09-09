.syntax unified
.cpu cortex-m3
.thumb
.text
.global count_array_positive
count_array_positive:
        cmp r0,#0
        beq ack_zero
        push {r4,lr}
        movs r4,#0
ack_loop:
        cmp r1,#0
        beq ack_done
        ldr r3,[r0],#4
        cmp r3,#0
        ble ack_next
        adds r4,#1
ack_next:
        subs r1,#1
        b ack_loop
ack_done:
        mov r0,r4
        pop {r4,pc}
ack_zero:
        movs r0,#0
        bx lr
.balign 4
