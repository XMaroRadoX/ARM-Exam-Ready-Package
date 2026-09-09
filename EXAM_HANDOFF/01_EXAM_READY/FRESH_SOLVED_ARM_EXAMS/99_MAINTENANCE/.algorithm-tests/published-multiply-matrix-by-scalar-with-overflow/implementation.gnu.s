.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_scalar_multiply_i32
matrix_scalar_multiply_i32:
        ldr r12,[sp]
        push {r4-r9,lr}
        sub sp,sp,#4
        ldr r4,[sp,#36]
        cmp r1,#256
        bhi msm_fail
        cmp r2,#256
        bhi msm_fail
        mul r5,r1,r2
        cmp r4,r5
        blo msm_fail
        cmp r5,#0
        beq msm_yes
        cmp r0,#0
        beq msm_fail
        cmp r12,#0
        beq msm_fail
        movs r6,#0
msm_check:
        cmp r6,r5
        bhs msm_write_start
        ldr r7,[r0,r6,lsl #2]
        smull r8,r9,r7,r3
        asr r7,r8,#31
        cmp r9,r7
        bne msm_fail
        adds r6,#1
        b msm_check
msm_write_start:
        movs r6,#0
msm_write:
        cmp r6,r5
        bhs msm_yes
        ldr r7,[r0,r6,lsl #2]
        mul r7,r3,r7
        str r7,[r12,r6,lsl #2]
        adds r6,#1
        b msm_write
msm_yes:
        movs r0,#1
        b msm_return
msm_fail:
        movs r0,#0
msm_return:
        add sp,sp,#4
        pop {r4-r9,pc}
.balign 4
