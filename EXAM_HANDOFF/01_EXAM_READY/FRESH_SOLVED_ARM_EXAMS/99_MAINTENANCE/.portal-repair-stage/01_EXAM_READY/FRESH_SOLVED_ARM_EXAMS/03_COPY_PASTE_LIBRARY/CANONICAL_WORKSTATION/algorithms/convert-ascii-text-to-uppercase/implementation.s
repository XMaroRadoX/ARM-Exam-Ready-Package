; Convert ASCII text to uppercase
; int string_to_ascii_uppercase(uint8_t *text, uint32_t capacity)
; Convert ASCII letters in place; digits, punctuation, and non-ASCII bytes remain unchanged. Missing NUL or invalid storage returns 0 before any mutation.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT string_to_ascii_uppercase
string_to_ascii_uppercase
        ; R0=text, R1=capacity. First find NUL, then convert safely.
        cmp r0,#0
        beq scc_bad
        push {r4-r6,lr}
        mov r4,r0
        movs r2,#0
scc_validate
        cmp r2,r1
        bhs scc_fail
        ldrb r3,[r4,r2]
        adds r2,#1
        cmp r3,#0
        bne scc_validate
        subs r2,#1
        movs r3,#0
scc_loop
        cmp r3,r2
        bhs scc_done
        ldrb r5,[r4,r3]
        cmp r5,#97
        blo scc_next
        cmp r5,#122
        bhi scc_next
        subs r5,#32
        strb r5,[r4,r3]
scc_next
        adds r3,#1
        b scc_loop
scc_done
        movs r0,#1
        pop {r4-r6,pc}
scc_fail
        movs r0,#0
        pop {r4-r6,pc}
scc_bad
        movs r0,#0
        bx lr

        ALIGN
        END
