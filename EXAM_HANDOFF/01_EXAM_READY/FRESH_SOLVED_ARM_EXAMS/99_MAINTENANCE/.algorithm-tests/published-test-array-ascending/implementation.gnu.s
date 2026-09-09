.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_is_ascending
array_is_ascending:
        cmp r1,#0
        beq aia_yes
        cmp r0,#0
        beq aia_no
        ldr r2,[r0],#4
        subs r1,#1
aia_loop:
        cmp r1,#0
        beq aia_yes
        ldr r3,[r0],#4
        cmp r3,r2
        blt aia_no
        mov r2,r3
        subs r1,#1
        b aia_loop
aia_yes:
        movs r0,#1
        bx lr
aia_no:
        movs r0,#0
        bx lr
.balign 4
