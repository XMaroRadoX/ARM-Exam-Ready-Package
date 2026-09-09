.syntax unified
.cpu cortex-m3
.thumb
.text
.global string_last_occurrence
string_last_occurrence:
        cmp r0,#0
        beq soc_invalid
        cmp r2,#0
        beq soc_invalid
        push {r4-r7,lr}
        sub sp,sp,#4
        mov r5,r0
        mov r6,r2
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt soc_pop_invalid
        mov r7,r0
        mvn r4,#0
        movs r3,#0
soc_loop:
        cmp r3,r7
        bhs soc_done
        ldrb r12,[r5,r3]
        cmp r12,r6
        bne soc_next
        mov r4,r3
soc_next:
        adds r3,#1
        b soc_loop
soc_done:
        mov r0,r4
        add sp,sp,#4
        pop {r4-r7,pc}
soc_pop_invalid:
        add sp,sp,#4
        pop {r4-r7,lr}
soc_invalid:
        mvn r0,#1
        bx lr
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
