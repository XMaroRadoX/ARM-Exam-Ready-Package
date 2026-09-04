.syntax unified
.cpu cortex-m3
.thumb
.text
.global bounded_collatz
bounded_collatz:
        cmp r0,#0
        beq bc_bad
        cmp r1,#0
        beq bc_bad
        push {r4,r5}
        movs r3,#0
        ldr r4,=1431655764
bc_loop:
        cmp r3,r2
        bhs bc_fail
        str r0,[r1,r3,lsl #2]
        adds r3,#1
        cmp r0,#1
        beq bc_done
        tst r0,#1
        beq bc_even
        cmp r0,r4
        bhi bc_fail
        add r0,r0,r0,lsl #1
        adds r0,#1
        b bc_loop
bc_even:
        lsrs r0,#1
        b bc_loop
bc_done:
        mov r0,r3
        pop {r4,r5}
        bx lr
bc_fail:
        pop {r4,r5}
bc_bad:
        movs r0,#0
        bx lr
.balign 4
