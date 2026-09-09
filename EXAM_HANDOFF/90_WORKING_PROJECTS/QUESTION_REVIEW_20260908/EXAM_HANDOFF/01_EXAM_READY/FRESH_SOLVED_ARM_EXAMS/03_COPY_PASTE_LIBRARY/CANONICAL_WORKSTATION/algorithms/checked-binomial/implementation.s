; Bounded checked binomial coefficient
; int binomial_coefficient(uint32_t n, uint32_t k, uint32_t *out)
; Accept 0<=k<=n<=30. Return 1 and C(n,k), or 0 without writing. This bound keeps intermediate multiplication within 32 bits.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT binomial_coefficient
binomial_coefficient
        cmp r2,#0
        beq bn_bad
        cmp r0,#30
        bhi bn_bad
        cmp r1,r0
        bhi bn_bad
        push {r4-r6,lr}
        sub r3,r0,r1
        cmp r1,r3
        bls bn_start
        mov r1,r3
bn_start
        sub r0,r0,r1
        movs r3,#1
        movs r4,#1
bn_loop
        cmp r4,r1
        bhi bn_done
        add r5,r0,r4
        mul r3,r5,r3
        udiv r3,r3,r4
        adds r4,#1
        b bn_loop
bn_done
        str r3,[r2]
        movs r0,#1
        pop {r4-r6,pc}
bn_bad
        movs r0,#0
        bx lr

        ALIGN
        END
