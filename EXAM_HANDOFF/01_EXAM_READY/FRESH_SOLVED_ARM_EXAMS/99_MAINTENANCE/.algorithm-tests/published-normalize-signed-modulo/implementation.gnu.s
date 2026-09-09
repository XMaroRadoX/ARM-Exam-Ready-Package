.syntax unified
.cpu cortex-m3
.thumb
.text
.global normalized_modulo_i32
normalized_modulo_i32:
        cmp r2,#0
        beq nmi_bad
        cmp r1,#0
        ble nmi_bad
        sdiv r3,r0,r1
        mls r12,r3,r1,r0
        cmp r12,#0
        bge nmi_store
        add r12,r12,r1
nmi_store:
        str r12,[r2]
        movs r0,#1
        bx lr
nmi_bad:
        movs r0,#0
        bx lr
.balign 4
