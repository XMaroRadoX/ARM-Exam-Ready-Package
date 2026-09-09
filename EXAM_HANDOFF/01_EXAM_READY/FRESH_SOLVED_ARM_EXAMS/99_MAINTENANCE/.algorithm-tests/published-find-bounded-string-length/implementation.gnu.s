.syntax unified
.cpu cortex-m3
.thumb
.text
.global string_length_bounded
string_length_bounded:
        cmp r0,#0
        beq sbl_bad_main
        cmp r2,#0
        beq sbl_bad_main
        movs r3,#0
sbl_main_loop:
        cmp r3,r1
        bhs sbl_bad_main
        ldrb r12,[r0,r3]
        cmp r12,#0
        beq sbl_found
        adds r3,#1
        b sbl_main_loop
sbl_found:
        str r3,[r2]
        movs r0,#1
        bx lr
sbl_bad_main:
        movs r0,#0
        bx lr
.balign 4
