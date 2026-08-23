#ifndef EXAM_API_H
#define EXAM_API_H

#include "exam_board.h"

/* Main exam API. Time values say ms or Hz in the function name. */
typedef board_status_t exam_status_t;
typedef board_button_t exam_button_t;
typedef button_event_t exam_button_event_t;
typedef adc_sample_t exam_adc_sample_t;
typedef svc_context_t exam_svc_context_t;
typedef fault_snapshot_t exam_fault_snapshot_t;

typedef void (*exam_button_callback_t)(exam_button_t button, exam_button_event_t event);
typedef void (*exam_joystick_callback_t)(uint32_t current, uint32_t changed);
typedef void (*exam_timer_callback_t)(uint8_t timer, uint32_t flags);

#define EXAM_OK        BOARD_OK
#define EXAM_INVALID   BOARD_INVALID
#define EXAM_BUSY      BOARD_BUSY
#define EXAM_RANGE     BOARD_RANGE
#define EXAM_NOT_READY BOARD_NOT_READY
#define EXAM_BUTTON_INT0 BOARD_BUTTON_INT0
#define EXAM_BUTTON_KEY1 BOARD_BUTTON_KEY1
#define EXAM_BUTTON_KEY2 BOARD_BUTTON_KEY2
#define EXAM_PRESS       BUTTON_EVENT_PRESS
#define EXAM_RELEASE     BUTTON_EVENT_RELEASE
#define EXAM_JOY_SELECT JOYSTICK_SELECT
#define EXAM_JOY_DOWN   JOYSTICK_DOWN
#define EXAM_JOY_LEFT   JOYSTICK_LEFT
#define EXAM_JOY_RIGHT  JOYSTICK_RIGHT
#define EXAM_JOY_UP     JOYSTICK_UP
#define EXAM_TIMER_INTERRUPT TIMER_ACTION_INTERRUPT
#define EXAM_TIMER_RESET     TIMER_ACTION_RESET
#define EXAM_TIMER_STOP      TIMER_ACTION_STOP

void exam_init(void);
void exam_idle(void);

/* Printed LED numbers are 4..11. A mask uses the eight P2 output bits. */
exam_status_t exam_led_on(uint8_t printed_number);
exam_status_t exam_led_off(uint8_t printed_number);
exam_status_t exam_led_toggle(uint8_t printed_number);
exam_status_t exam_led_write(uint8_t mask);
uint8_t exam_led_read(void);
void exam_leds_off(void);

/* INT0, KEY1 and KEY2 are active-low; confirmation is 50 ms by default. */
exam_status_t exam_buttons_start(exam_button_callback_t callback);
/* Exact EINT handler setup only: no callback and no debounce scheduler. */
exam_status_t exam_button_irq_start(exam_button_t button);
void exam_buttons_confirmation_ms(uint32_t milliseconds);
uint8_t exam_button_pressed(exam_button_t button);
uint32_t exam_buttons_pressed(void);

/* Joystick results are masks, so diagonal input remains visible. */
exam_status_t exam_joystick_start(exam_joystick_callback_t callback);
uint32_t exam_joystick_read(void);
uint32_t exam_joystick_first(void);
void exam_joystick_reset_first(void);

/* Timer number is 0..3. */
exam_status_t exam_timer_every_ms(int timer, int milliseconds, exam_timer_callback_t callback);
exam_status_t exam_timer_every_hz(int timer, int hertz, exam_timer_callback_t callback);
exam_status_t exam_timer_clock_divider(uint8_t timer, uint8_t divider);
exam_status_t exam_timer_prescaler(uint8_t timer, uint32_t prescaler);
exam_status_t exam_timer_match(uint8_t timer, uint8_t match, uint32_t ticks, uint32_t actions);
exam_status_t exam_timer_start(uint8_t timer);
exam_status_t exam_timer_stop(uint8_t timer);
exam_status_t exam_timer_reset(uint8_t timer);
uint32_t exam_timer_count(uint8_t timer);
uint8_t exam_timer_match_happened(uint32_t flags, uint8_t match);
uint8_t exam_timer_capture_happened(uint32_t flags, uint8_t capture);

exam_status_t exam_rit_start(void);
void exam_rit_stop(void);
uint32_t exam_rit_ticks(void);
exam_status_t exam_systick_every_ms(int milliseconds);
uint32_t exam_systick_ticks(void);

/* Potentiometer: fit JP12. A fresh result is 0..4095. */
exam_status_t exam_pot_start(void);
exam_status_t exam_pot_read(int *value);
exam_status_t exam_adc_read(uint8_t channel, uint16_t *value);

/* Speaker/analog output: fit JP2. A sample is 0..1023. */
exam_status_t exam_dac_write(int value);
exam_status_t exam_dac_percent(int percent);
void exam_dac_silence(void);

/* Event bits transfer deferred work from callbacks to exam_user_loop. */
void exam_events_set(uint32_t bits);
uint32_t exam_events_take(uint32_t mask);
uint32_t exam_critical_enter(void);
void exam_critical_exit(uint32_t saved_primask);

uint32_t exam_self_test(void);
extern volatile exam_fault_snapshot_t fault_snapshot;
extern volatile uint8_t fault_snapshot_valid;

#endif
