.syntax unified
.cpu cortex-m3
.thumb
.text
.global hysteresis_update
hysteresis_update:
        cmp r3,#0
        beq hy_bad
        uxth r0,r0
        uxth r1,r1
        uxth r2,r2
        cmp r1,r2
        bhs hy_bad
        ldrb r12,[r3]
        cmp r12,#0
        bne hy_on
        cmp r0,r2
        blo hy_done
        movs r0,#1
        strb r0,[r3]
        b hy_done
hy_on:
        cmp r0,r1
        bhi hy_done
        movs r0,#0
        strb r0,[r3]
hy_done:
        movs r0,#1
        bx lr
hy_bad:
        movs r0,#0
        bx lr
.balign 4
