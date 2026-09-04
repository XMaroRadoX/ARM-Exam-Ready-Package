#include "exam_api.h"
static void stop_on_error(void) { exam_led_write(0xFFu); for (;;) {} }

int main(void)
{
    uint8_t count=0u;
    exam_init();
    exam_buttons_init();
    if (exam_debounce_config(10u,50u)!=EXAM_OK) stop_on_error();
    if (exam_rit_config_ms(10u)!=EXAM_OK) stop_on_error();
    exam_rit_start();
    for (;;) {
        uint32_t pressed=exam_button_events_take();
        if (pressed & EXAM_BUTTON_EVENT_INT0) {
            count=(uint8_t)(count+1u);
            exam_led_write(count);
        }
    }
}
