/* Recommended exam template: free-running timer with reset but no IRQ. */
#include "exam_api.h"

exam_status_t free_running_timer_init(void) {
    exam_status_t status;

    status = timer_set_prescaler(1u, 0u);
    if (status != EXAM_OK) return status;

    /* RESET is selected without TIMER_ACTION_INTERRUPT. */
    status = timer_configure_match(1u, 0u, 0xFFFFu, TIMER_ACTION_RESET);
    if (status != EXAM_OK) return status;

    status = timer_reset(1u);
    if (status != EXAM_OK) return status;
    return timer_start(1u);
}

uint32_t free_running_timer_sample(void) {
    return timer_read_counter(1u);
}
