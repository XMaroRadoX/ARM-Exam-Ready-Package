.syntax unified
.cpu cortex-m3
.thumb
.text
.global count_above
count_above:
        movs r3,#0
        cmp r0,#0
        beq ca_done
        push {r4,r5}
ca_loop:
        cmp r1,#0
        beq ca_pop
        ldr r4,[r0],#4
        cmp r4,r2
        ble ca_next
        adds r3,#1
ca_next:
        subs r1,#1
        b ca_loop
ca_pop:
        pop {r4,r5}
ca_done:
        mov r0,r3
        bx lr
.balign 4
