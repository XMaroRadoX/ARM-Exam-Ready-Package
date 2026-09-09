; Replace every occurrence of a character
; uint32_t string_replace_character(uint8_t *text, uint32_t capacity,
;                                   uint8_t old_character, uint8_t new_character)
; Replace every old_character before NUL and return the replacement count. Both characters must be non-NUL. Invalid or unterminated input returns UINT32_MAX without modifying text.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT string_replace_character
string_replace_character
        ; R0=text, R1=capacity, R2=old byte, R3=new byte. Validate before mutation.
        cmp r0,#0
        beq src_bad
        cmp r2,#0
        beq src_bad
        cmp r3,#0
        beq src_bad
        push {r4-r7,lr}
        mov r4,r0
        mov r5,r2
        mov r6,r3
        movs r2,#0
src_validate
        cmp r2,r1
        bhs src_fail
        ldrb r7,[r4,r2]
        adds r2,#1
        cmp r7,#0
        bne src_validate
        subs r2,#1
        movs r0,#0
        movs r1,#0
src_loop
        cmp r1,r2
        bhs src_done
        ldrb r7,[r4,r1]
        cmp r7,r5
        bne src_next
        strb r6,[r4,r1]
        adds r0,#1
src_next
        adds r1,#1
        b src_loop
src_done
        pop {r4-r7,pc}
src_fail
        pop {r4-r7,lr}
src_bad
        mvn r0,#0
        bx lr

        ALIGN
        END
