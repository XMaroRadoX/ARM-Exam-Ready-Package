#include "LPC17xx.h"
#include "exam_api.h"
#include <stdint.h>

extern uint32_t bitwiseAffineTransformation(const uint8_t *matrix,
                                          uint32_t b, uint32_t c);

static const uint8_t transformationMatrix[8] = {
    0x8F, 0xC7, 0xE3, 0xF1, 0xF8, 0x7C, 0x3E, 0x1F
};

static volatile uint32_t timer1_sample = 0u;
static volatile uint8_t displayed_value = 0u;
static volatile uint8_t blinking = 0u;
static volatile uint8_t leds_on = 0u;

static void require_ok(exam_status_t status)
{
    if (status != EXAM_OK) {
        __disable_irq();
        for (;;) { /* Configuration failure: inspect status in debugger. */ }
    }
}

/* Called before changing the displayed value or restarting a blink. */
static void stop_blink(void)
{
    exam_timer_stop(EXAM_TIMER0);
    blinking = 0u;
    (void)exam_timer_ack(EXAM_TIMER0);
    NVIC_ClearPendingIRQ(TIMER0_IRQn);
}

int main(void)
{
    exam_init();
    __disable_irq();
    exam_led_clear();

    require_ok(exam_debounce_config(10u, 30u));
    exam_buttons_init();
    NVIC_DisableIRQ(EINT2_IRQn);  /* KEY2 is unused. */

    require_ok(exam_timer_config_ticks(EXAM_TIMER1, 0xFFFFu,
                                      EXAM_TIMER_MODULO_NO_IRQ));
    NVIC_DisableIRQ(TIMER1_IRQn);

    require_ok(exam_timer_config_ms(EXAM_TIMER0, 250u,
                                   EXAM_TIMER_PERIODIC));
    require_ok(exam_rit_config_ms(10u));

    /* Equal priorities prevent these handlers from interrupting each other. */
    NVIC_SetPriority(EINT0_IRQn, 2u);
    NVIC_SetPriority(EINT1_IRQn, 2u);
    NVIC_SetPriority(RIT_IRQn, 2u);
    NVIC_SetPriority(TIMER0_IRQn, 2u);

    exam_timer_start(EXAM_TIMER1);
    exam_rit_start();
    __enable_irq();

    for (;;) {
        __WFI();
    }
}

void EINT0_IRQHandler(void)
{
    /* Sample at the button edge; use the sample after press confirmation. */
    timer1_sample = exam_timer_read(EXAM_TIMER1) & 0xFFFFu;
    (void)exam_debounce_begin(EXAM_BUTTON_INT0);
}

void EINT1_IRQHandler(void)
{
    (void)exam_debounce_begin(EXAM_BUTTON_KEY1);
}

void RIT_IRQHandler(void)
{
    uint32_t events;
    uint32_t low_byte;
    uint32_t high_byte;

    exam_rit_ack();
    exam_debounce_tick();
    events = exam_button_events_take();

    if ((events & EXAM_BUTTON_EVENT_INT0) != 0u) {
        stop_blink();
        low_byte = timer1_sample & 0xFFu;
        high_byte = (timer1_sample >> 8) & 0xFFu;
        displayed_value = (uint8_t)(low_byte ^ high_byte);
        leds_on = 1u;
        exam_led_write(displayed_value);
    }

    if ((events & EXAM_BUTTON_EVENT_KEY1) != 0u) {
        stop_blink();
        displayed_value = (uint8_t)bitwiseAffineTransformation(
            transformationMatrix, displayed_value, 0x63u);

        leds_on = 1u;
        exam_led_write(displayed_value);
        exam_timer_reset(EXAM_TIMER0);
        blinking = 1u;
        exam_timer_start(EXAM_TIMER0);
    }
}

void TIMER0_IRQHandler(void)
{
    uint32_t flags = exam_timer_ack(EXAM_TIMER0);

    if (((flags & 1u) != 0u) && (blinking != 0u)) {
        leds_on ^= 1u;
        exam_led_write(leds_on ? displayed_value : 0u);
    }
}
