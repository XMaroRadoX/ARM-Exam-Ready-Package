; Cocktail shaker sort
; void cocktail_sort(int *a, size_t n)
; Stable ascending adjacent-swap sort. Null input is a no-op; arrays of length below two are unchanged.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT cocktail_sort
cocktail_sort
        cmp r0,#0
        beq ck_done
        cmp r1,#2
        blo ck_done
        push {r4-r10,lr}
        movs r4,#0
        mov r5,r1
ck_outer
        add r6,r4,#1
        cmp r5,r6
        bls ck_pop
        movs r7,#0
        add r6,r4,#1
ck_forward
        cmp r6,r5
        bhs ck_reverse
        sub r10,r6,#1
        ldr r8,[r0,r10,lsl #2]
        ldr r9,[r0,r6,lsl #2]
        cmp r8,r9
        ble ck_fn
        str r9,[r0,r10,lsl #2]
        str r8,[r0,r6,lsl #2]
        movs r7,#1
ck_fn
        adds r6,#1
        b ck_forward
ck_reverse
        cmp r7,#0
        beq ck_pop
        subs r5,#1
        movs r7,#0
        sub r6,r5,#1
ck_backward
        cmp r6,r4
        bls ck_end
        sub r10,r6,#1
        ldr r8,[r0,r10,lsl #2]
        ldr r9,[r0,r6,lsl #2]
        cmp r8,r9
        ble ck_bn
        str r9,[r0,r10,lsl #2]
        str r8,[r0,r6,lsl #2]
        movs r7,#1
ck_bn
        subs r6,#1
        b ck_backward
ck_end
        adds r4,#1
        cmp r7,#0
        bne ck_outer
ck_pop
        pop {r4-r10,lr}
ck_done
        bx lr

        ALIGN
        END
