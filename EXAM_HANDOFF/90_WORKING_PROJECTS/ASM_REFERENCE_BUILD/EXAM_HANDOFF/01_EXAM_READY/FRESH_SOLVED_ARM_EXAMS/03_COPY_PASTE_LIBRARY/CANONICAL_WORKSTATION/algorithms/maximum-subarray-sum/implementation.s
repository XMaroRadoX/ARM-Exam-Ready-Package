; Maximum contiguous subarray sum
; int64_t maximum_subarray(const int32_t *a, uint32_t n)
; Return the maximum nonempty contiguous signed-word sum in 64 bits. Null or empty input returns zero; an all-negative array returns its largest element.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT maximum_subarray
maximum_subarray
        cmp r0,#0
        beq ms_zero
        cmp r1,#0
        beq ms_zero
        push {r4-r10,lr}
        ldr r4,[r0],#4
        asr r5,r4,#31
        mov r6,r4
        mov r7,r5
        subs r1,#1
ms_loop
        cmp r1,#0
        beq ms_done
        cmp r5,#0
        bge ms_add
        movs r4,#0
        movs r5,#0
ms_add
        ldr r8,[r0],#4
        asr r9,r8,#31
        adds r4,r4,r8
        adc r5,r5,r9
        cmp r5,r7
        bgt ms_best
        blt ms_next
        cmp r4,r6
        bls ms_next
ms_best
        mov r6,r4
        mov r7,r5
ms_next
        subs r1,#1
        b ms_loop
ms_done
        mov r0,r6
        mov r1,r7
        pop {r4-r10,pc}
ms_zero
        movs r0,#0
        movs r1,#0
        bx lr

        ALIGN
        END
