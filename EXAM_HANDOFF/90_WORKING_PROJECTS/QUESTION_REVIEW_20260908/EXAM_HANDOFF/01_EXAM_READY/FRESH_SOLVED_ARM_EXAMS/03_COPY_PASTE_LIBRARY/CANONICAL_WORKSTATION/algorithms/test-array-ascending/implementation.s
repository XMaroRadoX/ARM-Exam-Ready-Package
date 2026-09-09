; Test whether an array is ascending
; int array_is_ascending(const int32_t *values, uint32_t count)
; Return 1 when every adjacent pair is in nondecreasing signed order. Empty and one-element arrays are ascending; a null pointer is valid only for count zero.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT array_is_ascending
array_is_ascending
        ; R0=values, R1=count. R2=previous, R3=current.
        cmp r1,#0
        beq aia_yes
        cmp r0,#0
        beq aia_no
        ldr r2,[r0],#4
        subs r1,#1
aia_loop
        cmp r1,#0
        beq aia_yes
        ldr r3,[r0],#4
        cmp r3,r2
        blt aia_no
        mov r2,r3
        subs r1,#1
        b aia_loop
aia_yes
        movs r0,#1
        bx lr
aia_no
        movs r0,#0
        bx lr

        ALIGN
        END
