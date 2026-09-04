.syntax unified
.cpu cortex-m3
.thumb
.text
.global armstrong_number
armstrong_number:
        push {r4-r10,lr}
        mov r4,r0
        mov r5,r0
        movs r6,#0
        movs r7,#10
an_count:
        adds r6,#1
        udiv r0,r0,r7
        cmp r0,#0
        bne an_count
        movs r8,#0
        movs r9,#0
an_digit:
        udiv r0,r5,r7
        mls r1,r0,r7,r5
        mov r5,r0
        mov r2,r6
        movs r3,#1
an_power:
        mul r3,r1,r3
        subs r2,#1
        bne an_power
        adds r8,r8,r3
        adc r9,r9,#0
        cmp r5,#0
        bne an_digit
        movs r0,#0
        cmp r9,#0
        bne an_done
        cmp r8,r4
        bne an_done
        movs r0,#1
an_done:
        pop {r4-r10,pc}
.balign 4
