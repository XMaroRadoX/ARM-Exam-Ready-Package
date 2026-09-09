.syntax unified
.cpu cortex-m3
.thumb
.text
.global strings_compare_ascii_casefold
strings_compare_ascii_casefold:
        push {r4-r8,lr}
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt scf_bad
        mov r0,r6
        mov r1,r7
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt scf_bad
scf_loop:
        ldrb r2,[r4],#1
        ldrb r3,[r6],#1
        cmp r2,#65
        blo scf_right
        cmp r2,#90
        bhi scf_right
        adds r2,#32
scf_right:
        cmp r3,#65
        blo scf_compare
        cmp r3,#90
        bhi scf_compare
        adds r3,#32
scf_compare:
        cmp r2,r3
        blo scf_less
        bhi scf_more
        cmp r2,#0
        bne scf_loop
        movs r0,#0
        pop {r4-r8,pc}
scf_less:
        mvn r0,#0
        pop {r4-r8,pc}
scf_more:
        movs r0,#1
        pop {r4-r8,pc}
scf_bad:
        movs r0,#2
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
