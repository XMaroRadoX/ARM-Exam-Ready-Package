#include "LPC17xx.h"
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
