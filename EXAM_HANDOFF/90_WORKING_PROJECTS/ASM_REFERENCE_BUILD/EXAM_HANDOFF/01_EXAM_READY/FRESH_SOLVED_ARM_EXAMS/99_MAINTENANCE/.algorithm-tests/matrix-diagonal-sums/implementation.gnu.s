.syntax unified
.cpu cortex-m3
.thumb
.text
.global diagonal_sums
diagonal_sums:
        cmp r2,#0
        beq dg_bad
        cmp r3,#2
        blo dg_bad
        cmp r1,#256
        bhi dg_bad
        cmp r1,#0
        beq dg_start
        cmp r0,#0
        beq dg_bad
dg_start:
        push {r4-r8,lr}
        movs r4,#0
        movs r5,#0
        movs r6,#0
dg_loop:
        cmp r6,r1
        bhs dg_done
        mla r7,r6,r1,r6
        lsl r7,r7,#1
        ldrsh r8,[r0,r7]
        add r4,r8
        mul r7,r6,r1
        add r7,r1
        subs r7,#1
        sub r7,r6
        lsl r7,r7,#1
        ldrsh r8,[r0,r7]
        add r5,r8
        adds r6,#1
        b dg_loop
dg_done:
        str r4,[r2]
        asr r4,r4,#31
        str r4,[r2,#4]
        str r5,[r2,#8]
        asr r5,r5,#31
        str r5,[r2,#12]
        movs r0,#1
        pop {r4-r8,pc}
dg_bad:
        movs r0,#0
        bx lr
.balign 4
