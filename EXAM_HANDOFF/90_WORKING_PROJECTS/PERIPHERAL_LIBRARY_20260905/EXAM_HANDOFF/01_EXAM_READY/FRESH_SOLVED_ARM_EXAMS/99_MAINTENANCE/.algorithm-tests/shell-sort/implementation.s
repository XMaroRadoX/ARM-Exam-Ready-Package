; Shell sort
; void shell_sort(int *a, size_t n)
; Ascending signed-word sort using halved gaps. In place and not guaranteed stable; null input is a no-op.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT shell_sort
shell_sort
        cmp r0,#0
        beq sh_done
        push {r4-r8,lr}
        lsrs r4,r1,#1
sh_gap
        cmp r4,#0
        beq sh_pop
        mov r5,r4
sh_outer
        cmp r5,r1
        bhs sh_half
        ldr r6,[r0,r5,lsl #2]
        mov r7,r5
sh_inner
        cmp r7,r4
        blo sh_store
        sub r3,r7,r4
        ldr r8,[r0,r3,lsl #2]
        cmp r8,r6
        ble sh_store
        str r8,[r0,r7,lsl #2]
        mov r7,r3
        b sh_inner
sh_store
        str r6,[r0,r7,lsl #2]
        adds r5,#1
        b sh_outer
sh_half
        lsrs r4,#1
        b sh_gap
sh_pop
        pop {r4-r8,lr}
sh_done
        bx lr

        ALIGN
        END
