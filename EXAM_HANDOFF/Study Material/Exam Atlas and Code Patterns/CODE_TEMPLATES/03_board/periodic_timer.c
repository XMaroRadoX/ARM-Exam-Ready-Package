/* Recommended exam template: periodic timer signals foreground work. */
#include "exam_api.h"

enum { PERIODIC_EVENT = 1u << 8 };

static void periodic_callback(uint8_t timer, uint32_t flags) {
    if (timer == 0u && exam_timer_match_happened(flags, 0u)) {
        exam_events_set(PERIODIC_EVENT);
    }
}

exam_status_t periodic_example_init(void) {
    return exam_timer_every_ms(0, 500, periodic_callback);
}

void periodic_example_loop(void) {
    if ((exam_events_take(PERIODIC_EVENT) & PERIODIC_EVENT) != 0u) {
        (void)exam_led_toggle(4u);
    }
}
