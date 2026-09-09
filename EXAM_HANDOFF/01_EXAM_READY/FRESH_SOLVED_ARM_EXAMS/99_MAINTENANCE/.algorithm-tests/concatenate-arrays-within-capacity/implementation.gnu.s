.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_concatenate
array_concatenate:
        ldr r12,[sp]
        push {r4-r8,lr}
        ldr r4,[sp,#28]
        adds r5,r1,r3
        bcs acon_bad
        cmp r4,r5
        blo acon_bad
        cmp r5,#0
        beq acon_yes
        cmp r12,#0
        beq acon_bad
        cmp r1,#0
        beq acon_right_check
        cmp r0,#0
        beq acon_bad
acon_right_check:
        cmp r3,#0
        beq acon_copy_left
        cmp r2,#0
        beq acon_bad
acon_copy_left:
        mov r4,r12
        mov r5,r1
acon_left_loop:
        cmp r5,#0
        beq acon_copy_right
        ldr r6,[r0],#4
        str r6,[r4],#4
        subs r5,#1
        b acon_left_loop
acon_copy_right:
        cmp r3,#0
        beq acon_yes
        ldr r6,[r2],#4
        str r6,[r4],#4
        subs r3,#1
        b acon_copy_right
acon_yes:
        movs r0,#1
        pop {r4-r8,pc}
acon_bad:
        movs r0,#0
        pop {r4-r8,pc}
.balign 4
