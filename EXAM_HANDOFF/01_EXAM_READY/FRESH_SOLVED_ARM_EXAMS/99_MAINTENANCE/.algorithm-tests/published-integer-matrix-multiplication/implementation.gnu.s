.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_multiply_i16
matrix_multiply_i16:
        push {r4-r11,lr}
        sub sp,sp,#28
        ldr r4,[sp,#64]
        ldr r5,[sp,#68]
        ldr r6,[sp,#72]
        cmp r0,#0
        beq mm_bad
        cmp r1,#0
        beq mm_bad
        cmp r5,#0
        beq mm_bad
        cmp r2,#1
        blo mm_bad
        cmp r3,#1
        blo mm_bad
        cmp r4,#1
        blo mm_bad
        cmp r2,#256
        bhi mm_bad
        cmp r3,#256
        bhi mm_bad
        cmp r4,#256
        bhi mm_bad
        mul r7,r2,r4
        cmp r6,r7
        blo mm_bad
        str r0,[sp]
        str r1,[sp,#4]
        str r2,[sp,#8]
        str r3,[sp,#12]
        str r4,[sp,#16]
        str r5,[sp,#20]
        movs r6,#0
mm_rows:
        ldr r0,[sp,#8]
        cmp r6,r0
        bhs mm_good
        movs r7,#0
mm_cols:
        ldr r0,[sp,#16]
        cmp r7,r0
        bhs mm_nextrow
        movs r8,#0
        movs r9,#0
        movs r10,#0
mm_inner:
        ldr r0,[sp,#12]
        cmp r8,r0
        bhs mm_store
        mla r1,r6,r0,r8
        lsl r1,r1,#1
        ldr r2,[sp]
        ldrsh r3,[r2,r1]
        ldr r0,[sp,#16]
        mla r1,r8,r0,r7
        lsl r1,r1,#1
        ldr r2,[sp,#4]
        ldrsh r4,[r2,r1]
        smlal r9,r10,r3,r4
        adds r8,#1
        b mm_inner
mm_store:
        ldr r0,[sp,#20]
        str r9,[r0],#4
        str r10,[r0],#4
        str r0,[sp,#20]
        adds r7,#1
        b mm_cols
mm_nextrow:
        adds r6,#1
        b mm_rows
mm_good:
        movs r0,#1
        b mm_return
mm_bad:
        movs r0,#0
mm_return:
        add sp,sp,#28
        pop {r4-r11,pc}
.balign 4
