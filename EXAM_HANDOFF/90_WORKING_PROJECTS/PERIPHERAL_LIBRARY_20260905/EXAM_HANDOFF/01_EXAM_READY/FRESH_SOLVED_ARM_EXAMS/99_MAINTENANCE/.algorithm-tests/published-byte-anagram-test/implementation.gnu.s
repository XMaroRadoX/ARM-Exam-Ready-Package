.syntax unified
.cpu cortex-m3
.thumb
.text
.global byte_anagram
byte_anagram:
        cmp r1,r3
        bne ag_bad
        cmp r1,#0
        beq ag_yes
        cmp r0,#0
        beq ag_bad
        cmp r2,#0
        beq ag_bad
        push {r4-r8,lr}
        sub sp,sp,#1024
        movs r3,#0
        movs r4,#0
ag_clear:
        str r3,[sp,r4]
        adds r4,#4
        cmp r4,#1024
        blo ag_clear
        movs r4,#0
ag_count:
        cmp r4,r1
        bhs ag_second
        ldrb r5,[r0,r4]
        lsl r5,r5,#2
        ldr r6,[sp,r5]
        adds r6,#1
        str r6,[sp,r5]
        adds r4,#1
        b ag_count
ag_second:
        movs r4,#0
ag_consume:
        cmp r4,r1
        bhs ag_ok
        ldrb r5,[r2,r4]
        lsl r5,r5,#2
        ldr r6,[sp,r5]
        cmp r6,#0
        beq ag_fail
        subs r6,#1
        str r6,[sp,r5]
        adds r4,#1
        b ag_consume
ag_ok:
        movs r0,#1
        b ag_finish
ag_fail:
        movs r0,#0
ag_finish:
        add sp,sp,#1024
        pop {r4-r8,pc}
ag_yes:
        movs r0,#1
        bx lr
ag_bad:
        movs r0,#0
        bx lr
.balign 4
