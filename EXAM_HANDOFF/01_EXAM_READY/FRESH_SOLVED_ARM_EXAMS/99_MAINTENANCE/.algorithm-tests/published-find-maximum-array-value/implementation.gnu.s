.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_maximum
array_maximum:
        cmp r0,#0
        beq axe_bad
        cmp r2,#0
        beq axe_bad
        cmp r1,#0
        beq axe_bad
        push {r4,lr}
        ldr r3,[r0],#4
        subs r1,#1
axe_loop:
        cmp r1,#0
        beq axe_done
        ldr r4,[r0],#4
        cmp r4,r3
        ble axe_next
        mov r3,r4
axe_next:
        subs r1,#1
        b axe_loop
axe_done:
        str r3,[r2]
        movs r0,#1
        pop {r4,pc}
axe_bad:
        movs r0,#0
        bx lr
.balign 4
