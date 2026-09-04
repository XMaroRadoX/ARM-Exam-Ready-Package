; Rectangular matrix transpose
; int matrix_transpose(const int *in, size_t rows, size_t cols, int *out)
; Transpose a row-major signed-word matrix into disjoint output with rows*cols words. Zero dimensions succeed. Reject null nonempty inputs, exact aliasing, and products exceeding the 32-bit word-address range.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT matrix_transpose
matrix_transpose
        cmp r1,#0
        beq tx_yes
        cmp r2,#0
        beq tx_yes
        cmp r0,#0
        beq tx_bad
        cmp r3,#0
        beq tx_bad
        cmp r0,r3
        beq tx_bad
        push {r4-r8,lr}
        umull r4,r5,r1,r2
        cmp r5,#0
        bne tx_fail
        lsr r5,r4,#30
        cmp r5,#0
        bne tx_fail
        movs r4,#0
tx_row
        cmp r4,r1
        bhs tx_done
        movs r5,#0
tx_col
        cmp r5,r2
        bhs tx_next
        mla r6,r4,r2,r5
        mla r7,r5,r1,r4
        ldr r8,[r0,r6,lsl #2]
        str r8,[r3,r7,lsl #2]
        adds r5,#1
        b tx_col
tx_next
        adds r4,#1
        b tx_row
tx_done
        pop {r4-r8,lr}
tx_yes
        movs r0,#1
        bx lr
tx_fail
        pop {r4-r8,lr}
tx_bad
        movs r0,#0
        bx lr

        ALIGN
        END
