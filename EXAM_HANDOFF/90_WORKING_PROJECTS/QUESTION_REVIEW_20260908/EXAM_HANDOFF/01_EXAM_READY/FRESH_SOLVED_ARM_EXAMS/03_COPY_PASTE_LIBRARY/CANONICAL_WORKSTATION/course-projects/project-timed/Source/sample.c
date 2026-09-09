#include "exam_api.h"
static void stop_on_error(void) { exam_led_write(0xFFu); for (;;) {} }

extern uint32_t sum_words(const uint32_t *values,uint32_t count);
static const uint32_t values[4]={1u,2u,3u,4u};
int main(void)
{
    exam_init();
    if (exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC)!=EXAM_OK)
        stop_on_error();
    exam_timer_start(EXAM_TIMER0);
    for (;;) {
        if (exam_events_take(1u) & 1u) {
            uint32_t result=sum_words(values,4u);
            exam_led_write((uint8_t)result);
        }
    }
}
