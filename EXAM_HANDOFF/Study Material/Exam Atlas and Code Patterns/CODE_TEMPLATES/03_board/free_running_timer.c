/* Recommended exam template: free-running timer with reset but no IRQ. */
#include "exam_api.h"

exam_status_t free_running_timer_init(void) {
    exam_status_t status;

    status = exam_timer_prescaler(1u, 0u);
    if (status != EXAM_OK) return status;

    /* RESET is selected without EXAM_TIMER_INTERRUPT. */
    status = exam_timer_match(1u, 0u, 0xFFFFu, EXAM_TIMER_RESET);
    if (status != EXAM_OK) return status;

    status = exam_timer_reset(1u);
    if (status != EXAM_OK) return status;
    return exam_timer_start(1u);
}

uint32_t free_running_timer_sample(void) {
    return exam_timer_count(1u);
}
