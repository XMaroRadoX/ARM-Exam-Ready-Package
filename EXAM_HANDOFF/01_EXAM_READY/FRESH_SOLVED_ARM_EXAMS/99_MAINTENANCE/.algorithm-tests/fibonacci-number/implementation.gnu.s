.syntax unified
.cpu cortex-m3
.thumb
.text
.global fibonacci_number
fibonacci_number:
        cmp r1,#0
        beq fn_bad
        cmp r0,#47
        bhi fn_bad
        movs r2,#0
        cmp r0,#0
        beq fn_store
        movs r3,#1
fn_loop:
        subs r0,#1
        beq fn_last
        add r12,r2,r3
        mov r2,r3
        mov r3,r12
        b fn_loop
fn_last:
        mov r2,r3
fn_store:
        str r2,[r1]
        movs r0,#1
        bx lr
fn_bad:
        movs r0,#0
        bx lr
.balign 4
