; Total bit differences between word arrays
; uint64_t array_bit_differences(const uint32_t *a, const uint32_t *b, uint32_t n)
; Return an exact 64-bit sum. Zero count or a null input pointer returns zero. Arrays each contain n elements; no outputs are mutated.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_bit_differences
array_bit_differences
        push {r4-r8,lr}
        movs r6,#0
        movs r7,#0
        cmp r0,#0
        beq wr_done
        cmp r1,#0
        beq wr_done
wr_loop
        cmp r2,#0
        beq wr_done
        ldr r4,[r0],#4
        ldr r5,[r1],#4
        eor r4,r4,r5
wr_bits
        cmp r4,#0
        beq wr_next
        sub r5,r4,#1
        and r4,r4,r5
        adds r6,#1
        adc r7,r7,#0
        b wr_bits
wr_next
        subs r2,#1
        b wr_loop
wr_done
        mov r0,r6
        mov r1,r7
        pop {r4-r8,pc}

        ALIGN
        END
