; Copy an array safely with overlap
; int array_copy_overlap(int32_t *destination, uint32_t capacity,
;                        const int32_t *source, uint32_t count)
; Copy count words with memmove semantics. Require capacity>=count and valid nonempty pointers. Exact aliasing succeeds. Direction is chosen before writing so overlapping slices are preserved.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_copy_overlap
array_copy_overlap
        ; R0=destination, R1=capacity, R2=source, R3=count.
        cmp r1,r3
        blo aco_bad
        cmp r3,#0
        beq aco_yes
        cmp r0,#0
        beq aco_bad
        cmp r2,#0
        beq aco_bad
        cmp r0,r2
        beq aco_yes
        blo aco_forward
        sub r12,r0,r2
        cmp r12,r3,lsl #2
        bhs aco_forward
        add r0,r0,r3,lsl #2
        add r2,r2,r3,lsl #2
aco_backward
        ldr r12,[r2,#-4]!
        str r12,[r0,#-4]!
        subs r3,#1
        bne aco_backward
        b aco_yes
aco_forward
        ldr r12,[r2],#4
        str r12,[r0],#4
        subs r3,#1
        bne aco_forward
aco_yes
        movs r0,#1
        bx lr
aco_bad
        movs r0,#0
        bx lr

        ALIGN
        END
