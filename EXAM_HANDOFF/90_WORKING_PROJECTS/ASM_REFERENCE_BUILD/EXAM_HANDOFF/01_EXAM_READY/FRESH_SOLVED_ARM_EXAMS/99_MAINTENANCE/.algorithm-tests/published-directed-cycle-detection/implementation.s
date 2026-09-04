; Directed cycle detection
; int directed_cycle(const uint8_t *a, size_t n, uint8_t *state)
; Directed byte adjacency matrix, n<=256, and n state bytes. Return 1 for a cycle, 0 otherwise or for invalid input. Initialize states internally. Recursion uses at most n helper frames.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT directed_cycle
directed_cycle
        cmp r0,#0
        beq cy_bad
        cmp r2,#0
        beq cy_bad
        cmp r1,#256
        bhi cy_bad
        push {r4-r8,lr}
        mov r4,r0
        mov r5,r1
        mov r6,r2
        movs r7,#0
        movs r8,#0
cy_init
        cmp r7,r5
        bhs cy_start
        strb r8,[r6,r7]
        adds r7,#1
        b cy_init
cy_start
        movs r7,#0
cy_outer
        cmp r7,r5
        bhs cy_no
        ldrb r0,[r6,r7]
        cmp r0,#0
        bne cy_next
        mov r0,r4
        mov r1,r5
        mov r2,r7
        mov r3,r6
        bl cy_visit
        cmp r0,#0
        bne cy_return
cy_next
        adds r7,#1
        b cy_outer
cy_no
        movs r0,#0
cy_return
        pop {r4-r8,pc}
cy_bad
        movs r0,#0
        bx lr
cy_visit
        push {r4-r8,lr}
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        movs r0,#1
        strb r0,[r7,r6]
        movs r8,#0
cy_vloop
        cmp r8,r5
        bhs cy_black
        mla r0,r6,r5,r8
        ldrb r0,[r4,r0]
        cmp r0,#0
        beq cy_vnext
        ldrb r0,[r7,r8]
        cmp r0,#1
        beq cy_found
        cmp r0,#0
        bne cy_vnext
        mov r0,r4
        mov r1,r5
        mov r2,r8
        mov r3,r7
        bl cy_visit
        cmp r0,#0
        bne cy_vreturn
cy_vnext
        adds r8,#1
        b cy_vloop
cy_black
        movs r0,#2
        strb r0,[r7,r6]
        movs r0,#0
        b cy_vreturn
cy_found
        movs r0,#1
cy_vreturn
        pop {r4-r8,pc}
        ALIGN
        END
