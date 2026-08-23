#ifndef EXAM_BOARD_H
#define EXAM_BOARD_H

#include <stdint.h>
#include "LPC17xx.h"
#include "exam_config.h"

/* Public board API. Function comments state units, ranges and ownership. */

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

enum {
  AUTO_INIT_BUTTONS = 1u << 0,
  AUTO_INIT_JOYSTICK = 1u << 1,
  AUTO_INIT_TIMER0 = 1u << 2,
  AUTO_INIT_TIMER1 = 1u << 3,
  AUTO_INIT_TIMER2 = 1u << 4,
  AUTO_INIT_TIMER3 = 1u << 5,
  AUTO_INIT_RIT = 1u << 6,
  AUTO_INIT_SYSTICK = 1u << 7,
  AUTO_INIT_ADC = 1u << 8,
  AUTO_INIT_DAC = 1u << 9
};

/* The started mask records successful resources; zero failures means every
 * startup feature selected in exam_config.h succeeded. */
extern volatile uint32_t exam_auto_init_started;
extern volatile uint32_t exam_auto_init_failures;
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

/* Convenience functions with signed integer parameters. Inputs are validated
 * before conversion to the typed driver API. */
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

/* LEDs: numbered functions use board labels 4..11; masks use GPIO P2 bits. */
board_status_t led_write_number(uint8_t led_number, uint8_t on);
board_status_t led_on(uint8_t led_number);
board_status_t led_off(uint8_t led_number);
void led_all_off(void);
board_status_t led_write_mask(uint8_t mask);
board_status_t led_toggle(uint8_t led_number);
uint8_t led_read_mask(void);
void led_write8(uint8_t value);

/* Inputs: callbacks execute inside an interrupt and should remain bounded.
 * Button confirmation defaults to 50 ms; milliseconds must be a 10 ms multiple. */
void buttons_init(button_callback_t callback);
/* Enables one EINT line without callback or debounce processing. */
board_status_t button_irq_start(board_button_t button);
void buttons_set_confirmation_ms(uint32_t milliseconds);
uint32_t buttons_pressed_mask(void);
/* Returns 1 while the selected external button is pressed. */
uint8_t button_is_pressed(board_button_t button);
void joystick_init(joystick_callback_t callback);
uint32_t joystick_read(void);
/* Returns 1 only when every requested joystick direction is held. */
uint8_t joystick_is_pressed(uint32_t direction);
uint32_t joystick_first_movement(void);
void joystick_reset_first_movement(void);

/* Timers: timer=0..3, match=0..3, capture=0..1; values are peripheral ticks.
 * PR divides the incoming timer clock by PR+1. pending_flags bits 0..3 map
 * to MR0..MR3 and bits 4..5 map to CR0..CR1.
 *
 * The PCLK divider must be 1, 2, 4 or 8. Changing the divider while the timer
 * is running returns BOARD_BUSY. The default divider is 4.
 *
 * events_per_cycle is 1 for one callback per cycle, 2 for two toggles per
 * blink cycle, or the number of samples in a DAC waveform table.
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
/* Configures a periodic interrupt in milliseconds, owns MR0 and starts. */
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

/* RIT scheduler and raw access are compile-time exclusive. */
board_status_t rit_scheduler_start(void);
void rit_scheduler_stop(void);
uint32_t rit_scheduler_ticks(void);
board_status_t rit_raw_configure(uint32_t compare, uint32_t mask, uint8_t clear_on_match);
board_status_t rit_raw_start(void);
void rit_raw_stop(void);
uint32_t rit_raw_read(void);

/* SysTick reload is a count in 1..0xFFFFFF, not milliseconds. Configuration
 * follows stop -> load -> clear current -> enable. CALIB may be imprecise. */
board_status_t systick_configure(uint32_t reload, uint8_t periodic, uint8_t interrupt_enable);
/* Converts a millisecond period to a SysTick reload value and starts it. */
board_status_t systick_start_periodic_ms(uint32_t period_ms);
board_status_t systick_set_clock_source(uint8_t processor_clock);
uint32_t systick_calibration_value(void);
uint8_t systick_has_precise_calibration(void);
uint32_t systick_ticks(void);

/* ADC: pass the peripheral clock; CLKDIV is chosen so ADC <=13 MHz.
 * Results come from the ISR cache because reading ADGDR clears DONE. */
board_status_t adc_init(uint8_t channel, uint32_t peripheral_clock_hz);
board_status_t adc_configure_trigger(adc_trigger_t trigger, uint8_t falling_edge);
board_status_t adc_start_conversion(void);
board_status_t adc_start_burst(uint32_t channel_mask);
void adc_stop_burst(void);
board_status_t adc_read_channel(uint8_t channel, adc_sample_t *sample);
/* Returns only the normalized 12-bit result. */
board_status_t adc_read_value(uint8_t channel, uint16_t *value);
uint32_t adc_clock_hz(void);

/* DAC values are 10-bit. Update rate must be <=1 MHz. Sample playback claims the
 * selected timer; check BOARD_BUSY. Fit JP2 for the physical-board speaker. */
board_status_t dac_init(void);
board_status_t dac_write(uint16_t value);
void dac_silence(void);
board_status_t dac_validate_update_rate(uint32_t update_hz);
board_status_t dac_play_samples(const uint16_t *samples, uint32_t count, uint32_t update_hz, uint8_t timer);

/* Concurrency: event flags transfer work from IRQs to exam_user_loop().
 * critical_exit restores the interrupt state returned by critical_enter. */
uint32_t critical_enter(void);
void critical_exit(uint32_t previous_primask);
void event_flags_set(uint32_t flags);
uint32_t event_flags_take(uint32_t mask);

extern volatile fault_snapshot_t fault_snapshot;
extern volatile uint8_t fault_snapshot_valid;
/* fault_traps_configure applies exam_config.h trap settings. */
void fault_traps_configure(void);
void svc_dispatch(uint8_t service_number, svc_context_t *context);

/* Provides access to supported registers not covered by the typed API.
 * Valid names are documented in exam_board.c. */
void *board_direct_register(const char *name);
void exam_user_10ms_hook(void);
uint32_t board_self_test_run(void);

#endif
