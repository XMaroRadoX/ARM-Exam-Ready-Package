; Delete one character at an index
; int string_delete_character(uint8_t *text, uint32_t *length,
;                             uint32_t index, uint8_t *removed_out)
; Delete index, return the removed byte, and preserve NUL termination. Require index<length and text[length] to be NUL. Invalid input writes nothing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT string_delete_character
string_delete_character
        ; R0=text, R1=length, R2=index, R3=removed_out.
        cmp r0,#0
        beq sdc_bad
        cmp r1,#0
        beq sdc_bad
        cmp r3,#0
        beq sdc_bad
        ldr r12,[r1]
        cmp r2,r12
        bhs sdc_bad
        push {r4,r5}
        ldrb r4,[r0,r12]
        cmp r4,#0
        bne sdc_fail
        ldrb r4,[r0,r2]
sdc_shift
        cmp r2,r12
        bhs sdc_done
        add r5,r2,#1
        ldrb r5,[r0,r5]
        strb r5,[r0,r2]
        adds r2,#1
        b sdc_shift
sdc_done
        subs r12,#1
        str r12,[r1]
        strb r4,[r3]
        pop {r4,r5}
        movs r0,#1
        bx lr
sdc_fail
        pop {r4,r5}
sdc_bad
        movs r0,#0
        bx lr

        ALIGN
        END
