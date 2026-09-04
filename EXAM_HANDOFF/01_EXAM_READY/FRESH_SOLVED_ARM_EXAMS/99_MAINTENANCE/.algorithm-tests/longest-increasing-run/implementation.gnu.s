.syntax unified
.cpu cortex-m3
.thumb
.text
.global longest_increasing_run
longest_increasing_run:
        cmp r0,#0
        beq lr_bad
        cmp r1,#0
        beq lr_bad
        push {r4-r6,lr}
        ldr r2,[r0],#4
        movs r3,#1
        movs r4,#1
        subs r1,#1
lr_loop:
        cmp r1,#0
        beq lr_done
        ldr r5,[r0],#4
        cmp r5,r2
        ble lr_reset
        adds r3,#1
        b lr_max
lr_reset:
        movs r3,#1
lr_max:
        cmp r3,r4
        bls lr_next
        mov r4,r3
lr_next:
        mov r2,r5
        subs r1,#1
        b lr_loop
lr_done:
        mov r0,r4
        pop {r4-r6,pc}
lr_bad:
        movs r0,#0
        bx lr
.balign 4
