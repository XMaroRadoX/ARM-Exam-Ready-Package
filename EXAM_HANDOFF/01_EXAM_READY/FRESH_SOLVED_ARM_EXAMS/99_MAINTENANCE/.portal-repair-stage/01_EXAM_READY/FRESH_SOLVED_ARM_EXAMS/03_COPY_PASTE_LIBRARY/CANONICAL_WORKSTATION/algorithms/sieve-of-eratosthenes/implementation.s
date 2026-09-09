; Sieve of Eratosthenes
; int prime_sieve(uint8_t *flags, uint32_t limit, uint32_t capacity)
; Fill flags[0..limit]: 1 for prime, 0 otherwise. Accept limit<=65535 and capacity>limit. Invalid input returns 0 before writes.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT prime_sieve
prime_sieve
        cmp r0,#0
        beq ps_bad
        ldr r3,=65535
        cmp r1,r3
        bhi ps_bad
        cmp r2,r1
        bls ps_bad
        push {r4-r6,lr}
        movs r2,#0
ps_init
        movs r3,#0
        cmp r2,#2
        blo ps_write
        movs r3,#1
ps_write
        strb r3,[r0,r2]
        adds r2,#1
        cmp r2,r1
        bls ps_init
        movs r2,#2
ps_outer
        udiv r3,r1,r2
        cmp r2,r3
        bhi ps_done
        ldrb r3,[r0,r2]
        cmp r3,#0
        beq ps_next
        mul r4,r2,r2
        movs r5,#0
ps_inner
        cmp r4,r1
        bhi ps_next
        strb r5,[r0,r4]
        add r4,r2
        b ps_inner
ps_next
        adds r2,#1
        b ps_outer
ps_done
        movs r0,#1
        pop {r4-r6,pc}
ps_bad
        movs r0,#0
        bx lr

        ALIGN
        END
