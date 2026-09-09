.syntax unified
.cpu cortex-m3
.thumb
.text
.global matrix_row_maximum_i32
matrix_row_maximum_i32:
        ldr r12,[sp]
        cmp r0,#0
        beq mse_bad
        cmp r12,#0
        beq mse_bad
        cmp r1,#1
        blo mse_bad
        cmp r2,#1
        blo mse_bad
        cmp r1,#256
        bhi mse_bad
        cmp r2,#256
        bhi mse_bad
        cmp r3,r1
        bhs mse_bad
        push {r4-r6,lr}
        mov r4,r3
        mul r1,r4,r2
        add r0,r0,r1,lsl #2
        mov r1,r2
        ldr r3,[r0]
        subs r1,#1
mse_loop:
        cmp r1,#0
        beq mse_done
        add r0,r0,#4
        ldr r5,[r0]
        cmp r5,r3
        ble mse_next
        mov r3,r5
mse_next:
        subs r1,#1
        b mse_loop
mse_done:
        str r3,[r12]
        movs r0,#1
        pop {r4-r6,pc}
mse_bad:
        movs r0,#0
        bx lr
.balign 4
