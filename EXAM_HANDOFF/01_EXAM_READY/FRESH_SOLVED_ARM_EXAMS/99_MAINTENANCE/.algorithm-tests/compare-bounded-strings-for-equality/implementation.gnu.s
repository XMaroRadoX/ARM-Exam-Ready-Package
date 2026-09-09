.syntax unified
.cpu cortex-m3
.thumb
.text
.global strings_equal_bounded
strings_equal_bounded:
        push {r4-r8,lr}
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt seq_invalid
        mov r8,r0
        mov r0,r6
        mov r1,r7
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt seq_invalid
        cmp r8,r0
        bne seq_no
        mov r1,r8
seq_loop:
        cmp r1,#0
        beq seq_yes
        ldrb r2,[r4],#1
        ldrb r3,[r6],#1
        cmp r2,r3
        bne seq_no
        subs r1,#1
        b seq_loop
seq_yes:
        movs r0,#1
        pop {r4-r8,pc}
seq_no:
        movs r0,#0
        pop {r4-r8,pc}
seq_invalid:
        mvn r0,#0
        pop {r4-r8,pc}
sbl_loop:
        cmp r1,#0
        beq sbl_bad
        ldrb r2,[r0],#1
        cmp r2,#0
        beq sbl_done
        subs r1,#1
        adds r3,#1
        b sbl_loop
sbl_done:
        mov r0,r3
        bx lr
sbl_bad:
        mvn r0,#0
        bx lr
.balign 4
