; Average two signed integers without overflow
; int32_t average_two_i32(int32_t left, int32_t right)
; Return (left+right)/2 with C signed-division semantics: truncate toward zero. The addition is formed as a signed 64-bit value, so opposite and extreme inputs cannot overflow.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT average_two_i32
average_two_i32
        ; R0=left,R1=right. R2:R3 is the signed 64-bit sum.
        asr r2,r0,#31
        asr r3,r1,#31
        adds r0,r0,r1
        adc r2,r2,r3
        cmp r2,#0
        bge ati_shift
        tst r0,#1
        beq ati_shift
        adds r0,#1
        adc r2,r2,#0
ati_shift
        lsrs r0,#1
        orr r0,r0,r2,lsl #31
        bx lr

        ALIGN
        END
