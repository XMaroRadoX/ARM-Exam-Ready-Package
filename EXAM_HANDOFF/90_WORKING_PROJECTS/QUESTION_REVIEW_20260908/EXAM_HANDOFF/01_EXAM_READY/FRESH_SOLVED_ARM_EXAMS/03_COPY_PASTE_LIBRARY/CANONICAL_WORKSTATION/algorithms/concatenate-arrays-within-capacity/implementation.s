; Concatenate two arrays within capacity
; int array_concatenate(const int32_t *left, uint32_t left_count,
;                       const int32_t *right, uint32_t right_count,
;                       int32_t *output, uint32_t capacity)
; Write left followed by right. Reject count overflow, insufficient capacity, or invalid nonempty pointers before writing. The output must not overlap either input. Empty inputs are allowed.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_concatenate
array_concatenate
        ; R0-R3 hold left, left_count, right, right_count. Output and capacity are on the stack.
        ldr r12,[sp]
        push {r4-r8,lr}
        ldr r4,[sp,#28]
        adds r5,r1,r3
        bcs acon_bad
        cmp r4,r5
        blo acon_bad
        cmp r5,#0
        beq acon_yes
        cmp r12,#0
        beq acon_bad
        cmp r1,#0
        beq acon_right_check
        cmp r0,#0
        beq acon_bad
acon_right_check
        cmp r3,#0
        beq acon_copy_left
        cmp r2,#0
        beq acon_bad
acon_copy_left
        mov r4,r12
        mov r5,r1
acon_left_loop
        cmp r5,#0
        beq acon_copy_right
        ldr r6,[r0],#4
        str r6,[r4],#4
        subs r5,#1
        b acon_left_loop
acon_copy_right
        cmp r3,#0
        beq acon_yes
        ldr r6,[r2],#4
        str r6,[r4],#4
        subs r3,#1
        b acon_copy_right
acon_yes
        movs r0,#1
        pop {r4-r8,pc}
acon_bad
        movs r0,#0
        pop {r4-r8,pc}

        ALIGN
        END
