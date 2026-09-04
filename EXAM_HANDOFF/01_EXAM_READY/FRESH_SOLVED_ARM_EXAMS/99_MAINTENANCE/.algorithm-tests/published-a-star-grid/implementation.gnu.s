.syntax unified
.cpu cortex-m3
.thumb
.text
.global astar_grid
astar_grid:
        push {r4-r11,lr}
        sub sp,sp,#28
        mov r4,r0
        mov r5,r1
        mov r6,r2
        ldr r7,[sp,#64]
        ldr r8,[sp,#68]
        ldr r9,[sp,#72]
        cmp r4,#0
        beq as_bad
        cmp r8,#0
        beq as_bad
        cmp r9,#0
        beq as_bad
        cmp r5,#1
        blo as_bad
        cmp r6,#1
        blo as_bad
        cmp r5,#256
        bhi as_bad
        cmp r6,#256
        bhi as_bad
        mul r10,r5,r6
        cmp r3,r10
        bhs as_bad
        cmp r7,r10
        bhs as_bad
        ldrb r0,[r4,r3]
        cmp r0,#0
        bne as_bad
        ldrb r0,[r4,r7]
        cmp r0,#0
        bne as_bad
        movs r0,#0
        mvn r1,#0
        movs r2,#0
as_init:
        cmp r0,r10
        bhs as_start
        str r1,[r8,r0,lsl #2]
        strb r2,[r9,r0]
        adds r0,#1
        b as_init
as_start:
        str r2,[r8,r3,lsl #2]
        udiv r0,r7,r6
        mls r1,r0,r6,r7
        str r0,[sp,#16]
        str r1,[sp,#20]
as_outer:
        str r10,[sp]
        mvn r0,#0
        str r0,[sp,#4]
        movs r0,#0
as_scan:
        cmp r0,r10
        bhs as_choose
        ldrb r1,[r9,r0]
        cmp r1,#0
        bne as_sn
        ldr r1,[r8,r0,lsl #2]
        cmn r1,#1
        beq as_sn
        udiv r2,r0,r6
        mls r3,r2,r6,r0
        ldr r11,[sp,#16]
        subs r2,r2,r11
        bpl as_rowabs
        rsb r2,r2,#0
as_rowabs:
        add r1,r2
        ldr r11,[sp,#20]
        subs r3,r3,r11
        bpl as_colabs
        rsb r3,r3,#0
as_colabs:
        add r1,r3
        ldr r2,[sp,#4]
        cmp r1,r2
        bhs as_sn
        str r1,[sp,#4]
        str r0,[sp]
as_sn:
        adds r0,#1
        b as_scan
as_choose:
        ldr r11,[sp]
        cmp r11,r10
        beq as_bad
        cmp r11,r7
        beq as_good
        movs r0,#1
        strb r0,[r9,r11]
        ldr r0,[r8,r11,lsl #2]
        adds r0,#1
        str r0,[sp,#8]
        cmp r11,r6
        blo as_down
        sub r0,r11,r6
        bl as_relax
as_down:
        add r0,r11,r6
        cmp r0,r10
        bhs as_left
        bl as_relax
as_left:
        udiv r0,r11,r6
        mls r0,r0,r6,r11
        cmp r0,#0
        beq as_right
        sub r0,r11,#1
        bl as_relax
as_right:
        udiv r0,r11,r6
        mls r0,r0,r6,r11
        adds r0,#1
        cmp r0,r6
        bhs as_outer
        add r0,r11,#1
        bl as_relax
        b as_outer
as_good:
        movs r0,#1
        b as_return
as_bad:
        movs r0,#0
as_return:
        add sp,sp,#28
        pop {r4-r11,pc}
as_relax:
        ldrb r1,[r4,r0]
        cmp r1,#0
        bne as_relax_done
        ldrb r1,[r9,r0]
        cmp r1,#0
        bne as_relax_done
        ldr r1,[r8,r0,lsl #2]
        ldr r2,[sp,#8]
        cmp r2,r1
        bhs as_relax_done
        str r2,[r8,r0,lsl #2]
as_relax_done:
        bx lr
.balign 4
