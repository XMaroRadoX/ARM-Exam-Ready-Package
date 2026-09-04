; Recursive factorial
; int factorial_recursive(uint32_t n, uint32_t *out)
; Accept n=0..12. Return 1 and store n!, or 0 without writing. At most 13 helper frames of eight bytes.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT factorial_recursive
factorial_recursive
        cmp r1,#0
        beq fr_bad
        cmp r0,#12
        bhi fr_bad
        push {r4,lr}
        mov r4,r1
        bl fr_step
        str r0,[r4]
        movs r0,#1
        pop {r4,pc}
fr_bad
        movs r0,#0
        bx lr
fr_step
        push {r4,lr}
        mov r4,r0
        cmp r0,#0
        beq fr_base
        subs r0,#1
        bl fr_step
        mul r0,r4,r0
        pop {r4,pc}
fr_base
        movs r0,#1
        pop {r4,pc}
        ALIGN
        END
