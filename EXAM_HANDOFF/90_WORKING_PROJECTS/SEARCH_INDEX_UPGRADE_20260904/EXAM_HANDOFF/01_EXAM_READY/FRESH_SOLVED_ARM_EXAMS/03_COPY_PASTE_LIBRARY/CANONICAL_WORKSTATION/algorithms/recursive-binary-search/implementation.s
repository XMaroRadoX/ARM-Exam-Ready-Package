; Recursive binary search
; int32_t recursive_binary_search(const int32_t *a, uint32_t n, int32_t key)
; Search ascending signed words, n<=INT32_MAX. Return a matching index or -1; any occurrence is allowed for duplicates. Empty or null input returns -1. At most 32 recursive frames.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT recursive_binary_search
recursive_binary_search
        cmp r0,#0
        beq bs_bad
        cmp r1,#0
        beq bs_bad
        bmi bs_bad
        push {r4,lr}
        lsrs r4,r1,#1
        ldr r3,[r0,r4,lsl #2]
        cmp r3,r2
        beq bs_found
        bgt bs_left
        adds r4,#1
        add r0,r0,r4,lsl #2
        sub r1,r1,r4
        bl recursive_binary_search
        cmp r0,#0
        blt bs_return
        add r0,r4
        b bs_return
bs_left
        mov r1,r4
        bl recursive_binary_search
        b bs_return
bs_found
        mov r0,r4
bs_return
        pop {r4,pc}
bs_bad
        mvn r0,#0
        bx lr

        ALIGN
        END
