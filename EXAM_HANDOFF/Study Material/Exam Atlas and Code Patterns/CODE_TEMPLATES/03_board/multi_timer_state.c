/* Recommended exam template: three independent timer states. */
#include "exam_api.h"

enum {
    TIMER_A_EVENT = 1u << 8,
    TIMER_B_EVENT = 1u << 9,
    TIMER_C_EVENT = 1u << 10
};

static volatile uint8_t timer_running_mask;

static void three_timer_callback(uint8_t timer, uint32_t flags) {
    if (!exam_timer_match_happened(flags, 0u)) return;
    if (timer == 0u) exam_events_set(TIMER_A_EVENT);
    if (timer == 1u) exam_events_set(TIMER_B_EVENT);
    if (timer == 2u) exam_events_set(TIMER_C_EVENT);
}

exam_status_t three_timer_init(void) {
    exam_status_t status = exam_timer_every_ms(0, 50, three_timer_callback);
    if (status != EXAM_OK) return status;
    timer_running_mask = 1u << 0;
    return EXAM_OK;
}

void three_timer_loop(void) {
    uint32_t events = exam_events_take(TIMER_A_EVENT | TIMER_B_EVENT | TIMER_C_EVENT);

    if ((events & TIMER_A_EVENT) != 0u) {
        if ((timer_running_mask & ((1u << 1) | (1u << 2))) == 0u) {
            /* Start the paper-specific B/C action here. */
        }
    }
    if ((events & TIMER_B_EVENT) != 0u) {
        /* Output the next sample; stop B when the table ends. */
    }
    if ((events & TIMER_C_EVENT) != 0u) {
        /* Stop the note-duration timer and clear its running bit. */
    }
}
