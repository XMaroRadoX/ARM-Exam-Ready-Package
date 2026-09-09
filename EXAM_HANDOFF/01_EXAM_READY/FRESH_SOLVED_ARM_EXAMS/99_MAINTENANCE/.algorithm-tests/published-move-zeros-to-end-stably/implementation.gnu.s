.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_move_zeros_to_end
array_move_zeros_to_end:
        cmp r1,#0
        beq amz_yes
        cmp r0,#0
        beq amz_bad
        push {r4,lr}
        mov r2,r0
        mov r3,r0
        mov r4,r1
amz_read:
        ldr r12,[r2],#4
        cmp r12,#0
        beq amz_next
        str r12,[r3],#4
amz_next:
        subs r4,#1
        bne amz_read
amz_fill:
        cmp r3,r2
        bhs amz_done
        movs r12,#0
        str r12,[r3],#4
        b amz_fill
amz_done:
        pop {r4,lr}
amz_yes:
        movs r0,#1
        bx lr
amz_bad:
        movs r0,#0
        bx lr
.balign 4
