.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_minimum_i32
matrix_minimum_i32:
        cmp r0,#0
        beq mex_bad
        cmp r3,#0
        beq mex_bad
        cmp r1,#1
        blo mex_bad
        cmp r2,#1
        blo mex_bad
        cmp r1,#256
        bhi mex_bad
        cmp r2,#256
        bhi mex_bad
        mul r1,r1,r2
        push {r4,lr}
        ldr r2,[r0],#4
        subs r1,#1
mex_loop:
        cmp r1,#0
        beq mex_done
        ldr r4,[r0],#4
        cmp r4,r2
        bge mex_next
        mov r2,r4
mex_next:
        subs r1,#1
        b mex_loop
mex_done:
        str r2,[r3]
        movs r0,#1
        pop {r4,pc}
mex_bad:
        movs r0,#0
        bx lr
.balign 4
