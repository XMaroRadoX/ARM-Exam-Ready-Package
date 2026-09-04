.syntax unified
.cpu cortex-m3
.thumb
.text
.global word_hamming
word_hamming:
        eor r0,r0,r1
        movs r1,#0
wh_loop:
        cmp r0,#0
        beq wh_done
        sub r2,r0,#1
        and r0,r0,r2
        adds r1,#1
        b wh_loop
wh_done:
        mov r0,r1
        bx lr
.balign 4
