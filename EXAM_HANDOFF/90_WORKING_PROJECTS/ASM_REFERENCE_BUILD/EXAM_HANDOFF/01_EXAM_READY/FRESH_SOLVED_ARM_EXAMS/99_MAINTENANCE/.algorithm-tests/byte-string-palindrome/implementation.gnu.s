.syntax unified
.cpu cortex-m3
.thumb
.text
.global bytes_palindrome
bytes_palindrome:
        cmp r1,#0
        beq sp_yes
        cmp r0,#0
        beq sp_no
        push {r4,r5}
        movs r2,#0
        subs r1,#1
sp_loop:
        cmp r2,r1
        bhs sp_ok
        ldrb r3,[r0,r2]
        ldrb r4,[r0,r1]
        cmp r3,r4
        bne sp_fail
        adds r2,#1
        subs r1,#1
        b sp_loop
sp_ok:
        pop {r4,r5}
sp_yes:
        movs r0,#1
        bx lr
sp_fail:
        pop {r4,r5}
sp_no:
        movs r0,#0
        bx lr
.balign 4
