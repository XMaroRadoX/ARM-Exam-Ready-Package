#ifndef __EXAM_API_H
#define __EXAM_API_H

#include <stdint.h>

/*
 * Core exception ownership is opt-in. Define either symbol as 1 for the
 * complete Keil target, not only in main.c. Disabled by default so a question
 * can provide its own handlers without duplicate symbols.
 */
#ifndef EXAM_ENABLE_FAULT_HANDLERS
#define EXAM_ENABLE_FAULT_HANDLERS 0
#endif

#ifndef EXAM_ENABLE_SVC_HANDLER
#define EXAM_ENABLE_SVC_HANDLER 0
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
  EXAM_OK = 0,
  EXAM_BAD_ARGUMENT,
  EXAM_OUT_OF_RANGE,
  EXAM_NOT_READY
} exam_status_t;

typedef enum {
  EXAM_BUTTON_INT0 = 0,
  EXAM_BUTTON_KEY1,
  EXAM_BUTTON_KEY2
} exam_button_t;

typedef enum {
  EXAM_TIMER0 = 0,
  EXAM_TIMER1,
  EXAM_TIMER2,
  EXAM_TIMER3
} exam_timer_t;

typedef enum {
  EXAM_TIMER_PERIODIC = 0,
  EXAM_TIMER_ONE_SHOT = 1,
  /* Reset at MR0 without an MR0 interrupt: a modulo counter. */
  EXAM_TIMER_MODULO_NO_IRQ = 2,
  /* Compatibility alias; this is not a true 32-bit free-running counter. */
  EXAM_TIMER_FREE_RUNNING = EXAM_TIMER_MODULO_NO_IRQ
} exam_timer_mode_t;

/* Hardware frame automatically stacked by Cortex-M3 on exception entry. */
typedef struct {
  uint32_t r0;
  uint32_t r1;
  uint32_t r2;
  uint32_t r3;
  uint32_t r12;
  uint32_t lr;
  uint32_t pc;
  uint32_t xpsr;
} exam_exception_frame_t;

/* Persistent debugger-readable state captured before an enabled fault stops. */
typedef struct {
  uint32_t exception_number;
  uint32_t exc_return;
  exam_exception_frame_t frame;
  uint32_t cfsr;
  uint32_t hfsr;
  uint32_t dfsr;
  uint32_t afsr;
  uint32_t bfar;
  uint32_t mmfar;
} exam_fault_snapshot_t;

#define EXAM_BUTTON_EVENT_INT0 (1u << 0)
#define EXAM_BUTTON_EVENT_KEY1 (1u << 1)
#define EXAM_BUTTON_EVENT_KEY2 (1u << 2)

#define EXAM_JOY_SELECT (1u << 0)
#define EXAM_JOY_DOWN   (1u << 1)
#define EXAM_JOY_LEFT   (1u << 2)
#define EXAM_JOY_RIGHT  (1u << 3)
#define EXAM_JOY_UP     (1u << 4)

/* Core */
void exam_init(void);

/* Single-LED helpers accept physical board labels 4..11 (LD4..LD11).
 * Board label n maps to GPIO P2.(11 - n); invalid labels leave LEDs unchanged.
 * Numbering change: older exam_ calls used indexes 0..7. Migrate to 11 - index.
 * Low-level professor LED_On/LED_Off functions still use indexes 0..7.
 * one_hot returns a status; write/read retain bit 0 -> LD11, bit 7 -> LD4. */
exam_status_t exam_led_on(uint8_t board_label);
exam_status_t exam_led_off(uint8_t board_label);
exam_status_t exam_led_toggle(uint8_t board_label);
exam_status_t exam_led_one_hot(uint8_t board_label);
void exam_led_write(uint8_t value);
uint8_t exam_led_read(void);
void exam_led_clear(void);

/*
 * Buttons and time-source-independent debouncing. Reconfiguration safely
 * restores any EINT pin that was temporarily owned by an active debounce.
 */
void exam_buttons_init(void);
void exam_button_ack(exam_button_t button);
uint8_t exam_button_is_pressed(exam_button_t button);
exam_status_t exam_debounce_config(uint32_t sample_period_ms,
                                   uint32_t confirmation_ms);
exam_status_t exam_debounce_begin(exam_button_t button);
void exam_debounce_tick(void);
uint32_t exam_button_events_take(void);

/*
 * Timer0..Timer3 helpers own MR0, select timer mode, and use PR = 0.
 * Millisecond/hertz helpers calculate from the selected timer's actual PCLK.
 * Configuration stops and resets the timer but does not start it.
 * exam_timer_ack() returns and clears IR bits 0..5:
 * MR0, MR1, MR2, MR3, CR0, CR1.
 */
exam_status_t exam_timer_config_ticks(exam_timer_t timer, uint32_t ticks,
                                      exam_timer_mode_t mode);
exam_status_t exam_timer_config_ms(exam_timer_t timer, uint32_t milliseconds,
                                   exam_timer_mode_t mode);
exam_status_t exam_timer_config_hz(exam_timer_t timer, uint32_t hertz,
                                   exam_timer_mode_t mode);
void exam_timer_start(exam_timer_t timer);
void exam_timer_stop(exam_timer_t timer);
void exam_timer_reset(exam_timer_t timer);
uint32_t exam_timer_read(exam_timer_t timer);
uint32_t exam_timer_ack(exam_timer_t timer);
uint8_t exam_timer_is_running(exam_timer_t timer);

/* SysTick. The safe helpers start SysTick immediately. */
exam_status_t exam_systick_config_ticks(uint32_t ticks);
exam_status_t exam_systick_config_ms(uint32_t milliseconds);
void exam_systick_stop(void);

/* Repetitive Interrupt Timer. Configuration does not start RIT. */
exam_status_t exam_rit_config_ticks(uint32_t ticks);
exam_status_t exam_rit_config_ms(uint32_t milliseconds);
void exam_rit_start(void);
void exam_rit_stop(void);
void exam_rit_reset(void);
void exam_rit_ack(void);

/*
 * Joystick: P1.25..P1.29 are unmasked GPIO inputs. Returned bits are 1 when
 * the active-low control is pressed. Sample periodically for press edges;
 * prolonged-pressure/key-repeat policy remains question code.
 */
void exam_joystick_init(void);
uint32_t exam_joystick_read(void);
uint32_t exam_joystick_pressed_edges(uint32_t previous, uint32_t current);

/*
 * ADC channel 5 / P1.31 potentiometer, one conversion at a time. The IRQ
 * capture accepts ADGDR only when DONE is set; advanced ADC modes are direct.
 */
void exam_adc_init(void);
void exam_adc_start(void);
void exam_adc_irq_capture(void);
uint8_t exam_adc_take(uint16_t *result);
void exam_adc_show_high8(uint16_t result);

/*
 * DAC output on P0.26. Init selects BIAS = 0. Writes accept 0..1023 and
 * preserve DACR.BIAS so question code can select the low-power mode directly.
 */
void exam_dac_init(void);
exam_status_t exam_dac_write(int32_t sample);

/* Small atomic event helper for interrupt-to-main communication. */
void exam_events_set(uint32_t bits);
uint32_t exam_events_take(uint32_t mask);
uint32_t exam_critical_enter(void);
void exam_critical_exit(uint32_t saved_primask);

/*
 * Cortex-M3 faults and SVC. Handlers are emitted only when the corresponding
 * EXAM_ENABLE_* symbol is 1. Otherwise the native startup/question owns them.
 */
extern volatile exam_fault_snapshot_t exam_fault_snapshot;
extern volatile uint8_t exam_fault_snapshot_valid;
void exam_faults_configure(uint8_t enable_configurable_faults,
                           uint8_t trap_divide_by_zero,
                           uint8_t trap_unaligned);
void exam_fault_snapshot_clear(void);
void exam_fault_capture_from_exception(exam_exception_frame_t *frame,
                                       uint32_t exc_return);
void exam_svc_capture_from_exception(exam_exception_frame_t *frame);
void exam_svc_dispatch(uint8_t service_number,
                       exam_exception_frame_t *frame);

#ifdef __cplusplus
}
#endif

#endif
