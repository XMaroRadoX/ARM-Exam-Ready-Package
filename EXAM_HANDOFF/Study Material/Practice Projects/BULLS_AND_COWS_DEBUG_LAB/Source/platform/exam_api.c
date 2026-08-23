#include "exam_api.h"

void exam_init(void) { board_init(); }
void exam_idle(void) { board_idle(); }
exam_status_t exam_led_on(uint8_t n) { return led_on(n); }
exam_status_t exam_led_off(uint8_t n) { return led_off(n); }
exam_status_t exam_led_toggle(uint8_t n) { return led_toggle(n); }
exam_status_t exam_led_write(uint8_t mask) { return led_write_mask(mask); }
uint8_t exam_led_read(void) { return led_read_mask(); }
void exam_leds_off(void) { led_all_off(); }
exam_status_t exam_buttons_start(exam_button_callback_t cb)
{
  exam_status_t status = rit_scheduler_start();
  if (status != EXAM_OK) return status;
  buttons_init(cb);
  return EXAM_OK;
}
exam_status_t exam_button_irq_start(exam_button_t b) { return button_irq_start(b); }
void exam_buttons_confirmation_ms(uint32_t ms) { buttons_set_confirmation_ms(ms); }
uint8_t exam_button_pressed(exam_button_t b) { return button_is_pressed(b); }
uint32_t exam_buttons_pressed(void) { return buttons_pressed_mask(); }
exam_status_t exam_joystick_start(exam_joystick_callback_t cb)
{
  exam_status_t status = rit_scheduler_start();
  if (status != EXAM_OK) return status;
  joystick_init(cb);
  return EXAM_OK;
}
uint32_t exam_joystick_read(void) { return joystick_read(); }
uint32_t exam_joystick_first(void) { return joystick_first_movement(); }
void exam_joystick_reset_first(void) { joystick_reset_first_movement(); }
exam_status_t exam_timer_every_ms(int t, int ms, exam_timer_callback_t cb) { return timer_every_ms(t, ms, cb); }
exam_status_t exam_timer_every_hz(int t, int hz, exam_timer_callback_t cb) { return timer_every_hz(t, hz, cb); }
exam_status_t exam_timer_clock_divider(uint8_t t, uint8_t d) { return timer_set_clock_divider(t, d); }
exam_status_t exam_timer_prescaler(uint8_t t, uint32_t p) { return timer_set_prescaler(t, p); }
exam_status_t exam_timer_match(uint8_t t, uint8_t m, uint32_t ticks, uint32_t a) { return timer_configure_match(t, m, ticks, a); }
exam_status_t exam_timer_start(uint8_t t) { return timer_start(t); }
exam_status_t exam_timer_stop(uint8_t t) { return timer_stop(t); }
exam_status_t exam_timer_reset(uint8_t t) { return timer_reset(t); }
uint32_t exam_timer_count(uint8_t t) { return timer_read_counter(t); }
uint8_t exam_timer_match_happened(uint32_t f, uint8_t m) { return timer_match_occurred(f, m); }
uint8_t exam_timer_capture_happened(uint32_t f, uint8_t c) { return timer_capture_occurred(f, c); }
exam_status_t exam_rit_start(void) { return rit_scheduler_start(); }
void exam_rit_stop(void) { rit_scheduler_stop(); }
uint32_t exam_rit_ticks(void) { return rit_scheduler_ticks(); }
exam_status_t exam_systick_every_ms(int ms) { return systick_every_ms(ms); }
uint32_t exam_systick_ticks(void) { return systick_ticks(); }
exam_status_t exam_pot_start(void) { return potentiometer_start(); }
exam_status_t exam_pot_read(int *value) { return potentiometer_read(value); }
exam_status_t exam_adc_read(uint8_t channel, uint16_t *value) { return adc_read_value(channel, value); }
exam_status_t exam_dac_write(int value) { return speaker_write(value); }
exam_status_t exam_dac_percent(int percent) { return speaker_write_percent(percent); }
void exam_dac_silence(void) { dac_silence(); }
void exam_events_set(uint32_t bits) { event_flags_set(bits); }
uint32_t exam_events_take(uint32_t mask) { return event_flags_take(mask); }
uint32_t exam_critical_enter(void) { return critical_enter(); }
void exam_critical_exit(uint32_t saved) { critical_exit(saved); }
uint32_t exam_self_test(void) { return board_self_test_run(); }
