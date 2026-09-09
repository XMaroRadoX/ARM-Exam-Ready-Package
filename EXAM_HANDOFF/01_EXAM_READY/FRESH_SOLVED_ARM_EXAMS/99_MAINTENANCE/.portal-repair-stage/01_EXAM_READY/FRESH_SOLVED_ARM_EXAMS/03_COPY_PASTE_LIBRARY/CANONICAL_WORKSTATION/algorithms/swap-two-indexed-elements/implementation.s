; Swap two indexed elements
; int array_swap_indexes(int32_t *values, uint32_t count, uint32_t first, uint32_t second)
; Swap two elements only when both indexes are in range and storage is valid. Equal indexes are a successful no-op. Invalid input returns 0 without writing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_swap_indexes
array_swap_indexes
        ; R0=values, R1=count, R2=first, R3=second.
        cmp r0,#0
        beq asi_bad
        cmp r2,r1
        bhs asi_bad
        cmp r3,r1
        bhs asi_bad
        ldr r1,[r0,r2,lsl #2]
        ldr r12,[r0,r3,lsl #2]
        str r12,[r0,r2,lsl #2]
        str r1,[r0,r3,lsl #2]
        movs r0,#1
        bx lr
asi_bad
        movs r0,#0
        bx lr

        ALIGN
        END
