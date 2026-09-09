.syntax unified
.cpu cortex-m3
.thumb
.text
.global swap_byte_nibbles
swap_byte_nibbles:
        uxtb r0,r0
        lsl r1,r0,#4
        lsr r0,r0,#4
        orr r0,r0,r1
        uxtb r0,r0
        bx lr
.balign 4
