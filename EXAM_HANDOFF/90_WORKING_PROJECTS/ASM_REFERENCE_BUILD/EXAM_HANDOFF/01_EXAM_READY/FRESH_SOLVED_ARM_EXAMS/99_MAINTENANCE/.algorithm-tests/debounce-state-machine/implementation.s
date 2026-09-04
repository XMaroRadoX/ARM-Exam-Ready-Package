; Debounce state machine
; typedef struct{uint8_t stable,candidate;uint16_t ticks;}Debounce;
; int debounce_update(Debounce *s, uint8_t sample, uint16_t required, uint8_t *changed)
; Caller initializes stable/candidate/ticks. Require required>=1; samples are byte states. Return 1 for a valid update and set changed only when required consecutive samples confirm a new state.
        AREA |.text.exam|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT debounce_update
debounce_update
        cmp r0,#0
        beq db_bad
        cmp r3,#0
        beq db_bad
        uxth r2,r2
        cmp r2,#0
        beq db_bad
        push {r4,r5}
        uxtb r1,r1
        movs r4,#0
        strb r4,[r3]
        ldrb r4,[r0,#1]
        cmp r4,r1
        beq db_same
        strb r1,[r0,#1]
        movs r4,#1
        strh r4,[r0,#2]
        b db_check
db_same
        ldrh r4,[r0,#2]
        cmp r4,r2
        bhs db_check
        adds r4,#1
        strh r4,[r0,#2]
db_check
        cmp r4,r2
        bne db_done
        ldrb r5,[r0]
        cmp r5,r1
        beq db_done
        strb r1,[r0]
        movs r4,#1
        strb r4,[r3]
db_done
        movs r0,#1
        pop {r4,r5}
        bx lr
db_bad
        movs r0,#0
        bx lr

        ALIGN
        END
