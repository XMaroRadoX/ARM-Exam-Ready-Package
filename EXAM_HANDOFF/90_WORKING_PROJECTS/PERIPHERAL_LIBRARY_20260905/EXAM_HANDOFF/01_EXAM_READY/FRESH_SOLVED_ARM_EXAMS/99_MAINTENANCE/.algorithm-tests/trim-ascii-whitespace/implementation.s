; Trim leading and trailing ASCII whitespace
; uint32_t trim_ascii(uint8_t *text, uint32_t length)
; Compact the trimmed byte span in place, without appending a terminator. Whitespace is space or byte 9..13. Return remaining length; null input returns zero.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT trim_ascii
trim_ascii
        cmp r0,#0
        beq tr_bad
        push {r4-r8,lr}
        mov r4,r0
        mov r5,r1
        movs r6,#0
tr_left
        cmp r6,r5
        bhs tr_right
        ldrb r3,[r4,r6]
        bl trim_space
        cmp r3,#0
        beq tr_right
        adds r6,#1
        b tr_left
tr_right
        cmp r5,r6
        bls tr_move
        sub r7,r5,#1
        ldrb r3,[r4,r7]
        bl trim_space
        cmp r3,#0
        beq tr_move
        subs r5,#1
        b tr_right
tr_move
        sub r0,r5,r6
        movs r7,#0
tr_copy
        cmp r7,r0
        bhs tr_done
        add r8,r6,r7
        ldrb r3,[r4,r8]
        strb r3,[r4,r7]
        adds r7,#1
        b tr_copy
tr_done
        pop {r4-r8,pc}
tr_bad
        movs r0,#0
        bx lr
trim_space
        cmp r3,#32
        beq tw_true
        cmp r3,#9
        blo tw_false
        cmp r3,#13
        bhi tw_false
tw_true
        movs r3,#1
        bx lr
tw_false
        movs r3,#0
        bx lr
        ALIGN
        END
