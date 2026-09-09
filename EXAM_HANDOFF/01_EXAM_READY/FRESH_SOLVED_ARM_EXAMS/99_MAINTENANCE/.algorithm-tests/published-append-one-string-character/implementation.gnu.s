.syntax unified
.cpu cortex-m3
.thumb
.text
.global string_append_character
string_append_character:
        cmp r0,#0
        beq sac_bad
        cmp r1,#0
        beq sac_bad
        cmp r3,#0
        beq sac_bad
        push {r4,lr}
        mov r4,r2
        ldr r12,[r1]
        cmp r12,r4
        bhs sac_fail
        add r2,r12,#1
        cmp r2,r4
        bhs sac_fail
        ldrb r4,[r0,r12]
        cmp r4,#0
        bne sac_fail
        strb r3,[r0,r12]
        movs r3,#0
        strb r3,[r0,r2]
        str r2,[r1]
        movs r0,#1
        pop {r4,pc}
sac_fail:
        movs r0,#0
        pop {r4,pc}
sac_bad:
        movs r0,#0
        bx lr
.balign 4
