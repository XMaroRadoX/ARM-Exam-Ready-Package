/* Recommended exam template: confirmed button press to foreground event. */
#include "exam_api.h"

exam_status_t confirmed_button_init(void) {
    exam_status_t status;
    exam_buttons_init();
    status = exam_debounce_config(10u, 50u);
    if (status != EXAM_OK) return status;
    return exam_debounce_begin(EXAM_BUTTON_INT0);
}

void confirmed_button_loop(void) {
    /* Call every 10 ms, matching exam_debounce_config(). */
    exam_debounce_tick();
    if ((exam_button_events_take() & EXAM_BUTTON_EVENT_INT0) != 0u) {
        (void)exam_led_toggle(11u);
    }
}
