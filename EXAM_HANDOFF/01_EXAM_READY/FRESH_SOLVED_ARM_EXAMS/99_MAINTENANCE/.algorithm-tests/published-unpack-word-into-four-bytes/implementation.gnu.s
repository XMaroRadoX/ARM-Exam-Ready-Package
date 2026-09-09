.syntax unified
.cpu cortex-m3
.thumb
.text
.global unpack_four_bytes_be
unpack_four_bytes_be:
        cmp r1,#0
        beq ufb_bad
        cmp r2,#4
        blo ufb_bad
        lsr r3,r0,#24
        strb r3,[r1]
        lsr r3,r0,#16
        strb r3,[r1,#1]
        lsr r3,r0,#8
        strb r3,[r1,#2]
        strb r0,[r1,#3]
        movs r0,#1
        bx lr
ufb_bad:
        movs r0,#0
        bx lr
.balign 4
