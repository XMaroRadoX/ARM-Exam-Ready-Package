/* Recommended exam template: confirmed button press to foreground event. */
#include "exam_api.h"

enum { BUTTON_WORK_EVENT = 1u << 8 };
static volatile exam_button_t confirmed_button;

static void confirmed_button_callback(exam_button_t button,
                                      exam_button_event_t event) {
    if (event == EXAM_PRESS) {
        confirmed_button = button;
        exam_events_set(BUTTON_WORK_EVENT);
    }
}

exam_status_t confirmed_button_init(void) {
    exam_buttons_confirmation_ms(50u);
    return exam_buttons_start(confirmed_button_callback);
}

void confirmed_button_loop(void) {
    if ((exam_events_take(BUTTON_WORK_EVENT) & BUTTON_WORK_EVENT) != 0u) {
        if (confirmed_button == EXAM_BUTTON_INT0) {
            (void)exam_led_toggle(4u);
        }
    }
}
