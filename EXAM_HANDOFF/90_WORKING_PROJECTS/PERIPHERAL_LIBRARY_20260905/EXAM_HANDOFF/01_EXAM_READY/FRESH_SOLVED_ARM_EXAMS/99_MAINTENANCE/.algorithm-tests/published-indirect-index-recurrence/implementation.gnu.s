.syntax unified
.cpu cortex-m3
.thumb
.text
.global algorithm_indirect_index_recurrence
algorithm_indirect_index_recurrence:
                CMP     R0, #0
                BEQ     recurrence_invalid
                CMP     R1, #0
                BEQ     recurrence_invalid
                PUSH    {R4-R11}
                MOV     R4, R0
                MOV     R5, R1
                MOVS    R0, #0
                STR     R0, [R4]
                MOVS    R6, #1
recurrence_outer:
                CMP     R6, R5
                BHS     recurrence_done
                SUB     R0, R6, #1
                LDR     R7, [R4, R0, LSL #2]
                MOVS    R11, #1
                ADD     R8, R7, R6
                CMP     R7, R6
                BLO     recurrence_store
                SUB     R9, R7, R6
                MOVS    R10, #0
                MOVS    R11, #0
recurrence_scan:
                CMP     R10, R6
                BHS     recurrence_scan_done
                LDR     R0, [R4, R10, LSL #2]
                CMP     R0, R9
                BNE     recurrence_scan_next
                MOVS    R11, #1
                B       recurrence_scan_done
recurrence_scan_next:
                ADDS    R10, R10, #1
                B       recurrence_scan
recurrence_scan_done:
                CMP     R11, #0
                IT      EQ
                MOVEQ   R8, R9
recurrence_store:
                CMP     R11, #0
                BEQ     recurrence_checked_store
                CMP     R8, R7
                BLO     recurrence_overflow
recurrence_checked_store:
                STR     R8, [R4, R6, LSL #2]
                ADDS    R6, R6, #1
                B       recurrence_outer
recurrence_done:
                MOV     R0, R5
                POP     {R4-R11}
                BX      LR
recurrence_overflow:
                POP     {R4-R11}
recurrence_invalid:
                MOVS    R0, #0
                BX      LR
.ltorg
.balign 4
.global algorithm_indirect_index_recurrence_hofstadter_q
algorithm_indirect_index_recurrence_hofstadter_q:
        cmp r0,#0
        beq hq_bad
        cmp r1,#0
        beq hq_bad
        movs r2,#1
        str r2,[r0]
        cmp r1,#1
        beq hq_single
        str r2,[r0,#4]
        push {r4-r8,lr}
        movs r2,#2
hq_loop:
        cmp r2,r1
        bhs hq_done
        sub r3,r2,#1
        ldr r4,[r0,r3,lsl #2]
        subs r3,#1
        ldr r5,[r0,r3,lsl #2]
        cmp r4,#0
        beq hq_fail
        cmp r5,#0
        beq hq_fail
        cmp r4,r2
        bhi hq_fail
        cmp r5,r2
        bhi hq_fail
        sub r4,r2,r4
        sub r5,r2,r5
        ldr r6,[r0,r4,lsl #2]
        ldr r7,[r0,r5,lsl #2]
        adds r6,r6,r7
        bcs hq_fail
        str r6,[r0,r2,lsl #2]
        adds r2,#1
        b hq_loop
hq_done:
        mov r0,r1
        pop {r4-r8,pc}
hq_fail:
        pop {r4-r8,lr}
hq_bad:
        movs r0,#0
        bx lr
hq_single:
        movs r0,#1
        bx lr
.balign 4
