; Sum of squared signed 16-bit differences
; uint64_t squared_differences_i16(const int16_t *a, const int16_t *b, uint32_t n)
; Return an exact 64-bit sum. Zero count or a null input pointer returns zero. Arrays each contain n elements; no outputs are mutated.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT squared_differences_i16
squared_differences_i16
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
        ldrsh r4,[r0],#2
        ldrsh r5,[r1],#2
        sub r4,r4,r5
        smull r4,r5,r4,r4
        adds r6,r6,r4
        adc r7,r7,r5
wr_next
        subs r2,#1
        b wr_loop
wr_done
        mov r0,r6
        mov r1,r7
        pop {r4-r8,pc}

        ALIGN
        END
