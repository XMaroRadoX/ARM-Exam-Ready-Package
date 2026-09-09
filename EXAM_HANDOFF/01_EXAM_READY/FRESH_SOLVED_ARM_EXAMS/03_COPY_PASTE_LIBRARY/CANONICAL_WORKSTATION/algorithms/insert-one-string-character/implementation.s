; Insert one character at an index
; int string_insert_character(uint8_t *text, uint32_t *length,
;                             uint32_t capacity, uint32_t index,
;                             uint8_t character)
; Insert one non-NUL byte before index, where index may equal length. Require a valid current terminator and one spare byte. Invalid input writes nothing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT string_insert_character
string_insert_character
        ; R0=text, R1=length, R2=capacity, R3=index; character is at entry SP.
        cmp r0,#0
        beq sic_bad
        cmp r1,#0
        beq sic_bad
        ldr r12,[r1]
        cmp r3,r12
        bhi sic_bad
        sub r2,r2,r12
        cmp r2,#2
        blo sic_bad
        ldrb r2,[r0,r12]
        cmp r2,#0
        bne sic_bad
        add r2,r12,#1
        push {r4,lr}
        ldr r4,[sp,#8]
        and r4,r4,#255
        cmp r4,#0
        beq sic_fail
sic_shift
        cmp r2,r3
        beq sic_place
        sub r12,r2,#1
        ldrb r12,[r0,r12]
        strb r12,[r0,r2]
        subs r2,#1
        b sic_shift
sic_place
        strb r4,[r0,r3]
        ldr r2,[r1]
        adds r2,#1
        str r2,[r1]
        movs r0,#1
        pop {r4,pc}
sic_fail
        movs r0,#0
        pop {r4,pc}
sic_bad
        movs r0,#0
        bx lr

        ALIGN
        END
