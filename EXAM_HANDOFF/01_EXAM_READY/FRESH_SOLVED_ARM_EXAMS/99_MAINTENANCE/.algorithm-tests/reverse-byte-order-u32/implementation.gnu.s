.syntax unified
.cpu cortex-m3
.thumb
.text
.global reverse_byte_order_u32
reverse_byte_order_u32:
        rev r0,r0
        bx lr
.balign 4
