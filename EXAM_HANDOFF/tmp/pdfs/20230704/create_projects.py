from pathlib import Path
import shutil

ROOT = Path.cwd()
OUT = ROOT / '90_WORKING_PROJECTS/20230704_Sociable_Complete'
TEMPLATE = ROOT / '01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API'
assert not OUT.exists(), 'Do not overwrite an existing solution'
OUT.mkdir(parents=True)
asm = '''                AREA    |.text|, CODE, READONLY
                PRESERVE8
                THUMB
                EXPORT  isSociable
                EXPORT  aliquotSum

; uint32_t isSociable(uint32_t n)
; R0: input n, then return value (0 or a cycle length from 1 to 8).
isSociable      PROC
                PUSH    {R4-R6, LR}     ; 16 bytes; keep SP 8-byte aligned.
                CMP     R0, #2          ; 0 and 1 are not sociable.
                BLO     not_found
                MOV     R4, R0          ; Preserve original n across BL.
                MOV     R5, R0          ; Current sequence value.
                MOVS    R6, #0          ; Computed sums, excluding input.

sequence_loop
                MOV     R0, R5          ; Argument for aliquotSum.
                BL      aliquotSum     ; R0 becomes s(current).
                ADDS    R6, R6, #1      ; Exactly one new term computed.
                CMP     R0, R4
                BEQ     found          ; Success even on the eighth term.
                CMP     R0, #1
                BLS     not_found      ; 1 per paper; also safely handles 0.
                CMP     R6, #8
                BEQ     not_found      ; No return to n within 8 terms.
                MOV     R5, R0          ; Next input is the latest sum.
                B       sequence_loop

found
                MOV     R0, R6          ; Return cycle length.
                POP     {R4-R6, PC}
not_found
                MOVS    R0, #0
                POP     {R4-R6, PC}
                ENDP

; uint32_t aliquotSum(uint32_t n)
; Implements the paper's divisor-pair algorithm literally for n >= 2.
; R0=n, R1=sum, R2=a, R3=b, R12=remainder. No nested calls.
; Exam inputs and intermediate sums are assumed to fit uint32_t.
aliquotSum      PROC
                CMP     R0, #2
                BLO     small_number
                MOVS    R1, #1          ; Include divisor 1, exclude n.
                MOVS    R2, #2          ; First candidate divisor.
divisor_loop
                UDIV    R3, R0, R2      ; b = floor(n / a).
                MLS     R12, R3, R2, R0 ; remainder = n - b*a.
                CMP     R12, #0
                BNE     next_divisor   ; Not divisible: try a+1.
                CMP     R2, R3
                BLO     add_pair       ; a < b: add two distinct divisors.
                BEQ     add_square     ; a == b: count sqrt(n) once.
                B       sum_done       ; a > b: pair already counted.
add_pair
                ADDS    R1, R1, R2
                ADDS    R1, R1, R3
                B       next_divisor
add_square
                ADDS    R1, R1, R2
sum_done
                MOV     R0, R1
                BX      LR
next_divisor
                ADDS    R2, R2, #1
                B       divisor_loop
small_number
                MOVS    R0, #0
                BX      LR
                ENDP
                ALIGN
                END
'''
q1 = '''#include "LPC17xx.h"
#include "exam_api.h"

extern uint32_t isSociable(uint32_t n);

/* Inspect results and tests_passed in the debugger after tests_done = 1. */
const uint32_t inputs[4] = {28u, 220u, 12496u, 100u};
const uint32_t expected[4] = {1u, 2u, 5u, 0u};
volatile uint32_t results[4];
volatile uint32_t tests_passed = 0u;
volatile uint32_t tests_done = 0u;

int main(void)
{
    uint32_t i;
    exam_init();
    for (i = 0u; i < 4u; ++i) {
        results[i] = isSociable(inputs[i]);
        if (results[i] == expected[i]) {
            ++tests_passed;
        }
    }
    tests_done = 1u;
    while (1) {
        __WFI();
    }
}
'''
q2 = '''#include "LPC17xx.h"
#include "exam_api.h"

/* Timer 1's handler and the array are in Source/timer/IRQ_timer.c. */
int main(void)
{
    exam_init();
    exam_led_clear();
    if (exam_timer_config_ms(EXAM_TIMER1, 2000u,
                             EXAM_TIMER_PERIODIC) != EXAM_OK) {
        while (1) { __WFI(); }
    }
    exam_timer_start(EXAM_TIMER1);
    while (1) {
        __WFI();
    }
}
'''
irq = '''#include "LPC17xx.h"
#include "exam_api.h"

extern uint32_t isSociable(uint32_t n);

const uint32_t numbers[7] = {
    8128u, 5564u, 5400u, 14264u, 1305184u, 1598470u, 4938136u
};
static uint32_t next_index = 0u;

/* Optional debugger observations; they do not control the algorithm. */
volatile uint32_t last_input = 0u;
volatile uint32_t last_result = 0u;
volatile uint32_t interrupt_count = 0u;

void TIMER1_IRQHandler(void)
{
    uint32_t pending = exam_timer_ack(EXAM_TIMER1);
    uint32_t length;

    if ((pending & 1u) == 0u) {
        return;                         /* Only MR0 advances the array. */
    }
    last_input = numbers[next_index];
    length = isSociable(last_input);
    last_result = length;
    ++interrupt_count;

    if ((length >= 1u) && (length <= 8u)) {
        /* Physical board label: 1 -> LD4, 2 -> LD5, ..., 8 -> LD11. */
        (void)exam_led_one_hot((uint8_t)(length + 3u));
    } else {
        exam_led_clear();
    }

    ++next_index;
    if (next_index == 7u) {
        next_index = 0u;
    }
}

/* The template owns one handler per timer. Unused timers stay stopped. */
void TIMER0_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER0); }
void TIMER2_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER2); }
void TIMER3_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER3); }
'''
for name, main in [('Q1_Assembly', q1), ('Q2_Timer_LEDs', q2)]:
    target = OUT / name
    shutil.copytree(TEMPLATE, target, ignore=shutil.ignore_patterns(
        'Objects', 'Listings', '*.uvguix.*', '*.bak'))
    (target/'Objects').mkdir()
    (target/'Listings').mkdir()
    (target/'Source/sample.c').write_text(main, encoding='ascii')
    (target/'Source/ASM_funct.s').write_text(asm, encoding='ascii')
    if name.startswith('Q2'):
        (target/'Source/timer/IRQ_timer.c').write_text(irq, encoding='ascii')
(OUT/'validation').mkdir()
print(OUT)
