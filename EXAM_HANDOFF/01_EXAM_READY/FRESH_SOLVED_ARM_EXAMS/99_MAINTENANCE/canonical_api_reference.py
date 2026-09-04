"""Canonical human documentation for the Official Combined Exam API.

The C header and implementation define the interface and behavior.  This file
contains the one maintained set of explanations used to generate both the raw
Markdown reference and every portal API page.
"""

from __future__ import annotations


GROUP_ORDER = [
    "Core", "LEDs", "Buttons", "Timers", "SysTick", "RIT",
    "Joystick", "ADC", "DAC", "Events", "Faults", "SVC",
]

GROUP_DESCRIPTIONS = {
    "Core": "Initialize the board support and reset the API's shared software state.",
    "LEDs": "Control the eight board LEDs through the professor-compatible LED driver.",
    "Buttons": "Use raw external interrupts or the API's time-source-independent debounce state machine.",
    "Timers": "Configure Timer0 through Timer3 with MR0 convenience calls or independent match channels and explicit peripheral-clock controls.",
    "SysTick": "Start or stop the Cortex-M3 system tick for short periodic work.",
    "RIT": "Configure and control the LPC1768 Repetitive Interrupt Timer.",
    "Joystick": "Read the five active-low joystick controls and derive press and release edges.",
    "ADC": "Start one channel-5 conversion, capture it in the IRQ, and consume the fresh 12-bit result in main.",
    "DAC": "Initialize P0.26 as AOUT and write a validated 10-bit sample.",
    "Events": "Transfer bit flags safely between interrupt handlers and foreground code, or protect a short compound update.",
    "Faults": "Configure Cortex-M3 fault trapping and preserve a debugger-readable exception snapshot when fault wrappers are enabled.",
    "SVC": "Decode an SVC immediate and pass the stacked exception frame to an overridable dispatcher.",
}

STATUS_VALUES = [
    ("EXAM_OK", "The operation completed successfully."),
    ("EXAM_BAD_ARGUMENT", "An enum value, pointer-dependent setup, or mode argument is invalid."),
    ("EXAM_OUT_OF_RANGE", "A numeric value cannot be represented or accepted by the hardware helper."),
    ("EXAM_NOT_READY", "Required configuration or a usable clock value is not available yet."),
]

PUBLIC_TYPES = [
    ("exam_status_t", "Status returned by validated configuration and output helpers."),
    ("exam_button_t", "EXAM_BUTTON_INT0, EXAM_BUTTON_KEY1, or EXAM_BUTTON_KEY2."),
    ("exam_timer_t", "EXAM_TIMER0 through EXAM_TIMER3."),
    ("exam_timer_mode_t", "Periodic, one-shot, or modulo-without-MR0-interrupt operation."),
    ("exam_exception_frame_t", "The eight words automatically stacked by the Cortex-M3 on exception entry."),
    ("exam_fault_snapshot_t", "The stacked frame plus Cortex-M3 fault-status registers captured before the fault loop."),
]

PUBLIC_CONSTANTS = [
    ("EXAM_BUTTON_EVENT_INT0", "Bit 0 in the debounced button-event word."),
    ("EXAM_BUTTON_EVENT_KEY1", "Bit 1 in the debounced button-event word."),
    ("EXAM_BUTTON_EVENT_KEY2", "Bit 2 in the debounced button-event word."),
    ("EXAM_JOY_SELECT", "Bit 0 returned by exam_joystick_read()."),
    ("EXAM_JOY_DOWN", "Bit 1 returned by exam_joystick_read()."),
    ("EXAM_JOY_LEFT", "Bit 2 returned by exam_joystick_read()."),
    ("EXAM_JOY_RIGHT", "Bit 3 returned by exam_joystick_read()."),
    ("EXAM_JOY_UP", "Bit 4 returned by exam_joystick_read()."),
    ("EXAM_ENABLE_FAULT_HANDLERS", "Set to 1 for the complete target to emit the API fault wrappers; default 0."),
    ("EXAM_ENABLE_SVC_HANDLER", "Set to 1 for the complete target to emit the API SVC wrapper; default 0."),
]

PUBLIC_GLOBALS = [
    ("exam_fault_snapshot", "Volatile debugger-readable state written by exam_fault_capture_from_exception()."),
    ("exam_fault_snapshot_valid", "Set to 1 only after the complete snapshot has been stored."),
]

LEGACY_GAPS = [
    "Core conveniences absent: exam_idle, exam_self_test. Use __WFI directly when sleeping is appropriate; the template does not claim a board self-test API.",
    "Retired LED names absent: exam_led_from_board_label, exam_led_set, exam_leds_bar, exam_leds_clear, exam_leds_fill, exam_leds_read, exam_leds_write.",
    "Retired button names absent: exam_button_irq_start, exam_button_is_down, exam_button_pressed_edges, exam_button_released_edges, exam_buttons_confirmation_ms, exam_buttons_down, exam_buttons_start.",
    "Retired joystick names absent: exam_joystick_down, exam_joystick_first, exam_joystick_released_edges, exam_joystick_reset_first, exam_joystick_start. The current API stores no key-repeat policy.",
    "Retired ADC and potentiometer names absent: exam_adc_read_raw, exam_potentiometer_read_percent, exam_potentiometer_read_raw, exam_potentiometer_start.",
    "Retired DAC names absent: exam_dac_play, exam_dac_silence, exam_dac_stop, exam_dac_write_percent, exam_dac_write_raw. Playback scheduling belongs to question code.",
    "Retired RIT and SysTick names absent: exam_rit_ticks, exam_systick_periodic_ms, exam_systick_ticks.",
    "Retired general-timer names absent: exam_timer_capture_happened, exam_timer_clock_divider, exam_timer_free_running_start, exam_timer_match, exam_timer_match_happened, exam_timer_periodic_hz, exam_timer_periodic_ms, exam_timer_prescaler.",
    "The current API has no callback-registration layer. Put question-specific work in the existing IRQ source or publish an event to main.",
    "EXAM_TIMER_FREE_RUNNING is only a compatibility alias for EXAM_TIMER_MODULO_NO_IRQ, not a true unrestricted 32-bit free-running mode.",
]


def value(value: str, use: str, basis: str, exams: tuple[str, ...] = ()) -> dict[str, object]:
    return {"value": value, "use": use, "basis": basis, "exams": list(exams)}


VALUE_GUIDANCE: dict[str, list[dict[str, object]]] = {
    "exam_init": [value("Once", "First API call in main(); initialize only required peripherals afterward.", "Current template contract")],
    "exam_led_on": [value("4, 5, 6, 7, 11", "Physical board labels used by migrated button, timer, and result scenarios.", "Observed in reviewed solutions", ("2023-09-18-q2", "2023-02-07-q2"))],
    "exam_led_off": [value("4, 5, 6, 7", "Clear individual status LEDs without disturbing the rest.", "Observed in reviewed solutions", ("2023-09-18-q2", "2023-02-07-q2"))],
    "exam_led_toggle": [value("11", "Simple heartbeat or confirmed-button indicator.", "Recommended package recipe")],
    "exam_led_one_hot": [value("4..11", "Select by the printed board label. A logical position 0..7 converts to label 11 - position.", "API range")],
    "exam_led_write": [value("0x00", "Clear all LEDs." , "Observed in reviewed solutions"), value("0xFF", "Show an error/all-on state.", "Observed in reviewed solutions", ("2024-02-28-q2", "2026-06-25-arm1-q2")), value("sample >> 4", "Map a 12-bit ADC result to eight LEDs.", "Observed in reviewed solutions", ("2026-02-03-arm1-q2",))],
    "exam_led_read": [value("Returned uint8_t", "Save the current API-controlled LED mask; do not invent a physical input value.", "API contract")],
    "exam_led_clear": [value("No argument", "Start from a known all-off display before showing a result.", "Observed throughout reviewed solutions")],
    "exam_buttons_init": [value("Once", "Before enabling raw or debounced INT0/KEY1/KEY2 workflows.", "Observed throughout button-based solutions")],
    "exam_button_ack": [value("EXAM_BUTTON_INT0 / KEY1 / KEY2", "Use the enum matching the active EINT0/EINT1/EINT2 handler.", "Observed in reviewed solutions", ("2023-09-18-q2", "2024-09-16-q2"))],
    "exam_button_is_pressed": [value("1 pressed, 0 released", "Read a level only while the pin is usable as GPIO; it is not an edge event.", "API contract")],
    "exam_debounce_config": [value("10 ms sample, 50 ms confirmation", "Five stable samples; a conservative default for the supplied board buttons.", "Recommended maintained recipe, not a literal past-paper constant"), value("10 ms sample, 30 ms confirmation", "Three stable samples when faster response is preferred.", "Safe illustrative alternative, not observed in solved exams")],
    "exam_debounce_begin": [value("Matching button enum", "Begin from the corresponding EINT handler, for example KEY1 in EINT1_IRQHandler.", "Current template workflow")],
    "exam_debounce_tick": [value("Every 10 ms", "Must exactly match sample_period_ms used by exam_debounce_config.", "Recommended maintained recipe")],
    "exam_button_events_take": [value("EXAM_BUTTON_EVENT_INT0 / KEY1 / KEY2", "Take once into a local mask, then test every required event bit.", "Current template workflow")],
    "exam_timer_config_ticks": [value("0xFF", "Short modulo counter used as a seed/input source.", "Observed in reviewed solution", ("2023-02-07-q2",)), value("0xFFFF", "16-bit-style modulo counter without MR0 IRQ.", "Observed in reviewed solutions", ("2025-01-29-arm1-q2", "2025-01-29-arm2-q2", "2025-01-29-arm3-q2")), value("UINT32_MAX", "Longest modulo interval available through MR0.", "Observed in reviewed solutions", ("2024-02-12-q2", "2026-06-25-arm1-q2")), value("1263 / 1592", "Periodic DAC update intervals for the 2025 sine/cosine solutions; do not reuse without the same clock/math.", "Observed in reviewed solutions", ("2025-02-12-arm1-q2", "2025-02-12-arm2-q2"))],
    "exam_timer_config_ms": [value("50 ms", "Controller/scheduler tick.", "Observed in reviewed solutions", ("2026-02-18-arm1-q2",)), value("250 ms", "Toggle interval yielding a 500 ms full blink cycle.", "Observed in reviewed solution", ("2025-01-29-arm1-q2",)), value("500 ms", "Half-second display step.", "Observed in reviewed solutions", ("2024-02-28-q2", "2025-01-29-arm2-q2")), value("2000 / 2500 / 3000 ms", "Slow result display or rhythm interval, selected by the paper.", "Observed in reviewed solutions", ("2023-07-04-q2", "2025-07-01-arm2-q3", "2025-07-01-arm1-q3"))],
    "exam_timer_config_hz": [value("1000 Hz", "Illustrative 1 kHz sample/update rate when the question specifies frequency rather than period.", "Safe API example, not observed in reviewed solutions")],
    "exam_timer_start": [value("Same timer just configured", "Start last, after state and handler ownership are ready.", "Observed throughout timer-based solutions")],
    "exam_timer_stop": [value("Timer0/1/2", "Freeze or terminate a periodic/one-shot workflow before reading or resetting.", "Observed in reviewed solutions", ("2025-01-29-arm1-q2", "2026-02-18-arm1-q2"))],
    "exam_timer_reset": [value("Stop → reset → configure → start", "Reliable restart sequence when changing a timer role or threshold.", "Observed in reviewed solutions", ("2026-02-18-arm1-q2",))],
    "exam_timer_read": [value("Raw TC ticks", "Use directly as a pseudo-random seed/input only when the question permits; otherwise convert using PCLK.", "Observed in reviewed solutions", ("2023-02-07-q2", "2026-06-25-arm1-q2"))],
    "exam_timer_ack": [value("1u << 0", "Test returned MR0 bit after taking the pending mask once.", "Observed throughout timer IRQ solutions")],
    "exam_timer_is_running": [value("0 or 1", "Guard against starting overlapping Timer1/Timer2 note workflows.", "Observed in reviewed solutions", ("2026-02-18-arm1-q2", "2026-02-18-arm2-q2"))],
    "exam_systick_config_ticks": [value("0x100000", "DFS scheduling tick used by the 2024 SysTick solution.", "Observed in reviewed solution", ("2024-07-09-q2",))],
    "exam_systick_config_ms": [value("10 ms", "Alternative debounce tick source; configuration starts SysTick immediately.", "Recommended workflow value, not observed in reviewed solutions")],
    "exam_systick_stop": [value("No argument", "Stop only when no other feature depends on SysTick.", "API ownership rule")],
    "exam_rit_config_ticks": [value("SystemFrequency / 100", "Ten-millisecond interval when RIT runs at CCLK.", "Derived equivalent of observed 10 ms usage")],
    "exam_rit_config_ms": [value("10 ms", "Joystick polling and input-edge sampling.", "Observed in reviewed solutions", ("2025-07-01-arm1-q3", "2025-07-01-arm2-q3", "2026-06-25-arm1-q2", "2026-06-25-arm2-q2"))],
    "exam_rit_start": [value("After successful configuration", "Start only after the handler and sampled state are initialized.", "Observed in reviewed solutions")],
    "exam_rit_stop": [value("No argument", "Stop when every RIT consumer has finished.", "API ownership rule")],
    "exam_rit_reset": [value("No argument", "Restart the counter origin; this does not replace IRQ acknowledgement.", "API contract")],
    "exam_rit_ack": [value("First line of RIT_IRQHandler", "Clear the hardware source before sampling or publishing events.", "Observed in reviewed solutions", ("2025-07-01-arm1-q3", "2026-06-25-arm1-q2"))],
    "exam_joystick_init": [value("Once", "Before the first state sample and before starting the 10 ms RIT poll.", "Observed in reviewed solutions")],
    "exam_joystick_read": [value("0..0x1F mask", "Store the first reading as previous; later readings are current.", "Observed in reviewed solutions")],
    "exam_joystick_pressed_edges": [value("previous, current", "Returns new press bits only; then assign previous=current.", "Observed in reviewed solutions", ("2025-07-01-arm1-q3", "2026-06-25-arm1-q2"))],
    "exam_adc_init": [value("Channel 5 / P1.31", "The fixed potentiometer input supported by this API.", "Current hardware contract")],
    "exam_adc_start": [value("One conversion", "Start once after init and again only after consuming the previous sample.", "Observed in reviewed solutions", ("2026-02-03-arm1-q2",))],
    "exam_adc_irq_capture": [value("ADGDR DONE=1", "Capture only completed 12-bit values; the helper ignores incomplete reads.", "Current hardware contract")],
    "exam_adc_take": [value("0..4095", "Valid 12-bit result only when the function returns 1.", "API range and observed workflow", ("2026-02-03-arm1-q2", "2026-02-03-arm2-q2", "2026-02-03-arm3-q2"))],
    "exam_adc_show_high8": [value("result >> 4", "Display ADC bits 11:4 as 0..255 on LEDs.", "Observed conversion pattern", ("2026-02-03-arm1-q2",))],
    "exam_dac_init": [value("Initial sample 0", "Start from silence/zero output before waveform playback.", "Observed in reviewed solutions", ("2026-02-18-arm1-q2",))],
    "exam_dac_write": [value("0", "Silence/terminate output.", "Observed in reviewed solutions", ("2025-02-12-arm1-q2", "2026-02-18-arm1-q2")), value("500", "Midscale DC offset around which signed waveform terms are centered.", "Observed in 2025 sine/cosine solutions", ("2025-02-12-arm1-q2", "2025-02-12-arm2-q2")), value("0..1023", "Only accepted hardware sample range.", "API range")],
    "exam_events_set": [value("1u << 0", "Typical first application event bit; assign one non-overlapping bit per event.", "Observed event pattern", ("2024-02-28-q2", "2026-06-25-arm1-q2"))],
    "exam_events_take": [value("Combined event mask", "Take once, then test all returned bits in foreground.", "Observed event pattern", ("2024-02-28-q2", "2026-06-25-arm1-q2"))],
    "exam_critical_enter": [value("Returned PRIMASK key", "Save exactly; never replace it with a guessed 0 or 1.", "Observed protected snapshot pattern", ("2026-06-25-arm1-q2",))],
    "exam_critical_exit": [value("saved", "Pass the unchanged value returned by the matching enter call.", "Observed protected snapshot pattern", ("2026-06-25-arm1-q2",))],
    "exam_faults_configure": [value("1, 1, 1", "Enable configurable faults plus divide-by-zero and unaligned traps for a deliberate debugger exercise.", "Safe illustrative configuration, not used by reviewed solutions"), value("0, 0, 0", "Disable those optional traps.", "API behavior")],
    "exam_fault_snapshot_clear": [value("Before each deliberate fault", "Marks old debugger state invalid without zeroing every field.", "Recommended debugger workflow")],
    "exam_fault_capture_from_exception": [value("Wrapper-provided frame and EXC_RETURN", "Never invent these arguments in normal foreground code.", "Exception ABI contract")],
    "exam_svc_capture_from_exception": [value("Wrapper-provided frame", "The bridge reads the SVC immediate at stacked PC minus two bytes.", "Cortex-M3 exception contract")],
    "exam_svc_dispatch": [value("Service 1", "Illustrative add service returning through stacked r0; actual service numbers come from the paper.", "Safe illustration based on the 2023 SVC topic", ("2023-02-24-q2",))],
}


SCENARIOS = [
    {
        "id": "debounced-key1",
        "title": "Debounced KEY1 press using a 10 ms RIT tick",
        "basis": "Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.",
        "exams": [],
        "functions": ("exam_buttons_init", "exam_debounce_config", "exam_debounce_begin", "exam_debounce_tick", "exam_button_events_take", "exam_rit_config_ms", "exam_rit_start", "exam_rit_ack", "exam_led_toggle"),
        "code": '''/* main setup */
exam_init();
exam_buttons_init();
if (exam_debounce_config(10u, 50u) == EXAM_OK &&
    exam_rit_config_ms(10u) == EXAM_OK) {
  exam_rit_start();
}

/* Source/button_EXINT/IRQ_button.c */
void EINT1_IRQHandler(void) {
  (void)exam_debounce_begin(EXAM_BUTTON_KEY1);
}

/* Source/RIT/IRQ_RIT.c */
void RIT_IRQHandler(void) {
  exam_rit_ack();
  exam_debounce_tick();
}

/* foreground loop */
uint32_t buttons = exam_button_events_take();
if ((buttons & EXAM_BUTTON_EVENT_KEY1) != 0u) {
  (void)exam_led_toggle(11u);
}''',
    },
    {
        "id": "half-second-display",
        "title": "Publish a half-second Timer0 event to the foreground",
        "basis": "Observed in the reviewed 2024-02-28 shortest-path solution.",
        "exams": ["2024-02-28-q2"],
        "functions": ("exam_timer_config_ms", "exam_timer_start", "exam_timer_ack", "exam_events_set", "exam_events_take", "exam_led_on", "exam_led_clear"),
        "code": '''#define EVENT_HALF_SECOND (1u << 0)

void TIMER0_IRQHandler(void) {
  uint32_t pending = exam_timer_ack(EXAM_TIMER0);
  if ((pending & 1u) != 0u) exam_events_set(EVENT_HALF_SECOND);
}

/* main setup */
exam_init();
if (exam_timer_config_ms(EXAM_TIMER0, 500u,
                         EXAM_TIMER_PERIODIC) == EXAM_OK)
  exam_timer_start(EXAM_TIMER0);

/* foreground loop */
if ((exam_events_take(EVENT_HALF_SECOND) & EVENT_HALF_SECOND) != 0u) {
  /* advance one display step */
}''',
    },
    {
        "id": "free-running-seed",
        "title": "Use a long modulo timer as an unpredictable user-timing seed",
        "basis": "UINT32_MAX is observed in the reviewed 2024 maze and 2026 game solutions; 0xFF and 0xFFFF appear in earlier timer questions.",
        "exams": ["2024-02-12-q2", "2026-06-25-arm1-q2"],
        "functions": ("exam_timer_config_ticks", "exam_timer_start", "exam_timer_read", "exam_timer_stop"),
        "code": '''exam_init();
if (exam_timer_config_ticks(EXAM_TIMER1, UINT32_MAX,
                            EXAM_TIMER_MODULO_NO_IRQ) == EXAM_OK)
  exam_timer_start(EXAM_TIMER1);

/* Read when the user acts; TC is a raw tick value. */
uint32_t seed = exam_timer_read(EXAM_TIMER1);''',
    },
    {
        "id": "systick-dfs",
        "title": "Start the exact SysTick interval used by the 2024 DFS solution",
        "basis": "Observed in the reviewed 2024-07-09 DFS/SysTick solution.",
        "exams": ["2024-07-09-q2"],
        "functions": ("exam_systick_config_ticks", "exam_systick_stop"),
        "code": '''exam_init();
if (exam_systick_config_ticks(0x100000u) != EXAM_OK) {
  exam_led_write(0xFFu);
}
/* Successful configuration has already started SysTick. */''',
    },
    {
        "id": "systick-debounce",
        "title": "Use SysTick instead of RIT for the same debounce interval",
        "basis": "Safe API-derived alternative; not an observed solved-exam combination.",
        "exams": [],
        "functions": ("exam_systick_config_ms", "exam_systick_stop", "exam_debounce_config", "exam_debounce_tick"),
        "code": '''exam_buttons_init();
if (exam_debounce_config(10u, 50u) == EXAM_OK)
  (void)exam_systick_config_ms(10u); /* starts immediately */

void SysTick_Handler(void) {
  exam_debounce_tick(); /* SysTick acknowledgement is automatic */
}''',
    },
    {
        "id": "joystick-poll",
        "title": "Poll joystick press edges every 10 ms",
        "basis": "Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions.",
        "exams": ["2025-07-01-arm1-q3", "2026-06-25-arm1-q2"],
        "functions": ("exam_joystick_init", "exam_joystick_read", "exam_joystick_pressed_edges", "exam_rit_config_ms", "exam_rit_start", "exam_rit_ack", "exam_events_set", "exam_events_take"),
        "code": '''static uint32_t previous_joystick;
#define EVENT_JOYSTICK (1u << 0)

void RIT_IRQHandler(void) {
  uint32_t current, pressed;
  exam_rit_ack();
  current = exam_joystick_read();
  pressed = exam_joystick_pressed_edges(previous_joystick, current);
  previous_joystick = current;
  if (pressed != 0u) exam_events_set(EVENT_JOYSTICK);
}

exam_joystick_init();
previous_joystick = exam_joystick_read();
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();''',
    },
    {
        "id": "adc-mailbox",
        "title": "Continuously convert the potentiometer and show its high byte",
        "basis": "Observed in the three reviewed 2026-02-03 ADC solutions.",
        "exams": ["2026-02-03-arm1-q2", "2026-02-03-arm3-q2"],
        "functions": ("exam_adc_init", "exam_adc_start", "exam_adc_irq_capture", "exam_adc_take", "exam_adc_show_high8", "exam_led_write"),
        "code": '''void ADC_IRQHandler(void) {
  exam_adc_irq_capture();
}

exam_init();
exam_adc_init();
exam_adc_start();
for (;;) {
  uint16_t sample;
  if (exam_adc_take(&sample)) {
    exam_adc_show_high8(sample);
    exam_adc_start();
  }
  __WFI();
}''',
    },
    {
        "id": "dac-waveform",
        "title": "Stream validated DAC samples from a periodic timer",
        "basis": "The 1263-tick Timer0 schedule, samples centered around 500, and zero termination are observed in the reviewed 2025 sine solution.",
        "exams": ["2025-02-12-arm1-q2"],
        "functions": ("exam_dac_init", "exam_dac_write", "exam_timer_config_ticks", "exam_timer_start", "exam_timer_ack", "exam_timer_stop"),
        "code": '''static const uint16_t wave[] = {500u, 620u, 500u, 380u};
static uint32_t sample_index;

void TIMER0_IRQHandler(void) {
  if ((exam_timer_ack(EXAM_TIMER0) & 1u) == 0u) return;
  (void)exam_dac_write(wave[sample_index]);
  sample_index = (sample_index + 1u) % 4u;
}

exam_init();
exam_dac_init();
if (exam_timer_config_ticks(EXAM_TIMER0, 1263u,
                            EXAM_TIMER_PERIODIC) == EXAM_OK)
  exam_timer_start(EXAM_TIMER0);''',
    },
    {
        "id": "multi-timer-note",
        "title": "Periodic waveform timer plus one-shot duration timer",
        "basis": "Observed structure in both reviewed 2026-02-18 three-timer solutions; thresholds are calculated by the paper's algorithm rather than guessed constants.",
        "exams": ["2026-02-18-arm1-q2", "2026-02-18-arm2-q2"],
        "functions": ("exam_timer_config_ticks", "exam_timer_start", "exam_timer_stop", "exam_timer_reset", "exam_timer_is_running", "exam_dac_write"),
        "code": '''exam_timer_stop(EXAM_TIMER1);
exam_timer_reset(EXAM_TIMER1);
exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                        EXAM_TIMER_PERIODIC);
exam_timer_stop(EXAM_TIMER2);
exam_timer_reset(EXAM_TIMER2);
exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                        EXAM_TIMER_ONE_SHOT);
exam_timer_start(EXAM_TIMER1);
exam_timer_start(EXAM_TIMER2);''',
    },
    {
        "id": "timer-hz",
        "title": "Configure a 1 kHz periodic update when frequency is given",
        "basis": "Safe API illustration. Reviewed solutions use tick and millisecond forms instead of exam_timer_config_hz.",
        "exams": [],
        "functions": ("exam_timer_config_hz", "exam_timer_start", "exam_timer_ack"),
        "code": '''if (exam_timer_config_hz(EXAM_TIMER2, 1000u,
                         EXAM_TIMER_PERIODIC) == EXAM_OK) {
  exam_timer_start(EXAM_TIMER2);
}''',
    },
    {
        "id": "raw-buttons",
        "title": "Use three raw button interrupts to select LED states",
        "basis": "Observed structure in the reviewed 2023-09-18 digit-addition solution.",
        "exams": ["2023-09-18-q2"],
        "functions": ("exam_buttons_init", "exam_button_ack", "exam_button_is_pressed", "exam_led_on", "exam_led_off", "exam_led_clear", "exam_init"),
        "code": '''void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  (void)exam_led_on(4u);
  (void)exam_led_off(5u);
}

exam_init();
exam_led_clear();
exam_buttons_init();''',
    },
    {
        "id": "led-pattern",
        "title": "Build and preserve a one-hot LED selection",
        "basis": "Safe current-API illustration. Use it when the question represents a selected position on LEDs; the exact position comes from the question logic.",
        "exams": [],
        "functions": ("exam_led_one_hot", "exam_led_read", "exam_led_write"),
        "code": '''uint8_t previous = exam_led_read();
(void)exam_led_one_hot(8u);  /* Physical LD8; pattern 0x08. */
/* The helper returns a status, not the selected bit mask. */
/* Restore the previous API-controlled pattern when required. */
exam_led_write(previous);''',
    },
    {
        "id": "rit-ticks-control",
        "title": "Configure and restart a 10 ms RIT interval in ticks",
        "basis": "Safe tick-form equivalent of the 10 ms RIT polling interval observed in the 2025 and 2026 joystick solutions. Confirm the RIT clock before deriving ticks.",
        "exams": ["2025-07-01-arm1-q3", "2026-06-25-arm1-q2"],
        "functions": ("exam_rit_config_ticks", "exam_rit_start", "exam_rit_stop", "exam_rit_reset", "exam_rit_ack"),
        "code": '''uint32_t rit_ticks = SystemFrequency / 100u; /* 10 ms only when RIT uses CCLK */
if (exam_rit_config_ticks(rit_ticks) == EXAM_OK) {
  exam_rit_reset();
  exam_rit_start();
}
/* Later, after every RIT consumer has finished: */
exam_rit_stop();''',
    },
    {
        "id": "atomic-pair",
        "title": "Take a two-word IRQ snapshot without tearing",
        "basis": "The protected snapshot pattern is observed in the reviewed 2026 game solutions.",
        "exams": ["2026-06-25-arm1-q2"],
        "functions": ("exam_critical_enter", "exam_critical_exit"),
        "code": '''uint32_t saved = exam_critical_enter();
uint32_t edges = joystick_press_edges;
joystick_press_edges = 0u;
exam_critical_exit(saved);
/* Process edges after interrupts are restored. */''',
    },
    {
        "id": "fault-debug",
        "title": "Capture a deliberate divide-by-zero fault for debugger inspection",
        "basis": "Safe debugger scenario based on the current opt-in fault API; not used by the reviewed solved exams.",
        "exams": [],
        "functions": ("exam_faults_configure", "exam_fault_snapshot_clear", "exam_fault_capture_from_exception"),
        "code": '''/* Define EXAM_ENABLE_FAULT_HANDLERS=1 for the whole target. */
exam_init();
exam_fault_snapshot_clear();
exam_faults_configure(1u, 1u, 1u);
/* A deliberate divide-by-zero now reaches the wrapper and never returns.
   Inspect exam_fault_snapshot only when exam_fault_snapshot_valid == 1. */''',
    },
    {
        "id": "svc-add",
        "title": "Return an SVC service result through stacked r0",
        "basis": "Illustrative current-API adaptation of the SVC topic in the reviewed 2023-02-24 exam.",
        "exams": ["2023-02-24-q2"],
        "functions": ("exam_svc_capture_from_exception", "exam_svc_dispatch"),
        "code": '''/* Define EXAM_ENABLE_SVC_HANDLER=1 for the whole target. */
void exam_svc_dispatch(uint8_t service_number,
                       exam_exception_frame_t *frame) {
  if (service_number == 1u) {
    frame->r0 = frame->r0 + frame->r1;
  }
}''',
    },
]


def p(direction: str, description: str) -> dict[str, str]:
    return {"direction": direction, "description": description}


def d(summary: str, *, params: dict[str, dict[str, str]] | None = None,
      returns: str, preconditions: str, side_effects: str, context: str,
      example: str, mistake: str, exam_note: str,
      related: tuple[str, ...] = ()) -> dict[str, object]:
    return {
        "summary": summary,
        "params": params or {},
        "returns": returns,
        "preconditions": preconditions,
        "side_effects": side_effects,
        "context": context,
        "example": example.strip(),
        "mistake": mistake,
        "exam_note": exam_note,
        "related": list(related),
    }


API_DOCS = {
    "exam_init": d(
        "Initialize the LPC1768 system clock and LED support, then clear every software flag and cached API state.",
        returns="No value.",
        preconditions="Call once near the start of main(), before any other exam_ helper.",
        side_effects="Calls SystemInit() and LED_init(); clears general events, button events, ADC freshness, debounce state, and the fault-snapshot valid flag. It does not initialize or start buttons, timers, SysTick, RIT, joystick, ADC, or DAC.",
        context="Foreground initialization only. It briefly masks interrupts while resetting shared software state.",
        example='''#include "exam_api.h"
#include "LPC17xx.h"

int main(void) {
  exam_init();
  exam_buttons_init();
  for (;;) { __WFI(); }
}''',
        mistake="Assuming exam_init() starts every peripheral or calling it again after interrupts are active and thereby erasing pending software events.",
        exam_note="Start every API-based answer here, then initialize only the peripherals the question actually uses.",
        related=("exam_buttons_init", "exam_joystick_init", "exam_adc_init", "exam_dac_init"),
    ),
    "exam_led_on": d(
        "Turn on one LED using its printed board label, 4 through 11.",
        params={"board_label": p("in", "Printed board label 4..11. LD11 maps to P2.0; LD4 maps to P2.7. Other values are rejected without changing the LEDs.")},
        returns="EXAM_OK, or EXAM_OUT_OF_RANGE when board_label is outside 4..11; invalid calls leave the display unchanged.",
        preconditions="exam_init() must have initialized the LED driver.",
        side_effects="Sets one LED bit and preserves the other seven LED states.",
        context="Safe from foreground or a short IRQ; the helper protects the shared LED shadow value with a short critical section.",
        example="if (exam_led_on(8u) != EXAM_OK) { /* handle invalid board label */ }",
        mistake="Using old 0..7 API indexes. Single-LED calls now take labels 4..11; migrate an old index to 11 - index. Values 4..7 have changed meaning.",
        exam_note="Use when the question says to set one LED without disturbing the rest.",
        related=("exam_led_off", "exam_led_toggle", "exam_led_one_hot"),
    ),
    "exam_led_off": d(
        "Turn off one board LED while preserving every other LED.",
        params={"board_label": p("in", "Printed board label 4..11, not a GPIO bit index.")},
        returns="EXAM_OK, or EXAM_OUT_OF_RANGE when board_label is outside 4..11; invalid calls leave the display unchanged.",
        preconditions="Call exam_init() first.",
        side_effects="Clears the selected bit in the LED output and shadow state.",
        context="Safe from foreground or a short IRQ; uses a bounded critical section.",
        example="(void)exam_led_off(8u);",
        mistake="Calling exam_led_clear() when only one LED should be turned off.",
        exam_note="Pair with exam_led_on() for explicit state control.",
        related=("exam_led_on", "exam_led_clear", "exam_led_read"),
    ),
    "exam_led_toggle": d(
        "Invert one LED based on the driver shadow state.",
        params={"board_label": p("in", "Printed board label 4..11, not a GPIO bit index.")},
        returns="EXAM_OK, or EXAM_OUT_OF_RANGE when board_label is outside 4..11; invalid calls leave the display unchanged.",
        preconditions="Call exam_init() first.",
        side_effects="Reads and updates the selected LED bit atomically with respect to interrupt code using the same helper.",
        context="Bounded and suitable for a timer IRQ when toggling is the complete required action.",
        example="if ((pending & 1u) != 0u) { (void)exam_led_toggle(11u); }",
        mistake="Reimplementing toggle as separate exam_led_read() and exam_led_write() calls, which creates a read-modify-write race.",
        exam_note="Useful for periodic blink questions; acknowledge the timer before toggling.",
        related=("exam_led_read", "exam_timer_ack", "exam_led_on"),
    ),
    "exam_led_one_hot": d(
        "Show exactly one lit LED selected by its printed board label.",
        params={"board_label": p("in", "Printed board label 4..11 of the only LED to light.")},
        returns="EXAM_OK, or EXAM_OUT_OF_RANGE when board_label is outside 4..11; invalid calls leave the display unchanged.",
        preconditions="Call exam_init() first.",
        side_effects="Replaces the complete eight-bit LED output with 1u << (11u - board_label).",
        context="Bounded call; safe in foreground or a short handler.",
        example="(void)exam_led_one_hot(8u); /* Only LD8; pattern 0x08. */",
        mistake="Passing a bit mask instead of a board label: 0x10 is not LD7. Pass 7 for LD7, or use exam_led_write(0x10u) for its mask.",
        exam_note="Use for moving-dot and selected-position displays.",
        related=("exam_led_write", "exam_led_clear"),
    ),
    "exam_led_write": d(
        "Write the complete eight-bit LED pattern.",
        params={"value": p("in", "Eight-bit display mask: bit n controls LD(11 - n). Bit 0 is LD11; bit 7 is LD4.")},
        returns="No value.",
        preconditions="Call exam_init() first.",
        side_effects="Replaces all eight LED states and updates the professor-driver shadow value.",
        context="Uses a short critical section; keep higher-level formatting outside an IRQ.",
        example="exam_led_write((uint8_t)(value & 0xFFu));",
        mistake="Expecting the call to preserve LEDs whose bits are zero.",
        exam_note="Use when an eight-bit result or ADC high byte must be displayed directly.",
        related=("exam_led_read", "exam_led_clear", "exam_adc_show_high8"),
    ),
    "exam_led_read": d(
        "Read the API's current eight-bit LED shadow value.",
        returns="The last LED pattern maintained by the LED driver as uint8_t.",
        preconditions="Call exam_init() before relying on the returned state.",
        side_effects="None; it reads the software shadow, not the physical voltage on the LED pins.",
        context="Safe from foreground or IRQ code; the read is protected by a short critical section.",
        example="uint8_t before = exam_led_read();",
        mistake="Treating the returned shadow value as an independent hardware input measurement.",
        exam_note="Use to inspect API-controlled LED state, not to build a non-atomic toggle sequence.",
        related=("exam_led_write", "exam_led_toggle"),
    ),
    "exam_led_clear": d(
        "Turn off all eight LEDs.",
        returns="No value.",
        preconditions="Call exam_init() first.",
        side_effects="Writes the complete LED output value 0.",
        context="Equivalent to exam_led_write(0u) and uses the same bounded critical section.",
        example="exam_led_clear();",
        mistake="Using it when only one selected LED should be cleared.",
        exam_note="Call before presenting a new result when the question requires a blank state.",
        related=("exam_led_write", "exam_led_off"),
    ),
    "exam_buttons_init": d(
        "Configure INT0, KEY1, and KEY2 as falling-edge external interrupts and reset button/debounce state.",
        returns="No value.",
        preconditions="Call exam_init() first and keep exactly one EINT0, EINT1, and EINT2 handler in the project.",
        side_effects="Clears EXTINT bits 0..2 and pending NVIC state, calls BUTTON_init(), resets debounce state and button events, and enables the button interrupt setup supplied by the template.",
        context="Foreground initialization only; call before waiting for button interrupts.",
        example="exam_init();\nexam_buttons_init();",
        mistake="Defining a second EINT handler or assuming initialization also implements the question-specific handler action.",
        exam_note="Choose raw acknowledgement or the debounce workflow in each existing EINT handler.",
        related=("exam_button_ack", "exam_debounce_begin", "exam_debounce_config"),
    ),
    "exam_button_ack": d(
        "Acknowledge one LPC1768 external-interrupt button source.",
        params={"button": p("in", "EXAM_BUTTON_INT0, EXAM_BUTTON_KEY1, or EXAM_BUTTON_KEY2. Invalid values are ignored.")},
        returns="No value.",
        preconditions="The selected button should have been initialized with exam_buttons_init().",
        side_effects="Writes the selected write-one-to-clear bit in LPC_SC->EXTINT.",
        context="Designed for the matching EINT handler; acknowledge before leaving a raw-button handler.",
        example="void EINT0_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_INT0); }",
        mistake="Returning from an EINT handler without clearing its EXTINT flag, causing immediate retriggering.",
        exam_note="For debouncing, call exam_debounce_begin() instead; it performs the acknowledgement itself.",
        related=("exam_buttons_init", "exam_debounce_begin", "exam_button_is_pressed"),
    ),
    "exam_button_is_pressed": d(
        "Read the current active-low GPIO level of one board button.",
        params={"button": p("in", "One valid exam_button_t value.")},
        returns="1 when pressed, 0 when released or when button is invalid.",
        preconditions="The pin must currently be usable as GPIO; exam_debounce_begin() temporarily establishes this for a debounced press.",
        side_effects="None.",
        context="A single bounded GPIO read. It does not debounce or acknowledge an interrupt.",
        example="if (exam_button_is_pressed(EXAM_BUTTON_KEY1)) { /* held now */ }",
        mistake="Treating a held level as a one-time press event.",
        exam_note="Use raw levels only when the paper wants level polling; use debounced events for one action per press.",
        related=("exam_debounce_tick", "exam_button_events_take"),
    ),
    "exam_debounce_config": d(
        "Set the number of periodic samples required to confirm a button press.",
        params={
            "sample_period_ms": p("in", "Actual interval in milliseconds between calls to exam_debounce_tick(); must be greater than 0."),
            "confirmation_ms": p("in", "Positive confirmation setting converted to ceil(confirmation_ms/sample_period_ms) consecutive pressed samples. This is a sample-count threshold, not a minimum wall-clock duration."),
        },
        returns="EXAM_OK; EXAM_BAD_ARGUMENT for either zero duration; EXAM_OUT_OF_RANGE if the rounded sample count cannot fit uint32_t.",
        preconditions="Call exam_init() first. Configure the timer, SysTick, or RIT that will call exam_debounce_tick() at sample_period_ms.",
        side_effects="Clears pending debounced events and cancels/restores every active debounce before installing the new threshold.",
        context="Foreground configuration; do not continuously reconfigure from an IRQ.",
        example="(void)exam_debounce_config(10u, 30u); /* three stable samples */",
        mistake="Passing the confirmation time as the tick period while the real tick uses a different interval.",
        exam_note="The API owns the sample count; your periodic interrupt owns timing. Five samples at10ms confirm roughly40..50ms after the initial edge, depending on sample phase; delayed servicing can extend this. A sampled release immediately rearms, as in the existing flow.",
        related=("exam_debounce_begin", "exam_debounce_tick", "exam_systick_config_ms"),
    ),
    "exam_debounce_begin": d(
        "Begin debouncing a button after its external interrupt fires.",
        params={"button": p("in", "The button whose EINT handler is currently running.")},
        returns="EXAM_OK; EXAM_BAD_ARGUMENT for an invalid button; EXAM_NOT_READY if debounce timing was not configured.",
        preconditions="Call exam_buttons_init() and exam_debounce_config() first.",
        side_effects="Disables the matching EINT NVIC source, changes the pin temporarily to GPIO, acknowledges EXTINT, and starts or preserves the per-button debounce state.",
        context="Call from the matching EINT handler. A periodic handler must then call exam_debounce_tick().",
        example="void EINT1_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_KEY1); }",
        mistake="Calling exam_button_ack() and then starting a second competing debounce mechanism.",
        exam_note="The interrupt is re-enabled only after exam_debounce_tick() observes release.",
        related=("exam_debounce_config", "exam_debounce_tick", "exam_button_events_take"),
    ),
    "exam_debounce_tick": d(
        "Advance every active button debounce state by one configured sample interval.",
        returns="No value.",
        preconditions="exam_debounce_config() must describe the real tick interval; active buttons are created by exam_debounce_begin().",
        side_effects="Records one event after enough stable pressed samples. On release it restores the EINT pin, clears pending state, and re-enables the matching NVIC interrupt.",
        context="Call exactly once per sample from one periodic IRQ source. The loop is bounded over three buttons.",
        example="void SysTick_Handler(void) { exam_debounce_tick(); }",
        mistake="Calling it from multiple timers or at an interval different from sample_period_ms.",
        exam_note="Keep the handler short; consume the recorded event later in main.",
        related=("exam_debounce_begin", "exam_button_events_take"),
    ),
    "exam_button_events_take": d(
        "Atomically obtain and clear all confirmed debounced button events.",
        returns="A bit mask containing EXAM_BUTTON_EVENT_INT0, EXAM_BUTTON_EVENT_KEY1, and/or EXAM_BUTTON_EVENT_KEY2; zero means no new event.",
        preconditions="Use the complete debounce flow to produce events.",
        side_effects="Clears all button event bits returned by this call.",
        context="Intended for the foreground loop. Events arriving after the protected snapshot remain pending for the next call.",
        example="uint32_t e = exam_button_events_take();\nif ((e & EXAM_BUTTON_EVENT_KEY1) != 0u) { /* once per press */ }",
        mistake="Calling it repeatedly in separate if expressions and clearing events before later tests see them.",
        exam_note="Take once into a local variable, then test every required bit.",
        related=("exam_debounce_tick", "exam_events_take"),
    ),
    "exam_timer_config_ticks": d(
        "Configure Timer0..Timer3 MR0 from an exact peripheral-clock tick count.",
        params={
            "timer": p("in", "EXAM_TIMER0..EXAM_TIMER3."),
            "ticks": p("in", "MR0 count in timer PCLK ticks; 1..0xFFFFFFFF."),
            "mode": p("in", "EXAM_TIMER_PERIODIC, EXAM_TIMER_ONE_SHOT, or EXAM_TIMER_MODULO_NO_IRQ."),
        },
        returns="EXAM_OK; EXAM_BAD_ARGUMENT for invalid timer/mode; EXAM_OUT_OF_RANGE when ticks is zero.",
        preconditions="Call exam_init() first and keep one matching TIMERn_IRQHandler when the selected mode enables MR0 interrupts.",
        side_effects="Powers the timer, stops and resets it, selects timer mode, sets PR=0 and MR0=ticks, clears IR/NVIC pending state, and enables the NVIC source except in modulo-no-IRQ mode. It does not start the timer.",
        context="Foreground configuration. Do not race reconfiguration against another owner of the same timer.",
        example="(void)exam_timer_config_ticks(EXAM_TIMER0, 25000u, EXAM_TIMER_PERIODIC);\nexam_timer_start(EXAM_TIMER0);",
        mistake="Forgetting exam_timer_start() or assuming ticks use the CPU clock instead of the timer's PCLK.",
        exam_note="Prefer ms or Hz helpers unless the question gives an exact tick count.",
        related=("exam_timer_config_ms", "exam_timer_config_hz", "exam_timer_start", "exam_timer_ack"),
    ),
    "exam_timer_config_ms": d(
        "Configure Timer0..Timer3 MR0 from a millisecond period using that timer's actual PCLK.",
        params={
            "timer": p("in", "EXAM_TIMER0..EXAM_TIMER3."),
            "milliseconds": p("in", "Requested period in milliseconds; must be greater than 0 and convert to 1..0xFFFFFFFF ticks."),
            "mode": p("in", "Periodic, one-shot, or modulo-no-IRQ mode."),
        },
        returns="EXAM_OK; EXAM_BAD_ARGUMENT for invalid timer/mode; EXAM_OUT_OF_RANGE for zero or unrepresentable period; EXAM_NOT_READY if the clock cannot be resolved.",
        preconditions="Call exam_init() first. Provide the matching IRQ handler for interrupting modes.",
        side_effects="Rounds the clock conversion to the nearest tick, then performs the same stopped/reset configuration as exam_timer_config_ticks(). It does not start the timer.",
        context="Foreground configuration; one module must own the selected timer.",
        example="if (exam_timer_config_ms(EXAM_TIMER1, 100u, EXAM_TIMER_PERIODIC) == EXAM_OK)\n  exam_timer_start(EXAM_TIMER1);",
        mistake="Configuring 100 ms and expecting the counter to run before calling exam_timer_start().",
        exam_note="This is the default timer helper for periods stated in milliseconds.",
        related=("exam_timer_start", "exam_timer_ack", "exam_timer_config_hz"),
    ),
    "exam_timer_config_hz": d(
        "Configure a Timer0..Timer3 periodic interval from a requested frequency.",
        params={
            "timer": p("in", "EXAM_TIMER0..EXAM_TIMER3."),
            "hertz": p("in", "Requested events per second; 1..timer PCLK."),
            "mode": p("in", "Periodic, one-shot, or modulo-no-IRQ mode."),
        },
        returns="EXAM_OK; EXAM_BAD_ARGUMENT for invalid timer/mode; EXAM_OUT_OF_RANGE for zero, above-PCLK, or unrepresentable values; EXAM_NOT_READY if the clock cannot be resolved.",
        preconditions="Call exam_init() first and provide the matching handler for interrupting modes.",
        side_effects="Rounds PCLK/hertz to the nearest tick and leaves the selected timer configured but stopped.",
        context="Foreground configuration only.",
        example="(void)exam_timer_config_hz(EXAM_TIMER2, 1000u, EXAM_TIMER_PERIODIC);\nexam_timer_start(EXAM_TIMER2);",
        mistake="Passing a period such as 10 when the parameter means 10 events per second.",
        exam_note="Use for sample rates and waveform update frequencies stated in Hz.",
        related=("exam_timer_config_ms", "exam_timer_start"),
    ),
    "exam_timer_start": d(
        "Start a previously configured hardware timer.",
        params={"timer": p("in", "EXAM_TIMER0..EXAM_TIMER3; invalid values are ignored.")},
        returns="No value.",
        preconditions="Successfully configure the same timer first.",
        side_effects="Writes TCR=1 for the selected timer; it does not reset TC first.",
        context="Start last, after shared state and interrupt ownership are ready.",
        example="exam_timer_start(EXAM_TIMER0);",
        mistake="Starting before configuration or expecting start to reset an old counter value.",
        exam_note="Use exam_timer_reset() explicitly when a fresh zero origin is required after prior use.",
        related=("exam_timer_stop", "exam_timer_reset", "exam_timer_is_running"),
    ),
    "exam_timer_stop": d(
        "Stop one hardware timer without clearing its counter.",
        params={"timer": p("in", "EXAM_TIMER0..EXAM_TIMER3; invalid values are ignored.")},
        returns="No value.",
        preconditions="None beyond a valid timer selection.",
        side_effects="Writes TCR=0; TC retains its current value.",
        context="Bounded register write; coordinate with the timer's single owner.",
        example="exam_timer_stop(EXAM_TIMER0);\nuint32_t elapsed = exam_timer_read(EXAM_TIMER0);",
        mistake="Assuming stop also resets TC to zero.",
        exam_note="Stop first when taking a stable final interval measurement.",
        related=("exam_timer_start", "exam_timer_reset", "exam_timer_read"),
    ),
    "exam_timer_reset": d(
        "Reset a timer counter to zero and leave it stopped.",
        params={"timer": p("in", "EXAM_TIMER0..EXAM_TIMER3; invalid values are ignored.")},
        returns="No value.",
        preconditions="The timer may be configured or unconfigured, but must be a valid timer enum.",
        side_effects="Pulses the reset bit through TCR=2 then writes TCR=0.",
        context="Bounded register operation; it does not acknowledge IR flags.",
        example="exam_timer_reset(EXAM_TIMER1);\nexam_timer_start(EXAM_TIMER1);",
        mistake="Expecting the timer to resume automatically after reset.",
        exam_note="Reset, then start, when measuring a new interval with the same configuration.",
        related=("exam_timer_start", "exam_timer_ack"),
    ),
    "exam_timer_read": d(
        "Read the current TC count from one hardware timer.",
        params={"timer": p("in", "EXAM_TIMER0..EXAM_TIMER3.")},
        returns="Current 32-bit TC value, or 0 for an invalid timer.",
        preconditions="Configure/start the timer when a meaningful elapsed value is required.",
        side_effects="None.",
        context="A single register read. The counter may advance immediately after the value is read.",
        example="uint32_t now = exam_timer_read(EXAM_TIMER3);",
        mistake="Interpreting TC directly as milliseconds when PR=0 means it counts PCLK ticks.",
        exam_note="Convert using the selected timer's clock when the paper asks for physical time.",
        related=("exam_timer_stop", "exam_timer_is_running"),
    ),
    "exam_timer_ack": d(
        "Snapshot and clear all active Timer match/capture interrupt flags.",
        params={"timer": p("in", "EXAM_TIMER0..EXAM_TIMER3.")},
        returns="Bits 0..5 from IR before clearing: MR0, MR1, MR2, MR3, CR0, and CR1; returns 0 for invalid timer or no pending source.",
        preconditions="Call from the selected timer's single IRQ handler.",
        side_effects="Clears every returned IR bit by writing the saved mask back to IR.",
        context="IRQ-oriented and bounded. Save the return value once, then test all enabled sources.",
        example="uint32_t pending = exam_timer_ack(EXAM_TIMER0);\nif ((pending & (1u << 0)) != 0u) { /* MR0 work */ }",
        mistake="Calling it separately for MR0 and MR1; the first call clears both and the second sees zero.",
        exam_note="Acknowledge first, then publish a small event or perform the short required action.",
        related=("exam_timer_config_ticks", "exam_events_set"),
    ),
    "exam_timer_is_running": d(
        "Test the enable bit of one hardware timer.",
        params={"timer": p("in", "EXAM_TIMER0..EXAM_TIMER3.")},
        returns="1 when TCR bit 0 is set; 0 when stopped or timer is invalid.",
        preconditions="None.",
        side_effects="None.",
        context="Single bounded register read.",
        example="if (!exam_timer_is_running(EXAM_TIMER0)) exam_timer_start(EXAM_TIMER0);",
        mistake="Using this result to infer that the timer was configured correctly or that an IRQ is enabled.",
        exam_note="It answers only whether the counter enable bit is set.",
        related=("exam_timer_start", "exam_timer_stop"),
    ),
    "exam_systick_config_ticks": d(
        "Configure and immediately start SysTick with an exact core-clock tick period.",
        params={"ticks": p("in", "Period in core-clock ticks, 1..0x01000000 inclusive.")},
        returns="EXAM_OK or EXAM_OUT_OF_RANGE.",
        preconditions="Provide exactly one SysTick_Handler and initialize shared state before calling.",
        side_effects="Stops SysTick, writes LOAD=ticks-1, clears VAL, then enables core-clock counting and its interrupt immediately.",
        context="Foreground configuration. SysTick exception entry clears its pending condition automatically; there is no API acknowledgement call.",
        example="(void)exam_systick_config_ticks(SystemFrequency / 1000u);",
        mistake="Calling a nonexistent acknowledge helper or forgetting that configuration starts SysTick immediately.",
        exam_note="Use for compact periodic scheduling when the 24-bit reload limit is sufficient.",
        related=("exam_systick_config_ms", "exam_systick_stop", "exam_debounce_tick"),
    ),
    "exam_systick_config_ms": d(
        "Configure and immediately start SysTick from a millisecond period.",
        params={"milliseconds": p("in", "Period in milliseconds; must be greater than 0 and fit the 24-bit SysTick reload range after conversion.")},
        returns="EXAM_OK or EXAM_OUT_OF_RANGE.",
        preconditions="Call exam_init() first and provide the single SysTick_Handler.",
        side_effects="Rounds SystemFrequency*milliseconds/1000 to ticks and starts SysTick immediately.",
        context="Foreground configuration; handler acknowledgement is automatic.",
        example="if (exam_systick_config_ms(10u) != EXAM_OK) { /* period too large */ }",
        mistake="Calling a separate start function; none exists because successful configuration already starts it.",
        exam_note="A 10 ms tick pairs naturally with exam_debounce_config(10, confirmation_ms).",
        related=("exam_systick_config_ticks", "exam_systick_stop", "exam_debounce_config"),
    ),
    "exam_systick_stop": d(
        "Disable SysTick counting and its interrupt.",
        returns="No value.",
        preconditions="None.",
        side_effects="Writes SysTick->CTRL=0; LOAD remains programmed but inactive.",
        context="Bounded register write.",
        example="exam_systick_stop();",
        mistake="Stopping SysTick when another feature, such as debounce, still depends on its ticks.",
        exam_note="Keep one owner for the shared SysTick resource.",
        related=("exam_systick_config_ms",),
    ),
    "exam_rit_config_ticks": d(
        "Configure RIT with an exact tick count and leave it stopped.",
        params={"ticks": p("in", "RIT compare interval in ticks; 1..0xFFFFFFFF.")},
        returns="EXAM_OK or EXAM_OUT_OF_RANGE when ticks is zero.",
        preconditions="Call exam_init() first and keep exactly one RIT_IRQHandler.",
        side_effects="Calls the professor init_RIT(ticks) helper. Configuration does not enable RIT.",
        context="Foreground setup; call exam_rit_start() after state and handler ownership are ready.",
        example="(void)exam_rit_config_ticks(SystemFrequency / 100u);\nexam_rit_start();",
        mistake="Expecting configuration to start the RIT interrupt stream.",
        exam_note="Prefer exam_rit_config_ms() when the required interval is stated in milliseconds.",
        related=("exam_rit_start", "exam_rit_ack", "exam_rit_config_ms"),
    ),
    "exam_rit_config_ms": d(
        "Configure RIT from a millisecond interval and leave it stopped.",
        params={"milliseconds": p("in", "Period in milliseconds; must convert to 1..0xFFFFFFFF SystemFrequency ticks.")},
        returns="EXAM_OK or EXAM_OUT_OF_RANGE for zero or an unrepresentable interval.",
        preconditions="Call exam_init() first and provide the one RIT_IRQHandler.",
        side_effects="Rounds SystemFrequency*milliseconds/1000 and delegates to exam_rit_config_ticks(); it does not start RIT.",
        context="Foreground configuration.",
        example="(void)exam_rit_config_ms(10u);\nexam_rit_start();",
        mistake="Confusing RIT configuration with SysTick configuration; RIT requires an explicit start.",
        exam_note="Useful as an independent periodic source for joystick polling or debounce.",
        related=("exam_rit_start", "exam_debounce_tick", "exam_joystick_read"),
    ),
    "exam_rit_start": d(
        "Enable a previously configured RIT.",
        returns="No value.",
        preconditions="Successfully call one RIT configuration helper first.",
        side_effects="Calls enable_RIT().",
        context="Start after the RIT handler and shared state are ready.",
        example="exam_rit_start();",
        mistake="Starting before configuration or allowing two features to reconfigure the same RIT.",
        exam_note="RIT is a single shared peripheral; assign it one timing responsibility.",
        related=("exam_rit_stop", "exam_rit_reset", "exam_rit_ack"),
    ),
    "exam_rit_stop": d(
        "Disable RIT without changing its documented configuration.",
        returns="No value.",
        preconditions="None.",
        side_effects="Calls disable_RIT().",
        context="Bounded peripheral-control call.",
        example="exam_rit_stop();",
        mistake="Stopping RIT while debounce or joystick sampling still depends on it.",
        exam_note="Stop only when every consumer of that tick source is finished.",
        related=("exam_rit_start", "exam_rit_reset"),
    ),
    "exam_rit_reset": d(
        "Reset the RIT counter through the professor driver.",
        returns="No value.",
        preconditions="RIT should already be configured when its compare interval must remain meaningful.",
        side_effects="Calls reset_RIT().",
        context="Bounded peripheral-control call; it is distinct from interrupt acknowledgement.",
        example="exam_rit_reset();",
        mistake="Using reset instead of exam_rit_ack() inside RIT_IRQHandler.",
        exam_note="Use acknowledgement for every IRQ; use reset only when the question needs a new timing origin.",
        related=("exam_rit_ack", "exam_rit_start"),
    ),
    "exam_rit_ack": d(
        "Acknowledge the active RIT interrupt.",
        returns="No value.",
        preconditions="Call from the single RIT_IRQHandler.",
        side_effects="Sets RICTRL bit 0 to clear the interrupt flag.",
        context="IRQ-only in normal use; call before returning from the handler.",
        example="void RIT_IRQHandler(void) { exam_rit_ack(); exam_debounce_tick(); }",
        mistake="Omitting acknowledgement and immediately re-entering the handler.",
        exam_note="Acknowledge first, then perform only bounded tick work.",
        related=("exam_rit_config_ms", "exam_debounce_tick"),
    ),
    "exam_joystick_init": d(
        "Configure P1.25..P1.29 as unmasked GPIO inputs for the five-way joystick.",
        returns="No value.",
        preconditions="Call exam_init() first.",
        side_effects="Calls joystick_init(), selects GPIO function and default pin mode, sets input direction, and clears the FIO mask for all five controls.",
        context="Foreground initialization only.",
        example="exam_joystick_init();\nuint32_t previous = exam_joystick_read();",
        mistake="Leaving FIO pins masked, which makes inversion look like every control is pressed.",
        exam_note="Initialize once, then sample periodically if the question needs press edges.",
        related=("exam_joystick_read", "exam_joystick_pressed_edges"),
    ),
    "exam_joystick_read": d(
        "Return the current pressed-state mask for all five active-low joystick controls.",
        returns="Bits EXAM_JOY_SELECT, DOWN, LEFT, RIGHT, and UP; a set bit means currently pressed. The API supports all 8 directions as combinations of four direction bits, plus a separate centre SELECT press. Diagonals are UP | LEFT, UP | RIGHT, DOWN | LEFT, and DOWN | RIGHT (use the EXAM_JOY_ prefix for each flag). There are no separate diagonal constants and no four-direction restriction in the API. Both inputs must be activated by the board or simulator. Follow the exam question: implement four directions when it asks for four, and diagonals when required.",
        preconditions="Call exam_joystick_init() first.",
        side_effects="None.",
        context="Single bounded GPIO read; it returns levels, not debounced events.",
        example="uint32_t current = exam_joystick_read();\nuint32_t diagonal = EXAM_JOY_UP | EXAM_JOY_RIGHT;\nif ((current & diagonal) == diagonal) {\n    /* UP and RIGHT are both held. */\n}",
        mistake="Inverting the returned mask again even though the helper already converts active-low input to pressed=1.",
        exam_note="Test the current held-state mask for a diagonal; the two controls may become pressed in different samples, so requiring both pressed-edge bits together can miss it. A held-state test remains true while held; implement one-action or repeat behavior separately as required by the paper.",
        related=("exam_joystick_pressed_edges",),
    ),
    "exam_joystick_pressed_edges": d(
        "Derive controls that changed from released to pressed between two joystick samples.",
        params={
            "previous": p("in", "Earlier pressed-state mask; bits outside the five joystick bits are ignored."),
            "current": p("in", "New pressed-state mask; bits outside the five joystick bits are ignored."),
        },
        returns="current & ~previous limited to the five EXAM_JOY_* bits.",
        preconditions="Supply successive values returned by exam_joystick_read().",
        side_effects="None.",
        context="Pure bounded computation; it does not store history or implement key repeat.",
        example="uint32_t current = exam_joystick_read();\nuint32_t pressed = exam_joystick_pressed_edges(previous, current);\nprevious = current;",
        mistake="Reversing previous and current or forgetting to update previous after each sample.",
        exam_note="The question owns sampling rate, debounce, prolonged-pressure, and repeat policy.",
        related=("exam_joystick_read", "exam_rit_config_ms"),
    ),
    "exam_adc_init": d(
        "Initialize ADC channel 5 on P1.31 and clear the API's cached result state.",
        returns="No value.",
        preconditions="Call exam_init() first and keep exactly one ADC_IRQHandler.",
        side_effects="Clears cached ADC value/freshness under a critical section, then calls ADC_init().",
        context="Foreground initialization only.",
        example="exam_adc_init();\nexam_adc_start();",
        mistake="Reading a result immediately after initialization without starting and completing a conversion.",
        exam_note="The supported simple workflow is one conversion at a time on the potentiometer channel.",
        related=("exam_adc_start", "exam_adc_irq_capture", "exam_adc_take"),
    ),
    "exam_adc_start": d(
        "Start one ADC conversion using the configured channel-5 driver.",
        returns="No value.",
        preconditions="Call exam_adc_init() first and do not start another conversion until the intended workflow is ready for it.",
        side_effects="Calls ADC_start_conversion().",
        context="Normally called from foreground or a bounded scheduler action; completion arrives through ADC_IRQHandler.",
        example="exam_adc_start();",
        mistake="Starting repeatedly without consuming or deliberately replacing the previous fresh sample.",
        exam_note="Use the sequence start -> IRQ capture -> take.",
        related=("exam_adc_irq_capture", "exam_adc_take"),
    ),
    "exam_adc_irq_capture": d(
        "Capture a completed 12-bit ADC result into the API's interrupt-to-main mailbox.",
        returns="No value.",
        preconditions="ADC must be initialized and the call should be made by the single ADC_IRQHandler.",
        side_effects="Reads ADGDR. When DONE bit 31 is set, stores result bits 15:4 and marks the sample fresh; otherwise leaves cached state unchanged.",
        context="IRQ helper; bounded and contains no foreground processing.",
        example="void ADC_IRQHandler(void) { exam_adc_irq_capture(); }",
        mistake="Reading/scaling the ADC in multiple owners or omitting the capture call from the IRQ.",
        exam_note="Capture in the handler and perform display, scaling, or algorithm work in main.",
        related=("exam_adc_start", "exam_adc_take"),
    ),
    "exam_adc_take": d(
        "Atomically take the newest captured ADC sample if one is fresh.",
        params={"result": p("out", "Non-null pointer receiving a 12-bit value 0..4095 when the function returns 1.")},
        returns="1 when a fresh sample was copied and consumed; 0 for null result or when no fresh sample is available.",
        preconditions="Use exam_adc_init(), exam_adc_start(), and exam_adc_irq_capture() to produce samples.",
        side_effects="Clears the fresh flag only when a sample is returned. Does not modify *result when returning 0.",
        context="Foreground consumer; the critical section prevents a torn mailbox update.",
        example="uint16_t sample;\nif (exam_adc_take(&sample)) exam_adc_show_high8(sample);",
        mistake="Using sample after a zero return, when the output variable was not updated.",
        exam_note="Test the return value before processing the result.",
        related=("exam_adc_start", "exam_adc_show_high8"),
    ),
    "exam_adc_show_high8": d(
        "Display ADC result bits 11:4 on the eight LEDs.",
        params={"result": p("in", "ADC result; only the low 12 bits are used before shifting right by four.")},
        returns="No value.",
        preconditions="Initialize LEDs with exam_init(); normally pass a successful exam_adc_take() result.",
        side_effects="Replaces the complete LED display through exam_led_write().",
        context="Keep it in foreground when called as part of the ADC mailbox workflow.",
        example="uint16_t sample;\nif (exam_adc_take(&sample)) exam_adc_show_high8(sample);",
        mistake="Calling it with an uninitialized value when exam_adc_take() returned zero.",
        exam_note="This is the direct 12-bit-to-8-bit display required by many potentiometer exercises.",
        related=("exam_adc_take", "exam_led_write"),
    ),
    "exam_dac_init": d(
        "Configure P0.26 as DAC AOUT with deterministic zero output and fast-mode BIAS=0.",
        returns="No value.",
        preconditions="Call exam_init() first.",
        side_effects="Selects the DAC pin function, sets P0.26 direction, and writes DACR=0.",
        context="Foreground initialization only.",
        example="exam_dac_init();\n(void)exam_dac_write(512);",
        mistake="Writing samples before selecting the DAC function on P0.26.",
        exam_note="Initialize once before waveform or loudspeaker output.",
        related=("exam_dac_write",),
    ),
    "exam_dac_write": d(
        "Write one validated 10-bit DAC sample while preserving DACR.BIAS.",
        params={"sample": p("in", "Signed integer sample in the inclusive range 0..1023.")},
        returns="EXAM_OK or EXAM_OUT_OF_RANGE for a negative value or a value above 1023.",
        preconditions="Call exam_dac_init() first.",
        side_effects="Updates DACR VALUE bits 15:6 and preserves BIAS bit 16.",
        context="Bounded register write suitable for a short periodic waveform-update handler when that is the required owner.",
        example="(void)exam_dac_write(wave[index]);",
        mistake="Passing an 8-bit value without intentionally scaling it, or allowing signed waveform values to go negative.",
        exam_note="Clamp or offset the algorithm's result into 0..1023 before writing.",
        related=("exam_dac_init", "exam_timer_config_hz"),
    ),
    "exam_events_set": d(
        "Atomically OR application-defined bits into the general interrupt-to-main event word.",
        params={"bits": p("in", "One or more question-defined event bits to publish; zero has no effect.")},
        returns="No value.",
        preconditions="Define non-overlapping event masks in question code and call exam_init() before use.",
        side_effects="Adds bits to the private event word without clearing existing events.",
        context="Designed for short IRQ publication; uses a nested-safe PRIMASK save/restore critical section.",
        example="#define EVENT_TICK (1u << 0)\nvoid TIMER0_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER0); exam_events_set(EVENT_TICK); }",
        mistake="Using the same bit for unrelated events or doing long foreground work directly in the IRQ instead.",
        exam_note="Publish state in the handler; take and process it in main.",
        related=("exam_events_take", "exam_critical_enter"),
    ),
    "exam_events_take": d(
        "Atomically obtain and clear selected application event bits.",
        params={"mask": p("in", "Bits to test and consume. Bits outside mask remain pending.")},
        returns="The subset of mask that was pending at the protected snapshot.",
        preconditions="Events are normally produced with exam_events_set().",
        side_effects="Clears exactly the returned selected bits; unrelated event bits are preserved.",
        context="Foreground consumer. New IRQ events published after the snapshot remain pending.",
        example="uint32_t events = exam_events_take(EVENT_TICK | EVENT_ADC);",
        mistake="Taking the same bit in multiple places and making event ownership nondeterministic.",
        exam_note="Take a combined mask once per loop, then branch on the local result.",
        related=("exam_events_set", "exam_button_events_take"),
    ),
    "exam_critical_enter": d(
        "Save PRIMASK, disable maskable interrupts, and issue a data-memory barrier.",
        returns="The previous PRIMASK value that must be passed unchanged to exam_critical_exit().",
        preconditions="Use only for a very short compound access that cannot use a higher-level atomic helper.",
        side_effects="Masks normal interrupts while preserving whether they were already masked.",
        context="No blocking work, loops, peripheral waits, or early returns may occur before the matching exit.",
        example="uint32_t key = exam_critical_enter();\nshared_pair.a = a; shared_pair.b = b;\nexam_critical_exit(key);",
        mistake="Calling __enable_irq() unconditionally afterward or losing the saved PRIMASK on an early return.",
        exam_note="Prefer exam_events_set/take for bit events; use this only for a short multi-step shared update.",
        related=("exam_critical_exit", "exam_events_set"),
    ),
    "exam_critical_exit": d(
        "Restore the exact PRIMASK state saved by exam_critical_enter().",
        params={"saved_primask": p("in", "Unmodified return value from the matching exam_critical_enter() call.")},
        returns="No value.",
        preconditions="Must pair with an earlier exam_critical_enter() on the same control path.",
        side_effects="Issues a data-memory barrier and restores prior interrupt masking, including an already-masked state.",
        context="Call promptly after the protected operations.",
        example="uint32_t key = exam_critical_enter();\n/* bounded shared update */\nexam_critical_exit(key);",
        mistake="Passing 0 instead of the saved value and accidentally enabling interrupts inside an outer critical region.",
        exam_note="Every path after enter must reach exactly one matching exit.",
        related=("exam_critical_enter",),
    ),
    "exam_faults_configure": d(
        "Enable or disable configurable Cortex-M3 faults and the divide-by-zero and unaligned-access traps.",
        params={
            "enable_configurable_faults": p("in", "Nonzero enables MemManage, BusFault, and UsageFault; zero disables them."),
            "trap_divide_by_zero": p("in", "Nonzero sets CCR.DIV_0_TRP; zero clears it."),
            "trap_unaligned": p("in", "Nonzero sets CCR.UNALIGN_TRP; zero clears it."),
        },
        returns="No value.",
        preconditions="If the API must own fault handlers, define EXAM_ENABLE_FAULT_HANDLERS=1 for the complete Keil target, not only in main.c.",
        side_effects="Updates SCB->SHCSR and SCB->CCR, then executes DSB and ISB.",
        context="Foreground setup before deliberately testing faults.",
        example="exam_fault_snapshot_clear();\nexam_faults_configure(1u, 1u, 1u);",
        mistake="Enabling traps without enabling/providing the intended handlers, or defining two owners for the same fault vector.",
        exam_note="Fault capture stops forever for debugger inspection; it is not a recovery mechanism.",
        related=("exam_fault_snapshot_clear", "exam_fault_capture_from_exception"),
    ),
    "exam_fault_snapshot_clear": d(
        "Mark the debugger fault snapshot as invalid before a new test.",
        returns="No value.",
        preconditions="None.",
        side_effects="Atomically writes exam_fault_snapshot_valid=0; stored snapshot words are not erased.",
        context="Foreground setup before triggering a fault.",
        example="exam_fault_snapshot_clear();",
        mistake="Assuming the snapshot structure itself is zero-filled after this call.",
        exam_note="Check the valid flag in the debugger before trusting snapshot fields.",
        related=("exam_faults_configure", "exam_fault_snapshot"),
    ),
    "exam_fault_capture_from_exception": d(
        "Copy the stacked exception frame and Cortex-M3 fault registers into persistent debugger state, then stop forever.",
        params={
            "frame": p("in", "Non-null pointer to the hardware-stacked r0-r3, r12, lr, pc, and xPSR frame."),
            "exc_return": p("in", "LR/EXC_RETURN value supplied by the naked fault wrapper."),
        },
        returns="Does not return.",
        preconditions="Normally reached only through the optional API fault wrappers or an equivalent correct naked assembly wrapper.",
        side_effects="Fills exam_fault_snapshot, sets exam_fault_snapshot_valid after barriers, and loops on __NOP() forever.",
        context="Fault-handler terminal path. Do not call as a normal C function to simulate recovery.",
        example="/* Enable EXAM_ENABLE_FAULT_HANDLERS for the whole target; wrappers call this automatically. */",
        mistake="Calling it with an ordinary local struct or expecting execution to resume.",
        exam_note="Inspect exception_number, frame.pc, CFSR, HFSR, BFAR, and MMFAR in the debugger.",
        related=("exam_faults_configure", "exam_fault_snapshot_clear"),
    ),
    "exam_svc_capture_from_exception": d(
        "Decode the SVC immediate from the instruction before stacked PC and dispatch the service with the stacked frame.",
        params={"frame": p("in/out", "Hardware-stacked exception frame. The dispatcher may alter fields such as r0 to return a service result.")},
        returns="No direct C return; results are communicated through the stacked frame.",
        preconditions="Use the optional API SVC wrapper or an equivalent correct wrapper. The stacked PC must follow a 16-bit SVC instruction.",
        side_effects="Reads byte PC[-2] as the service number and calls exam_svc_dispatch(service_number, frame).",
        context="SVC-handler bridge; keep dispatch work bounded and define one SVC owner.",
        example="/* With EXAM_ENABLE_SVC_HANDLER=1, SVC_Handler calls this bridge automatically. */",
        mistake="Reading the immediate from frame->pc instead of the SVC instruction immediately before it.",
        exam_note="Override exam_svc_dispatch(), not the capture bridge, for question-specific services.",
        related=("exam_svc_dispatch",),
    ),
    "exam_svc_dispatch": d(
        "Provide the weak overridable hook that implements question-specific SVC services.",
        params={
            "service_number": p("in", "8-bit immediate encoded by the SVC instruction."),
            "frame": p("in/out", "Pointer to the hardware-stacked frame; update frame fields to return results."),
        },
        returns="No direct C return.",
        preconditions="Provide one strong definition with the exact prototype when the question uses the API SVC bridge.",
        side_effects="The default weak implementation does nothing. A user override may update the stacked frame or controlled application state.",
        context="Runs in handler mode; keep services bounded and avoid blocking peripheral work.",
        example="void exam_svc_dispatch(uint8_t n, exam_exception_frame_t *f) {\n  if (n == 1u) f->r0 = f->r0 + f->r1;\n}",
        mistake="Defining a mismatched prototype or also defining a competing SVC_Handler.",
        exam_note="Return a scalar service result by writing frame->r0.",
        related=("exam_svc_capture_from_exception",),
    ),
}


from peripheral_helper_docs import extend as _extend_helpers, TIMER_BEHAVIOUR
_extend_helpers(API_DOCS, VALUE_GUIDANCE, SCENARIOS, PUBLIC_CONSTANTS, LEGACY_GAPS, d, p, value)


def render_quick_reference(records: list[dict[str, object]]) -> str:
    """Render the student-readable Markdown from the same records as the portal."""
    lines = [
        "# Official Combined Exam API - Complete Reference",
        "",
        "This document is generated from the current `exam_api.h` declarations and the canonical explanations used by the offline portal. Older templates are not an API authority.",
        "",
        "## Start Here",
        "",
        "```c",
        '#include "exam_api.h"',
        '#include "LPC17xx.h"',
        "",
        "int main(void) {",
        "  exam_init();",
        "  /* Initialize only the peripherals required by the question. */",
        "  for (;;) { __WFI(); }",
        "}",
        "```",
        "",
        "`exam_init()` initializes system and LED support and clears API software state. It does not initialize or start every peripheral.",
        "",
        "## Ownership and Data Flow",
        "",
        "- Use exactly one owner for each peripheral and each IRQ vector.",
        "- Configure shared state first, clear pending hardware state, enable interrupts, and start the time source last.",
        "- In an IRQ: acknowledge the real source, capture a small value or set an event, then return.",
        "- In `main()`: atomically take the event/value and perform longer processing or display work.",
        "- Timer and RIT configuration do not start their counters. Successful SysTick configuration starts SysTick immediately.",
        "- `volatile` provides visibility, not atomic compound updates; use the event or critical-section helpers.",
        "",
        "## How to Read Suggested Values",
        "",
        "- **Observed in reviewed solutions:** the value or pattern appears in a maintained solved exam. Follow the linked exam context; do not reuse a number blindly.",
        "- **Recommended maintained recipe:** a package teaching default, clearly separated from literal past-paper evidence.",
        "- **Safe illustration or API contract:** valid for the current template but not claimed as a past-paper answer.",
        "",
        "## Status Values",
        "",
        "| Value | Meaning |",
        "| --- | --- |",
    ]
    lines.extend(f"| `{name}` | {meaning} |" for name, meaning in STATUS_VALUES)
    lines.extend(["", "## Public Types", "", "| Type | Meaning |", "| --- | --- |"]) 
    lines.extend(f"| `{name}` | {meaning} |" for name, meaning in PUBLIC_TYPES)
    lines.extend(["", "## Public Constants", "", "| Constant | Meaning |", "| --- | --- |"]) 
    lines.extend(f"| `{name}` | {meaning} |" for name, meaning in PUBLIC_CONSTANTS)
    lines.extend(["", "## Public Fault Globals", "", "| Global | Meaning |", "| --- | --- |"]) 
    lines.extend(f"| `{name}` | {meaning} |" for name, meaning in PUBLIC_GLOBALS)
    lines.extend(["", "## Current API Compared with Retired Helpers", ""])
    lines.extend(["", "## Timer operation and ownership", "", "| Call | Counter effect | Configuration and interrupt effect |", "|---|---|---|"])
    lines.extend("| " + " | ".join(row) + " |" for row in TIMER_BEHAVIOUR)
    lines.extend(f"- {item}" for item in LEGACY_GAPS)
    by_group: dict[str, list[dict[str, object]]] = {group: [] for group in GROUP_ORDER}
    for record in records:
        by_group[str(record["group"])].append(record)
    lines.extend(["", "## Complete Function Reference", ""])
    for group in GROUP_ORDER:
        lines.extend([f"### {group}", "", GROUP_DESCRIPTIONS[group], ""])
        for record in by_group[group]:
            name = str(record["title"])
            doc = API_DOCS[name]
            lines.extend([
                f"#### `{name}`", "", str(doc["summary"]), "", "**Declaration**", "", "```c",
                str(record["declaration"]), "```", "",
                f"- **Preconditions:** {doc['preconditions']}",
                f"- **Returns:** {doc['returns']}",
                f"- **Side effects:** {doc['side_effects']}",
                f"- **Call context:** {doc['context']}",
            ])
            params = doc["params"]
            if params:
                lines.extend(["", "| Parameter | Direction | Meaning and valid values |", "| --- | --- | --- |"]) 
                for param_name, param_doc in params.items():
                    lines.append(f"| `{param_name}` | {param_doc['direction']} | {param_doc['description']} |")
            lines.extend(["", "**Typical exam values**", "", "| Suggested value | When to use | Evidence |", "| --- | --- | --- |"]) 
            for item in VALUE_GUIDANCE[name]:
                exam_names = ", ".join(f"`{exam}`" for exam in item["exams"])
                evidence = str(item["basis"]) + (f" — {exam_names}" if exam_names else "")
                lines.append(f"| `{item['value']}` | {item['use']} | {evidence} |")
            matching_scenarios = [scenario for scenario in SCENARIOS if name in scenario["functions"]]
            for scenario in matching_scenarios:
                exam_names = ", ".join(f"`{exam}`" for exam in scenario["exams"])
                evidence = str(scenario["basis"]) + (f" Sources: {exam_names}." if exam_names else "")
                lines.extend(["", f"**Scenario: {scenario['title']}**", "", evidence, "", "```c", str(scenario["code"]), "```"])
            lines.extend(["", "**Minimal example**", "", "```c", str(doc["example"]), "```", "",
                          f"> **Common mistake:** {doc['mistake']}", "", f"**Exam use:** {doc['exam_note']}", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_gap_report() -> str:
    lines = [
        "# Current API Gap Report",
        "",
        "The current header is authoritative. Individual timer matches, prescaler and clock-divider controls, saved match/capture flag tests, and joystick release edges are restored under the current contracts. They use no retired callback signatures.",
        "",
        "Basic timer start/stop/reset, raw joystick reads and press edges, explicit ADC capture/take and DAC writes were already available. They remain the way to combine peripherals with question-owned handlers.",
        "",
        "The following retired conveniences remain absent. Use explicit question code where needed; these names are not current declarations.",
        "",
    ]
    lines.extend(f"- {item}" for item in LEGACY_GAPS)
    lines.extend([
        "",
        "The current header remains the sole interface authority. Use the generated complete reference for all public functions declared in the current header.",
        "",
    ])
    return "\n".join(lines)
