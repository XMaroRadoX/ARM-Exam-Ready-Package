.syntax unified
.cpu cortex-m3
.thumb
.text
.global recursive_binary_search
recursive_binary_search:
        cmp r0,#0
        beq bs_bad
        cmp r1,#0
        beq bs_bad
        bmi bs_bad
        push {r4,lr}
        lsrs r4,r1,#1
        ldr r3,[r0,r4,lsl #2]
        cmp r3,r2
        beq bs_found
        bgt bs_left
        adds r4,#1
        add r0,r0,r4,lsl #2
        sub r1,r1,r4
        bl recursive_binary_search
        cmp r0,#0
        blt bs_return
        add r0,r4
        b bs_return
bs_left:
        mov r1,r4
        bl recursive_binary_search
        b bs_return
bs_found:
        mov r0,r4
bs_return:
        pop {r4,pc}
bs_bad:
        mvn r0,#0
        bx lr
.balign 4
