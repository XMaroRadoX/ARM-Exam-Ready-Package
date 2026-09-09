; Insert an array element at an index
; int array_insert_at(int32_t *values, uint32_t *length,
;                     uint32_t capacity, uint32_t index, int32_t value)
; Insert before index, where index may equal the old length. Require length<capacity, index<=length, and valid storage. Invalid input returns 0 without changing the array or length.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_insert_at
array_insert_at
        ; R0=values, R1=length, R2=capacity, R3=index; value is at entry SP.
        cmp r0,#0
        beq ains_bad
        cmp r1,#0
        beq ains_bad
        ldr r12,[r1]
        cmp r12,r2
        bhs ains_bad
        cmp r3,r12
        bhi ains_bad
        push {r4,lr}
        ldr r4,[sp,#8]
        mov r2,r12
ains_shift
        cmp r2,r3
        beq ains_place
        sub r12,r2,#1
        ldr r12,[r0,r12,lsl #2]
        str r12,[r0,r2,lsl #2]
        subs r2,#1
        b ains_shift
ains_place
        str r4,[r0,r3,lsl #2]
        ldr r2,[r1]
        adds r2,#1
        str r2,[r1]
        movs r0,#1
        pop {r4,pc}
ains_bad
        movs r0,#0
        bx lr

        ALIGN
        END
