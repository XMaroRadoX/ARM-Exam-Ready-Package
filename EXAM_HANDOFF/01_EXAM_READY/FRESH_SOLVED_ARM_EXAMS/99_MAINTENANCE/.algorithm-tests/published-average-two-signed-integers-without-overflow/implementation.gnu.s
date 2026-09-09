.syntax unified
.cpu cortex-m3
.thumb
.text
.global average_two_i32
average_two_i32:
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
ati_shift:
        lsrs r0,#1
        orr r0,r0,r2,lsl #31
        bx lr
.balign 4
