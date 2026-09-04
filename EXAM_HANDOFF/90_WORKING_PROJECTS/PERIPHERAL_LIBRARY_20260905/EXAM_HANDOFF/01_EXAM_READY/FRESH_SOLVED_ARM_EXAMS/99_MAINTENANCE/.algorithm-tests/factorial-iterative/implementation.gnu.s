.syntax unified
.cpu cortex-m3
.thumb
.text
.global factorial_iterative
factorial_iterative:
        cmp r1,#0
        beq fi_bad
        cmp r0,#12
        bhi fi_bad
        movs r2,#1
fi_loop:
        cmp r0,#0
        beq fi_done
        mul r2,r0,r2
        subs r0,#1
        b fi_loop
fi_done:
        str r2,[r1]
        movs r0,#1
        bx lr
fi_bad:
        movs r0,#0
        bx lr
.balign 4
