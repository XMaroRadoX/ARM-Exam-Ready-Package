; Find the first occurrence of a character
; int32_t string_first_occurrence(const uint8_t *text, uint32_t capacity, uint8_t target)
; Return a zero-based index, -1 when absent, or -2 for a null input, NUL target, zero capacity, or missing terminator. The complete bound is validated.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT string_first_occurrence
string_first_occurrence
        ; R0=text, R1=capacity, R2=target. Validate NUL before searching.
        cmp r0,#0
        beq soc_invalid
        cmp r2,#0
        beq soc_invalid
        push {r4-r7,lr}
        sub sp,sp,#4
        mov r5,r0
        mov r6,r2
        movs r3,#0
        bl sbl_loop
        cmp r0,#0
        blt soc_pop_invalid
        mov r7,r0
        mvn r4,#0
        movs r3,#0
soc_loop
        cmp r3,r7
        bhs soc_done
        ldrb r12,[r5,r3]
        cmp r12,r6
        bne soc_next
        mov r4,r3
        b soc_done
soc_next
        adds r3,#1
        b soc_loop
soc_done
        mov r0,r4
        add sp,sp,#4
        pop {r4-r7,pc}
soc_pop_invalid
        add sp,sp,#4
        pop {r4-r7,lr}
soc_invalid
        mvn r0,#1
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
