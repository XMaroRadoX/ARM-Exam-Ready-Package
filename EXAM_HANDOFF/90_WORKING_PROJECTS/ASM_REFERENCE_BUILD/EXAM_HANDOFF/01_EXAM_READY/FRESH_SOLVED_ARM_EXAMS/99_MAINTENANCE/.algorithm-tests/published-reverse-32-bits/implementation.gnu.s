.syntax unified
.cpu cortex-m3
.thumb
.text
.global reverse_bits
reverse_bits:
        movs r1,#0
        movs r2,#32
rb_loop:
        lsrs r0,#1
        adc r1,r1,r1
        subs r2,#1
        bne rb_loop
        mov r0,r1
        bx lr
.balign 4
