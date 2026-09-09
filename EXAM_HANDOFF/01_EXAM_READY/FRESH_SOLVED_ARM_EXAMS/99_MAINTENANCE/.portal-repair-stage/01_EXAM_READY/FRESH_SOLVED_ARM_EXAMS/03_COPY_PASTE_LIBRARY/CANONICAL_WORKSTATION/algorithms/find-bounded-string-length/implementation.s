; Find bounded string length
; int string_length_bounded(const uint8_t *text, uint32_t capacity, uint32_t *length_out)
; Find NUL within capacity and return its index through length_out. A null pointer, zero capacity, or missing terminator returns 0 without changing the output.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT string_length_bounded
string_length_bounded
        ; R0=text, R1=capacity, R2=length_out. R3 is the current index.
        cmp r0,#0
        beq sbl_bad_main
        cmp r2,#0
        beq sbl_bad_main
        movs r3,#0
sbl_main_loop
        cmp r3,r1
        bhs sbl_bad_main
        ldrb r12,[r0,r3]
        cmp r12,#0
        beq sbl_found
        adds r3,#1
        b sbl_main_loop
sbl_found
        str r3,[r2]
        movs r0,#1
        bx lr
sbl_bad_main
        movs r0,#0
        bx lr

        ALIGN
        END
