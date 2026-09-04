.syntax unified
.cpu cortex-m3
.thumb
.text
.global byte_count
byte_count:
        movs r3,#0
        cmp r0,#0
        beq cc_done
        push {r4,r5}
        uxtb r2,r2
cc_loop:
        cmp r1,#0
        beq cc_pop
        ldrb r4,[r0],#1
        cmp r4,r2
        bne cc_next
        adds r3,#1
cc_next:
        subs r1,#1
        b cc_loop
cc_pop:
        pop {r4,r5}
cc_done:
        mov r0,r3
        bx lr
.balign 4
