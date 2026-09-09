.syntax unified
.cpu cortex-m3
.thumb
.text
.global toggle_bit_u32
toggle_bit_u32:
        cmp r1,#32
        bhs beo_bad
        cmp r2,#0
        beq beo_bad
        movs r3,#1
        lsl r3,r3,r1
        eor r0,r0,r3
        str r0,[r2]
        movs r0,#1
        bx lr
beo_bad:
        movs r0,#0
        bx lr
.balign 4
