#ifndef EXAM_BOARD_H
#define EXAM_BOARD_H

#include <stdint.h>
#include "LPC17xx.h"
#include "exam_config.h"

/*
 * PUBLIC EXAM API
 * ---------------------------------------------------------------
 * Read this header during the exam; you normally do not need to open
 * ultimate_board.c. Every function states its units/valid ranges below.
 * Check a returned status whenever invalid input or resource conflicts are
 * possible. Ignoring BOARD_BUSY is a common cause of timer-helper failures.
 */

typedef enum {
  BOARD_OK = 0,           /* Operation succeeded. */
  BOARD_INVALID = -1,    /* Null pointer or logically invalid combination. */
  BOARD_BUSY = -2,       /* Timer/peripheral is owned by another helper/mode. */
  BOARD_RANGE = -3,      /* Number, reload, rate, channel or ID is out of range. */
  BOARD_NOT_ENABLED = -4,/* The selected helper is unavailable. */
  BOARD_NOT_READY = -5   /* No fresh cached sample/message/input is available. */
} board_status_t;

/* The external buttons are active-low. These enum values also match the
 * EXTMODE/EXTINT bit positions, which helps when reading a fault/debug view. */
typedef enum { BOARD_BUTTON_INT0 = 0, BOARD_BUTTON_KEY1 = 1, BOARD_BUTTON_KEY2 = 2 } board_button_t;
typedef enum { BUTTON_EVENT_PRESS = 1, BUTTON_EVENT_RELEASE = 2 } button_event_t;
typedef void (*button_callback_t)(board_button_t button, button_event_t event);

/* Joystick results are bit masks—not mutually exclusive enum choices.
 * Example: JOYSTICK_UP | JOYSTICK_RIGHT represents a combined press. */
enum {
  JOYSTICK_SELECT = 1u << 0,
  JOYSTICK_DOWN   = 1u << 1,
  JOYSTICK_LEFT   = 1u << 2,
  JOYSTICK_RIGHT  = 1u << 3,
  JOYSTICK_UP     = 1u << 4
};
typedef void (*joystick_callback_t)(uint32_t current_mask, uint32_t changed_mask);

/* Match actions can be ORed independently, exactly like the MCR I/R/S bits. */
enum { TIMER_ACTION_INTERRUPT = 1u, TIMER_ACTION_RESET = 2u, TIMER_ACTION_STOP = 4u };

/* Capture stores TC on an external edge. BOTH means rising and falling. */
typedef enum { CAPTURE_RISING = 1, CAPTURE_FALLING = 2, CAPTURE_BOTH = 3 } timer_capture_edge_t;

/* Counter modes increment TC from the selected CAP input instead of PCLK. */
typedef enum { TIMER_MODE_TIMER = 0, TIMER_MODE_COUNTER_RISING = 1, TIMER_MODE_COUNTER_FALLING = 2, TIMER_MODE_COUNTER_BOTH = 3 } timer_counter_mode_t;

/* External-match actions control MAT outputs when the corresponding MR hits. */
typedef enum { EXT_MATCH_DO_NOTHING = 0, EXT_MATCH_CLEAR = 1, EXT_MATCH_SET = 2, EXT_MATCH_TOGGLE = 3 } timer_external_match_t;
typedef void (*timer_callback_t)(uint8_t timer, uint32_t pending_flags);

/* These values are the LPC1768 ADCR START encodings. Software conversion is
 * started explicitly; every other value starts from the selected signal. */
typedef enum {
  ADC_TRIGGER_SOFTWARE = 0,
  ADC_TRIGGER_P2_10 = 2,
  ADC_TRIGGER_P2_11 = 3,
  ADC_TRIGGER_MAT0_1 = 4,
  ADC_TRIGGER_MAT0_3 = 5,
  ADC_TRIGGER_MAT1_0 = 6,
  ADC_TRIGGER_MAT1_1 = 7
} adc_trigger_t;

typedef struct {
  uint32_t raw;     /* Exact ADGDR value captured by the ISR's one read. */
  uint16_t value;  /* Normalized 12-bit result, 0..4095. */
  uint8_t channel; /* Hardware-reported channel number, 0..7. */
  uint8_t done;    /* DONE bit copied from the hardware result. */
  uint8_t overrun; /* OVERRUN bit: a result was replaced before being read. */
} adc_sample_t;

/* Saved exception context. PC is normally the most useful first value;
 * decode CFSR/HFSR next and trust BFAR/MMFAR only when their valid bits set. */
typedef struct {
  uint32_t exception_number;
  uint32_t exc_return;
  uint32_t r0, r1, r2, r3, r12, lr, pc, xpsr;
  uint32_t cfsr, hfsr, bfar, mmfar;
} fault_snapshot_t;

/* Hardware SVC stack frame. A service may modify r0/r1 to return a value. */
typedef struct { uint32_t r0, r1, r2, r3, r12, lr, pc, xpsr; } svc_context_t;

/* -------------------------------------------------------------------------
 * PLAIN-NUMBER BLACK-BOX SHORTCUTS
 * -------------------------------------------------------------------------
 * WHEN: use these for an ordinary exam task where the peripheral is a tool,
 * not the subject being tested.  Every numeric input is a normal signed int,
 * so calls such as timer_every_ms(0, 1000, callback) need no `u` suffixes and
 * no casts.  The precise typed APIs below remain available and unchanged.
 *
 * LIMIT: if the paper explicitly asks for MR/MCR/ADCR/register configuration,
 * capture/counter details, or an IRQ implementation, use the precise API or
 * registers because that lower-level work is part of the requested answer. */
board_status_t timer_every_ms(int timer, int milliseconds, timer_callback_t callback);
board_status_t timer_every_hz(int timer, int hertz, timer_callback_t callback);
board_status_t systick_every_ms(int milliseconds);

board_status_t potentiometer_start(void);
board_status_t potentiometer_read(int *value);
board_status_t speaker_write(int value);
board_status_t speaker_write_percent(int percent);

int int0_pressed(void);
int key1_pressed(void);
int key2_pressed(void);
int joystick_up_pressed(void);
int joystick_down_pressed(void);
int joystick_left_pressed(void);
int joystick_right_pressed(void);
int joystick_button_pressed(void);


enum {
  SELF_TEST_LED_API = 1u << 0,
  SELF_TEST_JOYSTICK_IDLE = 1u << 1,
  SELF_TEST_ADC_CLOCK = 1u << 2,
  SELF_TEST_SYSTICK_RANGE = 1u << 3,
  SELF_TEST_DAC_RANGE = 1u << 4
};

/* Call once at the beginning of main. It initializes the system clock, LEDs
 * and fault support. Every other peripheral remains off until requested. */
void board_init(void);

/* Default is a no-op so polling keeps running. CA_IDLE_USE_WFI enables sleep. */
void board_idle(void);

/* LEDs — WHEN: visible state, result display, blink or timed sequence.
 * Use printed numbers 4..11 for *_number APIs; masks use GPIO P2 bits.
 */
board_status_t led_write_number(uint8_t led_number, uint8_t on);
/* WHEN: simplest readable calls for one LED or clearing the whole LED row. */
board_status_t led_on(uint8_t led_number);
board_status_t led_off(uint8_t led_number);
void led_all_off(void);
board_status_t led_write_mask(uint8_t mask);
board_status_t led_toggle(uint8_t led_number);
uint8_t led_read_mask(void);
void led_write8(uint8_t value);

/* INPUTS — WHEN: INT0/KEY1/KEY2 or joystick appears in the statement.
 * Callbacks execute inside an interrupt; save data, set flags and return.
 * Button confirmation defaults to 50 ms; milliseconds must be a 10 ms multiple. */
void buttons_init(button_callback_t callback);
/* WHEN: an exact EINTx handler is required without callback/debounce logic. */
board_status_t button_irq_start(board_button_t button);
void buttons_set_confirmation_ms(uint32_t milliseconds);
uint32_t buttons_pressed_mask(void);
/* WHEN: polling one external button; returns 1 while pressed, otherwise 0. */
uint8_t button_is_pressed(board_button_t button);
void joystick_init(joystick_callback_t callback);
uint32_t joystick_read(void);
/* WHEN: polling one direction or combination; all requested bits must be held. */
uint8_t joystick_is_pressed(uint32_t direction);
uint32_t joystick_first_movement(void);
void joystick_reset_first_movement(void);

/* TIMERS — WHEN: delays, periodic events, pulse measurements/counters or MAT.
 * timer=0..3, match=0..3, capture=0..1; values are peripheral ticks.
 * PR divides the incoming timer clock by PR+1. pending_flags bits 0..3 map
 * to MR0..MR3 and bits 4..5 map to CR0..CR1.
 *
 * WHEN the paper asks you to choose PCLK: divider must be 1, 2, 4 or 8.
 * Call timer_set_clock_divider while stopped; changing a running timer returns
 * BOARD_BUSY. The course default is 4, producing 25 MHz from 100 MHz CCLK.
 *
 * WHEN the paper gives hertz: events_per_cycle is 1 for one periodic callback,
 * 2 when two LED toggles form one blink, or the sample count for a DAC table.
 * Frequency helpers round to the nearest tick and work only in timer mode. */
board_status_t timer_set_clock_divider(uint8_t timer, uint8_t divider);
uint32_t timer_peripheral_clock_hz(uint8_t timer);
board_status_t timer_set_prescaler(uint8_t timer, uint32_t prescaler);
uint32_t timer_counter_clock_hz(uint8_t timer);
board_status_t timer_calculate_match_for_frequency(uint8_t timer, uint32_t frequency_hz,
                                                   uint32_t events_per_cycle, uint32_t *match_value);
board_status_t timer_configure_frequency(uint8_t timer, uint8_t match, uint32_t frequency_hz,
                                         uint32_t events_per_cycle, uint32_t actions);
board_status_t timer_start_periodic_interrupt_hz(uint8_t timer, uint32_t frequency_hz,
                                                 uint32_t events_per_cycle,
                                                 timer_callback_t callback);
/* WHEN: the paper says every N milliseconds; owns MR0 and starts the timer. */
board_status_t timer_start_periodic_interrupt_ms(uint8_t timer, uint32_t period_ms,
                                                 timer_callback_t callback);
uint8_t timer_match_occurred(uint32_t pending_flags, uint8_t match);
uint8_t timer_capture_occurred(uint32_t pending_flags, uint8_t capture);
board_status_t timer_configure_match(uint8_t timer, uint8_t match, uint32_t value, uint32_t actions);
board_status_t timer_configure_capture(uint8_t timer, uint8_t capture, timer_capture_edge_t edge, uint8_t interrupt_enable);
board_status_t timer_read_capture(uint8_t timer, uint8_t capture, uint32_t *value);
board_status_t timer_set_counter_mode(uint8_t timer, timer_counter_mode_t mode, uint8_t capture_input);
board_status_t timer_configure_external_match(uint8_t timer, uint8_t match, timer_external_match_t action, uint8_t initial_state);
board_status_t timer_start(uint8_t timer);
board_status_t timer_stop(uint8_t timer);
board_status_t timer_reset(uint8_t timer);
board_status_t timer_set_callback(uint8_t timer, timer_callback_t callback);
uint32_t timer_read_counter(uint8_t timer);

/* RIT — scheduler and raw access are compile-time exclusive.
 * WHEN normal/debounced input: keep scheduler mode.
 * WHEN direct counter/compare/mask is explicitly requested: use raw mode. */
board_status_t rit_scheduler_start(void);
void rit_scheduler_stop(void);
uint32_t rit_scheduler_ticks(void);
board_status_t rit_raw_configure(uint32_t compare, uint32_t mask, uint8_t clear_on_match);
board_status_t rit_raw_start(void);
void rit_raw_stop(void);
uint32_t rit_raw_read(void);

/* SYSTICK — WHEN: the exercise explicitly names the Cortex system timer.
 * reload is a count in 1..0xFFFFFF, not milliseconds. Configuration always
 * follows stop -> load -> clear current -> enable. CALIB may be imprecise. */
board_status_t systick_configure(uint32_t reload, uint8_t periodic, uint8_t interrupt_enable);
/* WHEN: the paper explicitly names SysTick and gives a period in milliseconds. */
board_status_t systick_start_periodic_ms(uint32_t period_ms);
board_status_t systick_set_clock_source(uint8_t processor_clock);
uint32_t systick_calibration_value(void);
uint8_t systick_has_precise_calibration(void);
uint32_t systick_ticks(void);

/* ADC — WHEN: potentiometer/analog sampling, burst or hardware trigger.
 * Pass the real ADC peripheral clock; CLKDIV is chosen so ADC <=13 MHz.
 * Results come from the ISR cache because reading ADGDR clears DONE. */
board_status_t adc_init(uint8_t channel, uint32_t peripheral_clock_hz);
board_status_t adc_configure_trigger(adc_trigger_t trigger, uint8_t falling_edge);
board_status_t adc_start_conversion(void);
board_status_t adc_start_burst(uint32_t channel_mask);
void adc_stop_burst(void);
board_status_t adc_read_channel(uint8_t channel, adc_sample_t *sample);
/* WHEN: only the 12-bit value is needed; hides the advanced sample structure. */
board_status_t adc_read_value(uint8_t channel, uint16_t *value);
uint32_t adc_clock_hz(void);

/* DAC — WHEN: analog level, speaker tone or sample-table waveform.
 * Values are 10-bit. Update rate must be <=1 MHz. Sample playback claims the
 * selected timer; check BOARD_BUSY. Fit JP2 for the physical-board speaker. */
board_status_t dac_init(void);
board_status_t dac_write(uint16_t value);
void dac_silence(void);
board_status_t dac_validate_update_rate(uint32_t update_hz);
board_status_t dac_play_samples(const uint16_t *samples, uint32_t count, uint32_t update_hz, uint8_t timer);

/* CONCURRENCY — use event flags to move work from IRQs to exam_user_loop().
 * Save the critical_enter return value and pass it unchanged to critical_exit
 * so a function never enables interrupts that were already disabled. */
uint32_t critical_enter(void);
void critical_exit(uint32_t previous_primask);
void event_flags_set(uint32_t flags);
uint32_t event_flags_take(uint32_t mask);

extern volatile fault_snapshot_t fault_snapshot;
extern volatile uint8_t fault_snapshot_valid;
/* fault_traps_configure applies exam_config.h trap choices.
 * Override svc_dispatch in an exam file only when C handles an SVC service. */
void fault_traps_configure(void);
void svc_dispatch(uint8_t service_number, svc_context_t *context);

/* ESCAPE HATCH — use only when a question tests a register not wrapped above.
 * Valid names are documented in ultimate_board.c; cast to the LPC type before
 * dereferencing. Prefer typed APIs for ordinary work. */
void *board_direct_register(const char *name);
void exam_user_10ms_hook(void);
uint32_t board_self_test_run(void);

#endif
