.syntax unified
.cpu cortex-m3
.thumb
.text
.global leading_zero_count
leading_zero_count:
        cmp r0,#0
        beq z_all
        movs r1,#0
z_loop:
        tst r0,#0x80000000
        bne z_done
        adds r1,#1
        lsls r0,#1
        b z_loop
z_done:
        mov r0,r1
        bx lr
z_all:
        movs r0,#32
        bx lr
.balign 4
