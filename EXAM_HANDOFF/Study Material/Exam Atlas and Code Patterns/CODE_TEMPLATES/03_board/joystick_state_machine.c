/* Recommended exam template: debounced joystick foreground state machine. */
#include "exam_api.h"

enum { JOYSTICK_WORK_EVENT = 1u << 8 };
typedef enum { WAIT_START, EDIT_VALUE, SHOW_VALUE, FINISHED } game_state_t;

static volatile uint32_t joystick_edges;
static game_state_t game_state;
static uint8_t value;

static void state_joystick_callback(uint32_t current, uint32_t changed) {
    joystick_edges |= current & changed; /* Press edges only. */
    exam_events_set(JOYSTICK_WORK_EVENT);
}

exam_status_t joystick_state_init(void) {
    game_state = WAIT_START;
    value = 0u;
    return exam_joystick_start(state_joystick_callback);
}

void joystick_state_loop(void) {
    uint32_t edges;
    uint32_t saved;

    if ((exam_events_take(JOYSTICK_WORK_EVENT) & JOYSTICK_WORK_EVENT) == 0u) return;
    saved = exam_critical_enter();
    edges = joystick_edges;
    joystick_edges = 0u;
    exam_critical_exit(saved);

    if ((edges & EXAM_JOY_SELECT) != 0u) {
        if (game_state == WAIT_START || game_state == SHOW_VALUE) {
            value = 0u;
            game_state = EDIT_VALUE;
        } else if (game_state == EDIT_VALUE) {
            game_state = SHOW_VALUE;
        }
    } else if (game_state == EDIT_VALUE && (edges & EXAM_JOY_UP) != 0u) {
        value = (uint8_t)((value + 1u) & 0x3u);
    }
    (void)exam_led_write(value);
}
