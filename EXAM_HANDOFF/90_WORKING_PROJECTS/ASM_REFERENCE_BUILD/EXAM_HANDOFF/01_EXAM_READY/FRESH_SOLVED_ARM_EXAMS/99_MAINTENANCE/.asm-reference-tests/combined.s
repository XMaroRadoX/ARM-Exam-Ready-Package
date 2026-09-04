.syntax unified
.cpu cortex-m3
.thumb
.text

.global plus_one
.thumb_func
plus_one:
        ADDS R0, R0, #1
        BX LR

.syntax unified
.cpu cortex-m3
.thumb
.global fifth
.thumb_func
fifth:
        PUSH {R4,LR}
        LDR R0, [SP, #8]
        POP {R4,PC}

.syntax unified
.cpu cortex-m3
.thumb
.global sum_words
.thumb_func
sum_words:
        MOVS R2, #0
        CBZ R1, sum_done
sum_loop:
        LDR R3, [R0], #4
        ADD R2, R2, R3
        SUBS R1, R1, #1
        BNE sum_loop
sum_done:
        MOV R0, R2
        BX LR

.syntax unified
.cpu cortex-m3
.thumb
.global max_signed
.thumb_func
max_signed:
        CMP R0, R1
        BGE max_done
        MOV R0, R1
max_done:
        BX LR

.text
.global carry_case
.thumb_func
carry_case:
.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =0xFFFFFFFF
        ADDS R0, R1, #1
        MRS R0, APSR

 BX LR

.text
.global borrow_case
.thumb_func
borrow_case:
.syntax unified
.cpu cortex-m3
.thumb
        MOVS R1, #0
        SUBS R0, R1, #1
        MRS R0, APSR

 BX LR

.text
.global wide_case
.thumb_func
wide_case:
.syntax unified
.cpu cortex-m3
.thumb
        LDR R0, =0xFFFFFFFF
        MOVS R1, #0
        MOVS R2, #1
        MOVS R3, #0
        ADDS R0, R0, R2
        ADC R1, R1, R3
        MOV R0, R1

 BX LR

.text
.global signed_load_case
.thumb_func
signed_load_case:
.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =byte_data
        LDRB R0, [R1]
        LDRSB R2, [R1]
        B after_byte
byte_data:
.byte 0xFE
.balign 2
after_byte:
        MOV R0, R2

 BX LR

.text
.global overflow_case
.thumb_func
overflow_case:
.syntax unified
.cpu cortex-m3
.thumb
        LDR R0, =0x7FFFFFFF
        ADDS R0, R0, #1
        BVS matched
        MOVS R2, #0
        B finished
matched:
        MOVS R2, #1
finished:
        MOV R0, R2

 BX LR

.text
.global shift_case
.thumb_func
shift_case:
.syntax unified
.cpu cortex-m3
.thumb
        LDR R1, =0xFFFFFFFC
        LSR R0, R1, #1
        ASR R2, R1, #1
        MOV R0, R2

 BX LR

.text
.global remainder_case
.thumb_func
remainder_case:
.syntax unified
.cpu cortex-m3
.thumb
        UDIV R2, R0, R1
        MLS R0, R2, R1, R0

 BX LR

.text
.global nested
.thumb_func
nested:
.syntax unified
.cpu cortex-m3
.thumb
        PUSH {R4,LR}
        BL helper
        POP {R4,PC}
.global helper
.thumb_func
helper:
        ADDS R0, R0, #1
        BX LR
