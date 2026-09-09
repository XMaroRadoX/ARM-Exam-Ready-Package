.syntax unified
.cpu cortex-m3
.thumb
.text
.global test_bit_u32
test_bit_u32:
        cmp r1,#32
        bhs beo_bad
        cmp r2,#0
        beq beo_bad
        lsr r0,r0,r1
        and r0,r0,#1
        str r0,[r2]
        movs r0,#1
        bx lr
beo_bad:
        movs r0,#0
        bx lr
.balign 4
