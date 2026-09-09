.syntax unified
.cpu cortex-m3
.thumb
.text
.global scale_i32_between_ranges
scale_i32_between_ranges:
        ldr r12,[sp,#4]
        cmp r12,#0
        beq sir_bad
        push {r4-r10,lr}
        mov r4,r0
        mov r5,r1
        mov r6,r2
        mov r7,r3
        ldr r8,[sp,#32]
        ldr r9,[sp,#36]
        subs r10,r6,r5
        bvs sir_fail
        cmp r10,#0
        ble sir_fail
        subs r6,r8,r7
        bvs sir_fail
        cmp r4,r5
        bge sir_high
        mov r4,r5
sir_high:
        cmp r4,r2
        ble sir_product
        mov r4,r2
sir_product:
        sub r4,r4,r5
        smull r0,r1,r4,r6
        mov r2,r10
        movs r3,#0
        bl __aeabi_ldivmod
        adds r0,r0,r7
        bvs sir_fail
        str r0,[r9]
        movs r0,#1
        pop {r4-r10,pc}
sir_fail:
        movs r0,#0
        pop {r4-r10,pc}
sir_bad:
        movs r0,#0
        bx lr
.extern __aeabi_ldivmod
.balign 4
