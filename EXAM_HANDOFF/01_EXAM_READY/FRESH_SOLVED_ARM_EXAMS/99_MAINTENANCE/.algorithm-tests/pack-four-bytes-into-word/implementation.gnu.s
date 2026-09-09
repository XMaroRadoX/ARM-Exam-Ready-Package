.syntax unified
.cpu cortex-m3
.thumb
.text
.global pack_four_bytes_be
pack_four_bytes_be:
        uxtb r0,r0
        uxtb r1,r1
        uxtb r2,r2
        uxtb r3,r3
        lsl r0,r0,#24
        orr r0,r0,r1,lsl #16
        orr r0,r0,r2,lsl #8
        orr r0,r0,r3
        bx lr
.balign 4
