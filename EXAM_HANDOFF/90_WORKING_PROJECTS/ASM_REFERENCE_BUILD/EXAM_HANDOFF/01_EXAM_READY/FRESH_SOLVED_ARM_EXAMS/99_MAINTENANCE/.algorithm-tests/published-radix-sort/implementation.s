; LSD radix sort
; int radix_sort_u32(uint32_t *a, size_t n, uint32_t *tmp)
; Stable unsigned sort using four byte passes. a and tmp each hold n words and must not overlap; exact alias is rejected. Empty input succeeds. Uses 256 word counters on the stack.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT radix_sort_u32
radix_sort_u32
        cmp r1,#0
        beq rx_yes
        cmp r0,#0
        beq rx_bad
        cmp r2,#0
        beq rx_bad
        cmp r0,r2
        beq rx_bad
        push {r4-r11,lr}
        sub sp,sp,#4
        sub sp,sp,#1024
        mov r4,r0
        mov r5,r1
        mov r6,r2
        movs r7,#0
rx_pass
        movs r8,#0
        movs r9,#0
rx_clear
        str r9,[sp,r8]
        adds r8,#4
        cmp r8,#1024
        blo rx_clear
        movs r8,#0
rx_count
        cmp r8,r5
        bhs rx_prefix_start
        ldr r10,[r4,r8,lsl #2]
        lsr r9,r10,r7
        and r9,r9,#255
        lsl r9,r9,#2
        ldr r11,[sp,r9]
        adds r11,#1
        str r11,[sp,r9]
        adds r8,#1
        b rx_count
rx_prefix_start
        movs r8,#0
        movs r10,#0
rx_prefix
        ldr r9,[sp,r8]
        str r10,[sp,r8]
        add r10,r9
        adds r8,#4
        cmp r8,#1024
        blo rx_prefix
        movs r8,#0
rx_scatter
        cmp r8,r5
        bhs rx_copy_start
        ldr r10,[r4,r8,lsl #2]
        lsr r9,r10,r7
        and r9,r9,#255
        lsl r9,r9,#2
        ldr r11,[sp,r9]
        str r10,[r6,r11,lsl #2]
        adds r11,#1
        str r11,[sp,r9]
        adds r8,#1
        b rx_scatter
rx_copy_start
        movs r8,#0
rx_copy
        cmp r8,r5
        bhs rx_next
        ldr r9,[r6,r8,lsl #2]
        str r9,[r4,r8,lsl #2]
        adds r8,#1
        b rx_copy
rx_next
        adds r7,#8
        cmp r7,#32
        blo rx_pass
        add sp,sp,#1024
        add sp,sp,#4
        pop {r4-r11,lr}
rx_yes
        movs r0,#1
        bx lr
rx_bad
        movs r0,#0
        bx lr

        ALIGN
        END
