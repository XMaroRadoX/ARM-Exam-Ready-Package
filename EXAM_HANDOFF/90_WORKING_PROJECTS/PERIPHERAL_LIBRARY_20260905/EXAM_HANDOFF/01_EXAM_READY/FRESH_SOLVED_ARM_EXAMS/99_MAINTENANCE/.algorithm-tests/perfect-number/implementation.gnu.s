.syntax unified
.cpu cortex-m3
.thumb
.text
.global perfect_number
perfect_number:
        cmp r0,#2
        blo pn_bad
        push {r4,lr}
        mov r4,r0
        bl div_sum
        lsrs r2,r4,#31
        lsls r4,#1
        cmp r1,r2
        bne pn_fail
        cmp r0,r4
        bne pn_fail
        movs r0,#1
        pop {r4,pc}
pn_fail:
        movs r0,#0
        pop {r4,pc}
pn_bad:
        movs r0,#0
        bx lr
div_sum:
        push {r4-r8,lr}
        mov r4,r0
        movs r5,#1
        movs r6,#0
        movs r7,#0
        cmp r4,#0
        beq dv_done
dv_loop:
        udiv r8,r4,r5
        cmp r5,r8
        bhi dv_done
        mls r2,r8,r5,r4
        cmp r2,#0
        bne dv_next
        adds r6,r6,r5
        adc r7,r7,#0
        cmp r5,r8
        beq dv_next
        adds r6,r6,r8
        adc r7,r7,#0
dv_next:
        adds r5,#1
        b dv_loop
dv_done:
        mov r0,r6
        mov r1,r7
        pop {r4-r8,pc}
.balign 4
