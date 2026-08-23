#ifndef EXAM_USER_H
#define EXAM_USER_H

#include "exam_api.h"
#include "exam_compat.h"

enum { EXAM_EVENT_JOYSTICK = 1u << 0 };

void exam_user_init(void);
void exam_user_loop(void);
void exam_button_event(exam_button_t button, exam_button_event_t event);
void exam_joystick_event(uint32_t current, uint32_t changed);
void exam_timer_event(uint8_t timer, uint32_t flags);
void exam_user_10ms_hook(void);

#endif
