.syntax unified
.cpu cortex-m3
.thumb
.text
.global next_power_of_two_u32
next_power_of_two_u32:
        cmp r1,#0
        beq npt_bad
        cmp r0,#0
        beq npt_one
        cmp r0,#0x80000000
        bhi npt_bad
        subs r0,#1
        lsr r2,r0,#1
        orr r0,r0,r2
        lsr r2,r0,#2
        orr r0,r0,r2
        lsr r2,r0,#4
        orr r0,r0,r2
        lsr r2,r0,#8
        orr r0,r0,r2
        lsr r2,r0,#16
        orr r0,r0,r2
        adds r0,#1
        b npt_store
npt_one:
        movs r0,#1
npt_store:
        str r0,[r1]
        movs r0,#1
        bx lr
npt_bad:
        movs r0,#0
        bx lr
.balign 4
