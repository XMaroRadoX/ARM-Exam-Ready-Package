; Test whether a string ends with a suffix
; int32_t string_ends_with(const uint8_t *text, uint32_t text_capacity,
;                          const uint8_t *affix, uint32_t affix_capacity)
; Return 1 for a match, 0 for no match, and -1 for invalid or unterminated input. The empty affix matches every valid string.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT string_ends_with
string_ends_with
        ; R0=text,R1=text_capacity,R2=affix,R3=affix_capacity.
        push {r4-r9,lr}
        sub sp,sp,#4
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt saf_bad
        mov r8,r0
        mov r0,r6
        mov r1,r7
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt saf_bad
        mov r9,r0
        cmp r9,r8
        bhi saf_no
        sub r5,r8,r9
        movs r7,#0
saf_loop
        cmp r7,r9
        bhs saf_yes
        add r0,r5,r7
        ldrb r1,[r4,r0]
        ldrb r2,[r6,r7]
        cmp r1,r2
        bne saf_no
        adds r7,#1
        b saf_loop
saf_yes
        movs r0,#1
        b saf_return
saf_no
        movs r0,#0
        b saf_return
saf_bad
        mvn r0,#0
saf_return
        add sp,sp,#4
        pop {r4-r9,pc}
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
