; Iterative factorial
; int factorial_iterative(uint32_t n, uint32_t *out)
; Accept n=0..12 and a valid output pointer. Return 1 and write n!, or 0 without writing.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT factorial_iterative
factorial_iterative
        cmp r1,#0
        beq fi_bad
        cmp r0,#12
        bhi fi_bad
        movs r2,#1
fi_loop
        cmp r0,#0
        beq fi_done
        mul r2,r0,r2
        subs r0,#1
        b fi_loop
fi_done
        str r2,[r1]
        movs r0,#1
        bx lr
fi_bad
        movs r0,#0
        bx lr

        ALIGN
        END
