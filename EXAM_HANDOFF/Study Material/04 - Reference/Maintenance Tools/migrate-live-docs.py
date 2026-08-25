from pathlib import Path

STUDY = Path(__file__).resolve().parents[2]
SKIP = (
    "Original and Legacy Archives",
    "Original two-file migration snapshot",
    "Superseded",
    "Solved Answer Builds",
    "Recipe Builds",
)

REPLACE = [
    ("exam_user_contract.h", "exam_board.h"),
    ("exam_api.h", "exam_board.h"),
    ("exam_api.c", "exam_board.c"),
    ("exam_user.c", "main.c"),
    ("exam_user.h", "main.c declarations"),
    ("exam/main.c declarations", "Answer/main.c"),
    ("exam_main.c", "main.c"),
    ("exam_asm.s", "assembly.s"),
    ("exam_asm_solution", "asm_solution"),
    ("exam_user_10ms_hook", "user_10ms_hook"),
    ("exam_user_init()", "the initialization section of main()"),
    ("exam_user_loop()", "the foreground loop in main()"),
    ("exam_user_init", "main initialization"),
    ("exam_user_loop", "main foreground loop"),
    ("exam_status_t", "board_status_t"),
    ("EXAM_NOT_READY", "BOARD_NOT_READY"),
    ("EXAM_NOT_ENABLED", "BOARD_NOT_ENABLED"),
    ("EXAM_INVALID", "BOARD_INVALID"),
    ("EXAM_RANGE", "BOARD_RANGE"),
    ("EXAM_BUSY", "BOARD_BUSY"),
    ("EXAM_OK", "BOARD_OK"),
    ("exam_init", "board_init"),
    ("exam_idle", "board_idle"),
    ("exam_button_callback_t", "button_callback_t"),
    ("exam_button_event_t", "button_event_t"),
    ("exam_button_t", "board_button_t"),
    ("EXAM_BUTTON_INT0", "BOARD_BUTTON_INT0"),
    ("EXAM_BUTTON_KEY1", "BOARD_BUTTON_KEY1"),
    ("EXAM_BUTTON_KEY2", "BOARD_BUTTON_KEY2"),
    ("EXAM_PRESS", "BUTTON_EVENT_PRESS"),
    ("EXAM_RELEASE", "BUTTON_EVENT_RELEASE"),
    ("exam_buttons_confirmation_ms", "buttons_set_confirmation_ms"),
    ("exam_buttons_start", "buttons_init"),
    ("exam_buttons_down", "buttons_pressed_mask"),
    ("exam_button_is_down", "button_is_pressed"),
    ("exam_button_irq_start", "button_irq_start"),
    ("exam_joystick_callback_t", "joystick_callback_t"),
    ("exam_joystick_start", "joystick_init"),
    ("exam_joystick_down", "joystick_read"),
    ("exam_joystick_first", "joystick_first_movement"),
    ("exam_joystick_reset_first", "joystick_reset_first_movement"),
    ("EXAM_JOY_SELECT", "JOYSTICK_SELECT"),
    ("EXAM_JOY_DOWN", "JOYSTICK_DOWN"),
    ("EXAM_JOY_LEFT", "JOYSTICK_LEFT"),
    ("EXAM_JOY_RIGHT", "JOYSTICK_RIGHT"),
    ("EXAM_JOY_UP", "JOYSTICK_UP"),
    ("exam_leds_write", "led_write_mask"),
    ("exam_leds_read", "led_read_mask"),
    ("exam_leds_clear", "led_all_off"),
    ("exam_leds_fill", "led_write_mask"),
    ("exam_leds_bar", "answer-local LED bar helper"),
    ("exam_led_set", "led_write_number"),
    ("exam_led_on", "led_on"),
    ("exam_led_off", "led_off"),
    ("exam_led_toggle", "led_toggle"),
    ("exam_timer_callback_t", "timer_callback_t"),
    ("exam_timer_t", "uint8_t"),
    ("exam_timer_periodic_ms", "timer_every_ms"),
    ("exam_timer_periodic_hz", "timer_every_hz"),
    ("exam_timer_match_happened", "timer_match_occurred"),
    ("exam_timer_capture_happened", "timer_capture_occurred"),
    ("exam_timer_clock_divider", "timer_set_clock_divider"),
    ("exam_timer_prescaler", "timer_set_prescaler"),
    ("exam_timer_match", "timer_configure_match"),
    ("exam_timer_read", "timer_read_counter"),
    ("exam_timer_reset", "timer_reset"),
    ("exam_timer_start", "timer_start"),
    ("exam_timer_stop", "timer_stop"),
    ("EXAM_TIMER_INTERRUPT", "TIMER_ACTION_INTERRUPT"),
    ("EXAM_TIMER_RESET", "TIMER_ACTION_RESET"),
    ("EXAM_TIMER_STOP", "TIMER_ACTION_STOP"),
    ("EXAM_TIMER_0", "0u"),
    ("EXAM_TIMER_1", "1u"),
    ("EXAM_TIMER_2", "2u"),
    ("EXAM_TIMER_3", "3u"),
    ("exam_events_set", "event_flags_set"),
    ("exam_events_take", "event_flags_take"),
    ("exam_critical_enter", "critical_enter"),
    ("exam_critical_exit", "critical_exit"),
    ("exam_potentiometer_start", "potentiometer_start"),
    ("exam_potentiometer_read_raw", "potentiometer_read"),
    ("exam_adc_sample_t", "adc_sample_t"),
    ("exam_adc_read_raw", "adc_read_channel"),
    ("exam_adc_read", "adc_read_value"),
    ("exam_dac_write_raw", "dac_write"),
    ("exam_dac_write_percent", "speaker_write_percent"),
    ("exam_dac_play", "dac_play_samples"),
    ("exam_dac_stop", "dac_stop_samples"),
    ("exam_dac_silence", "dac_silence"),
    ("exam_rit_start", "rit_scheduler_start"),
    ("exam_rit_stop", "rit_scheduler_stop"),
    ("exam_rit_ticks", "rit_scheduler_ticks"),
    ("exam_systick_periodic_ms", "systick_start_periodic_ms"),
    ("exam_systick_ticks", "systick_ticks"),
    ("exam_fault_snapshot_t", "fault_snapshot_t"),
    ("exam_svc_context_t", "svc_context_t"),
    ("exam_self_test", "board_self_test_run"),
]

def main():
    changed = 0
    for path in STUDY.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".csv", ".json", ".txt"}:
            continue
        rel = str(path.relative_to(STUDY))
        if any(part in rel for part in SKIP):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        updated = text
        for old, new in REPLACE:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed += 1
    print(f"updated active documentation files: {changed}")

if __name__ == "__main__":
    main()
