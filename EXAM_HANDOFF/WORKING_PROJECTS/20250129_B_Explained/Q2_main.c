#include <stdint.h>
#include "LPC17xx.h"
#include "exam_api.h"

extern void transpose(const uint8_t *source, uint8_t *destination);

/* No explicit initializers: fill the inputs before checking the identity. */
static uint8_t A[8], B[8];
static uint8_t A_xor_B[8];
static uint8_t AT[8], BT[8], xor_T[8];
static uint32_t count_A = 0u;
static uint32_t count_B = 0u;

/* Captured at the initial button interrupt, accepted after debouncing. */
static volatile uint8_t key1_sample;
static volatile uint8_t key2_sample;

void EINT0_IRQHandler(void)
{
    (void)exam_debounce_begin(EXAM_BUTTON_INT0);
}

void EINT1_IRQHandler(void)
{
    key1_sample = (uint8_t)exam_timer_read(EXAM_TIMER2);
    (void)exam_debounce_begin(EXAM_BUTTON_KEY1);
}

void EINT2_IRQHandler(void)
{
    key2_sample = (uint8_t)exam_timer_read(EXAM_TIMER2);
    (void)exam_debounce_begin(EXAM_BUTTON_KEY2);
}

void SysTick_Handler(void)
{
    exam_debounce_tick();
}

static void check_equivalence(void)
{
    uint32_t i;
    uint32_t equal = 1u;

    for (i = 0u; i < 8u; ++i) {
        A_xor_B[i] = (uint8_t)(A[i] ^ B[i]);
    }

    /* Exactly three calls, as required by the question. */
    transpose(A_xor_B, xor_T);
    transpose(A, AT);
    transpose(B, BT);

    for (i = 0u; i < 8u; ++i) {
        if (xor_T[i] != (uint8_t)(AT[i] ^ BT[i])) {
            equal = 0u;
        }
    }

    exam_led_clear();
    if (equal != 0u) {
        (void)exam_led_on(4u);
    } else {
        (void)exam_led_on(5u);
    }
}

int main(void)
{
    uint32_t events;
    uint32_t saved_primask;
    uint8_t sample_A;
    uint8_t sample_B;

    exam_init();
    exam_buttons_init();

    if (exam_timer_config_ticks(EXAM_TIMER2, 0xFFFFu,
                               EXAM_TIMER_MODULO_NO_IRQ) != EXAM_OK) {
        for (;;) { /* Configuration failure: inspect in debugger. */ }
    }
    exam_timer_start(EXAM_TIMER2);

    /* SysTick is only for button debounce, separate from TIMER2. */
    if (exam_debounce_config(10u, 30u) != EXAM_OK) {
        for (;;) { }
    }
    if (exam_systick_config_ms(10u) != EXAM_OK) {
        for (;;) { }
    }

    for (;;) {
        /* Snapshot events and captured samples without IRQ interference. */
        saved_primask = exam_critical_enter();
        events = exam_button_events_take();
        sample_A = key1_sample;
        sample_B = key2_sample;
        exam_critical_exit(saved_primask);

        if (((events & EXAM_BUTTON_EVENT_KEY1) != 0u) &&
            (count_A < 8u)) {
            A[count_A] = sample_A;
            ++count_A;
        }

        if (((events & EXAM_BUTTON_EVENT_KEY2) != 0u) &&
            (count_B < 8u)) {
            B[count_B] = sample_B;
            ++count_B;
        }

        if (((events & EXAM_BUTTON_EVENT_INT0) != 0u) &&
            (count_A == 8u) && (count_B == 8u)) {
            check_equivalence();
        }

        __WFI();
    }
}
