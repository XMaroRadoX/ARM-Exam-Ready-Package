.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_symmetric
matrix_symmetric:
        cmp r1,#256
        bhi sy_bad
        cmp r1,#0
        beq sy_yes
        cmp r0,#0
        beq sy_bad
        push {r4-r8,lr}
        movs r2,#0
sy_outer:
        cmp r2,r1
        bhs sy_ok
        add r3,r2,#1
sy_inner:
        cmp r3,r1
        bhs sy_next
        mla r4,r2,r1,r3
        mla r5,r3,r1,r2
        ldr r6,[r0,r4,lsl #2]
        ldr r7,[r0,r5,lsl #2]
        cmp r6,r7
        bne sy_fail
        adds r3,#1
        b sy_inner
sy_next:
        adds r2,#1
        b sy_outer
sy_ok:
        pop {r4-r8,lr}
sy_yes:
        movs r0,#1
        bx lr
sy_fail:
        pop {r4-r8,lr}
sy_bad:
        movs r0,#0
        bx lr
.balign 4
