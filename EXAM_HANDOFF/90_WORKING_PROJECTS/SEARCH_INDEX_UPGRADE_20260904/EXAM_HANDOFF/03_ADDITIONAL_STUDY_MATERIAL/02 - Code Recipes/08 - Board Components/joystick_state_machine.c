/* Recommended exam template: debounced joystick foreground state machine. */
#include "exam_api.h"

typedef enum { WAIT_START, EDIT_VALUE, SHOW_VALUE, FINISHED } game_state_t;

static uint32_t previous_joystick;
static game_state_t game_state;
static uint8_t value;

exam_status_t joystick_state_init(void) {
    game_state = WAIT_START;
    value = 0u;
    exam_joystick_init();
    previous_joystick = exam_joystick_read();
    return EXAM_OK;
}

void joystick_state_loop(void) {
    uint32_t current;
    uint32_t edges;
    current = exam_joystick_read();
    edges = exam_joystick_pressed_edges(previous_joystick, current);
    previous_joystick = current;

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
    exam_led_write(value);
}
