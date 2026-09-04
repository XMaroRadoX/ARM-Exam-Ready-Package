.syntax unified
.cpu cortex-m3
.thumb
.text
.global longest_one_run
longest_one_run:
        movs r1,#0
        movs r2,#0
        movs r3,#32
lo_loop:
        tst r0,#1
        beq lo_zero
        adds r1,#1
        cmp r1,r2
        bls lo_next
        mov r2,r1
        b lo_next
lo_zero:
        movs r1,#0
lo_next:
        lsrs r0,#1
        subs r3,#1
        bne lo_loop
        mov r0,r2
        bx lr
.balign 4
