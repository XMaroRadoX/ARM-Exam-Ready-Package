.syntax unified
.cpu cortex-m3
.thumb
.text
.global is_power_of_two_u32
is_power_of_two_u32:
        cmp r0,#0
        beq ipt_no
        sub r1,r0,#1
        tst r0,r1
        bne ipt_no
        movs r0,#1
        bx lr
ipt_no:
        movs r0,#0
        bx lr
.balign 4
