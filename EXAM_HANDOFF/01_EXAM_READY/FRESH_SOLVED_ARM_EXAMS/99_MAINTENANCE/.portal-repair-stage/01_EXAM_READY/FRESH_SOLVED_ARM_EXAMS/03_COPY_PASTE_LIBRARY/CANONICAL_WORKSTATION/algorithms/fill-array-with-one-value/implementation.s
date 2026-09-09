; Fill an array with one value
; int array_fill(int32_t *values, uint32_t count, int32_t fill_value)
; Store fill_value in every element. Empty input succeeds without dereferencing the pointer; a null pointer with nonzero count fails.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_fill
array_fill
        ; R0=values, R1=count, R2=fill_value.
        cmp r1,#0
        beq afl_yes
        cmp r0,#0
        beq afl_bad
afl_loop
        str r2,[r0],#4
        subs r1,#1
        bne afl_loop
afl_yes
        movs r0,#1
        bx lr
afl_bad
        movs r0,#0
        bx lr

        ALIGN
        END
