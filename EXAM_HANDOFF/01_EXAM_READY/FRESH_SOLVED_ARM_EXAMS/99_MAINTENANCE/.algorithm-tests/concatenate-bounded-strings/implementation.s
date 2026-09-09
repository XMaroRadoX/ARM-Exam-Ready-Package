; Concatenate bounded strings
; int string_concatenate_bounded(uint8_t *destination, uint32_t *length,
;                                uint32_t capacity, const uint8_t *source,
;                                uint32_t source_capacity)
; Append source to destination. destination[length] must be NUL, source must terminate within source_capacity, and the final NUL must fit. Validate everything before writing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT string_concatenate_bounded
string_concatenate_bounded
        ; R0=destination, R1=length, R2=capacity, R3=source; source_capacity is at entry SP.
        cmp r0,#0
        beq scb_bad
        cmp r1,#0
        beq scb_bad
        cmp r3,#0
        beq scb_bad
        push {r4-r9,lr}
        sub sp,sp,#4
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        ldr r9,[sp,#32]
        ldr r8,[r5]
        cmp r8,r6
        bhs scb_fail
        ldrb r0,[r4,r8]
        cmp r0,#0
        bne scb_fail
        mov r0,r7
        mov r1,r9
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt scb_fail
        sub r1,r6,r8
        subs r1,#1
        cmp r0,r1
        bhi scb_fail
        mov r2,r0
        movs r3,#0
scb_copy
        ldrb r1,[r7,r3]
        add r9,r8,r3
        strb r1,[r4,r9]
        adds r3,#1
        cmp r3,r2
        bls scb_copy
        add r8,r8,r2
        str r8,[r5]
        movs r0,#1
        b scb_return
scb_fail
        movs r0,#0
scb_return
        add sp,sp,#4
        pop {r4-r9,pc}
scb_bad
        movs r0,#0
        bx lr
        ; Local helper: R0=text, R1=capacity; return length or -1.
sbl_loop
        cmp r1,#0
        beq sbl_bad
        ldrb r2,[r0],#1
        cmp r2,#0
        beq sbl_done
        subs r1,#1
        adds r3,#1
        b sbl_loop
sbl_done
        mov r0,r3
        bx lr
sbl_bad
        mvn r0,#0
        bx lr
        ALIGN
        END
