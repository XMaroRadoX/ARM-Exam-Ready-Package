.syntax unified
.cpu cortex-m3
.thumb
.text
.global array_monotonic_direction
array_monotonic_direction:
        cmp r1,#0
        beq amd_constant
        cmp r0,#0
        beq amd_none
        cmp r1,#1
        beq amd_constant
        push {r4,lr}
        ldr r2,[r0],#4
        movs r3,#0
        movs r12,#0
        subs r1,#1
amd_loop:
        ldr r4,[r0],#4
        cmp r4,r2
        bgt amd_mark_up
        blt amd_mark_down
        b amd_check
amd_mark_up:
        movs r3,#1
        b amd_check
amd_mark_down:
        movs r12,#1
amd_check:
        cmp r3,#0
        beq amd_next
        cmp r12,#0
        bne amd_pop_none
amd_next:
        mov r2,r4
        subs r1,#1
        bne amd_loop
        cmp r3,#0
        bne amd_up
        cmp r12,#0
        bne amd_down
        pop {r4,lr}
amd_constant:
        movs r0,#0
        bx lr
amd_up:
        movs r0,#1
        pop {r4,pc}
amd_down:
        mvn r0,#0
        pop {r4,pc}
amd_pop_none:
        pop {r4,lr}
amd_none:
        movs r0,#2
        bx lr
.balign 4
