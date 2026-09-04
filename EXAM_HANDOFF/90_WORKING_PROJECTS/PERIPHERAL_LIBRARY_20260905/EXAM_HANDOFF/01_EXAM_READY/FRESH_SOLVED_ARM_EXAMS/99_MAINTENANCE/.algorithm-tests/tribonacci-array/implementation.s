; Tribonacci array generation
; int tribonacci_array(uint32_t *out, uint32_t count, uint32_t capacity)
; Seeds 0,0,1; accept count<=32, capacity>=count. Return 1 on success; invalid input returns 0 before writes. Empty output is valid.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT tribonacci_array
tribonacci_array
        cmp r1,#32
        bhi seq_bad
        cmp r1,r2
        bhi seq_bad
        cmp r1,#0
        beq seq_ok
        cmp r0,#0
        beq seq_bad
        push {r4,r5}
        movs r2,#0
seq_loop
        movs r3,#0
        cmp r2,#2
        blo seq_write
        mov r3,#1
        beq seq_write
        sub r3,r2,#1
        ldr r4,[r0,r3,lsl #2]
        subs r3,#1
        ldr r5,[r0,r3,lsl #2]
        add r4,r5
        subs r3,#1
        ldr r5,[r0,r3,lsl #2]
        add r3,r4,r5
seq_write
        str r3,[r0,r2,lsl #2]
        adds r2,#1
        cmp r2,r1
        blo seq_loop
        pop {r4,r5}
seq_ok
        movs r0,#1
        bx lr
seq_bad
        movs r0,#0
        bx lr

        ALIGN
        END
