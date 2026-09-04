.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =byte_data
        LDRB R0, [R1]
        LDRSB R2, [R1]
        B after_byte
byte_data:
.byte 0xFE
.balign 2
after_byte:
