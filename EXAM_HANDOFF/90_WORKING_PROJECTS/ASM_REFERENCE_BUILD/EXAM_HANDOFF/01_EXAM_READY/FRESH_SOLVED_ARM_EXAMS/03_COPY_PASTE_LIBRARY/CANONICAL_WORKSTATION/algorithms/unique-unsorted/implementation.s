; Unsorted duplicate removal
; uint32_t unique_unsorted(int32_t *a, uint32_t n)
; Compact distinct values in place, preserving first occurrences; return new length. Null or empty input returns zero.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT unique_unsorted
unique_unsorted
        cmp r0,#0
        beq uq_zero
        push {r4-r6,lr}
        movs r2,#0
        movs r6,#0
uq_loop
        cmp r6,r1
        bhs uq_done
        ldr r3,[r0,r6,lsl #2]
        movs r4,#0
uq_find
        cmp r4,r2
        beq uq_write
        ldr r5,[r0,r4,lsl #2]
        cmp r3,r5
        beq uq_next
        adds r4,#1
        b uq_find
uq_write
        str r3,[r0,r2,lsl #2]
        adds r2,#1
uq_next
        adds r6,#1
        b uq_loop
uq_done
        mov r0,r2
        pop {r4-r6,pc}
uq_zero
        movs r0,#0
        bx lr

        ALIGN
        END
