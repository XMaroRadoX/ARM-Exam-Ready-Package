.syntax unified
.cpu cortex-m3
.thumb
.text
.global string_delete_character
string_delete_character:
        cmp r0,#0
        beq sdc_bad
        cmp r1,#0
        beq sdc_bad
        cmp r3,#0
        beq sdc_bad
        ldr r12,[r1]
        cmp r2,r12
        bhs sdc_bad
        push {r4,r5}
        ldrb r4,[r0,r12]
        cmp r4,#0
        bne sdc_fail
        ldrb r4,[r0,r2]
sdc_shift:
        cmp r2,r12
        bhs sdc_done
        add r5,r2,#1
        ldrb r5,[r0,r5]
        strb r5,[r0,r2]
        adds r2,#1
        b sdc_shift
sdc_done:
        subs r12,#1
        str r12,[r1]
        strb r4,[r3]
        pop {r4,r5}
        movs r0,#1
        bx lr
sdc_fail:
        pop {r4,r5}
sdc_bad:
        movs r0,#0
        bx lr
.balign 4
