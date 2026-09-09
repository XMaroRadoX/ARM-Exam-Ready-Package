.syntax unified
.cpu cortex-m3
.thumb
.text
.global integer_array_mean
integer_array_mean:
        cmp r0,#0
        beq iam_bad
        cmp r2,#0
        beq iam_bad
        cmp r1,#0
        beq iam_bad
        bmi iam_bad
        push {r4-r8,lr}
        mov r4,r0
        mov r5,r1
        mov r6,r2
        movs r7,#0
        movs r8,#0
        mov r12,r5
iam_loop:
        ldr r0,[r4],#4
        asr r1,r0,#31
        adds r7,r7,r0
        adc r8,r8,r1
        subs r12,#1
        bne iam_loop
        mov r0,r7
        mov r1,r8
        mov r2,r5
        movs r3,#0
        bl __aeabi_ldivmod
        str r0,[r6]
        movs r0,#1
        pop {r4-r8,pc}
iam_bad:
        movs r0,#0
        bx lr
.extern __aeabi_ldivmod
.balign 4
