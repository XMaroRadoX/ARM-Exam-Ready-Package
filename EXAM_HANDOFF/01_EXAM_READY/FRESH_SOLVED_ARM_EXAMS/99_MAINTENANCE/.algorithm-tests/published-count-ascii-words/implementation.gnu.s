.syntax unified
.cpu cortex-m3
.thumb
.text
.global string_count_ascii_words
string_count_ascii_words:
        cmp r0,#0
        beq scw_bad
        cmp r1,#0
        bmi scw_bad
        push {r4-r6,lr}
        mov r5,r0
        mov r6,r1
        movs r2,#0
scw_validate:
        cmp r2,r6
        bhs scw_fail
        ldrb r3,[r5,r2]
        adds r2,#1
        cmp r3,#0
        bne scw_validate
        subs r2,#1
        movs r3,#0
        movs r4,#0
        movs r1,#0
scw_loop:
        cmp r1,r2
        bhs scw_done
        ldrb r0,[r5,r1]
        cmp r0,#32
        beq scw_space
        cmp r0,#9
        blo scw_nonspace
        cmp r0,#13
        bls scw_space
scw_nonspace:
        cmp r4,#0
        bne scw_next
        adds r3,#1
        movs r4,#1
        b scw_next
scw_space:
        movs r4,#0
scw_next:
        adds r1,#1
        b scw_loop
scw_done:
        mov r0,r3
        pop {r4-r6,pc}
scw_fail:
        pop {r4-r6,lr}
scw_bad:
        mvn r0,#0
        bx lr
.balign 4
