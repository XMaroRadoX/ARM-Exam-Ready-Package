# Current API Gap Report

This report records conveniences found in retired material that are not declarations in the current Official Combined Exam API. They are not restored, aliased, or presented as current functions.

- Core conveniences absent: exam_idle, exam_self_test. Use __WFI directly when sleeping is appropriate; the template does not claim a board self-test API.
- Retired LED names absent: exam_led_from_board_label, exam_led_set, exam_leds_bar, exam_leds_clear, exam_leds_fill, exam_leds_read, exam_leds_write.
- Retired button names absent: exam_button_irq_start, exam_button_is_down, exam_button_pressed_edges, exam_button_released_edges, exam_buttons_confirmation_ms, exam_buttons_down, exam_buttons_start.
- Retired joystick names absent: exam_joystick_down, exam_joystick_first, exam_joystick_released_edges, exam_joystick_reset_first, exam_joystick_start. The current API stores no key-repeat policy.
- Retired ADC and potentiometer names absent: exam_adc_read_raw, exam_potentiometer_read_percent, exam_potentiometer_read_raw, exam_potentiometer_start.
- Retired DAC names absent: exam_dac_play, exam_dac_silence, exam_dac_stop, exam_dac_write_percent, exam_dac_write_raw. Playback scheduling belongs to question code.
- Retired RIT and SysTick names absent: exam_rit_ticks, exam_systick_periodic_ms, exam_systick_ticks.
- Retired general-timer names absent: exam_timer_capture_happened, exam_timer_clock_divider, exam_timer_free_running_start, exam_timer_match, exam_timer_match_happened, exam_timer_periodic_hz, exam_timer_periodic_ms, exam_timer_prescaler.
- The current API has no callback-registration layer. Put question-specific work in the existing IRQ source or publish an event to main.
- EXAM_TIMER_FREE_RUNNING is only a compatibility alias for EXAM_TIMER_MODULO_NO_IRQ, not a true unrestricted 32-bit free-running mode.

The current header remains the sole interface authority. Use the generated complete reference for its 52 public functions.
