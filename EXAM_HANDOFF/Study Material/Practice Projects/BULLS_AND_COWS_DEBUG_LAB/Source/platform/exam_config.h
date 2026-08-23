#ifndef EXAM_CONFIG_H
#define EXAM_CONFIG_H

/*
 * Normal rule: leave this file unchanged.
 *
 * Change one ownership switch to 1 only when the question explicitly asks
 * you to write that exact interrupt handler. This removes the matching
 * built-in handler, so your handler in exam_user.c becomes the only owner.
 */
#ifndef EXAM_OWN_TIMER0_HANDLER
#define EXAM_OWN_TIMER0_HANDLER 0
#endif
#ifndef EXAM_OWN_TIMER1_HANDLER
#define EXAM_OWN_TIMER1_HANDLER 0
#endif
#ifndef EXAM_OWN_TIMER2_HANDLER
#define EXAM_OWN_TIMER2_HANDLER 0
#endif
#ifndef EXAM_OWN_TIMER3_HANDLER
#define EXAM_OWN_TIMER3_HANDLER 0
#endif
#ifndef EXAM_OWN_RIT_HANDLER
#define EXAM_OWN_RIT_HANDLER 0
#endif
#ifndef EXAM_OWN_SYSTICK_HANDLER
#define EXAM_OWN_SYSTICK_HANDLER 0
#endif
#ifndef EXAM_OWN_ADC_HANDLER
#define EXAM_OWN_ADC_HANDLER 0
#endif
#ifndef EXAM_OWN_EINT0_HANDLER
#define EXAM_OWN_EINT0_HANDLER 0
#endif
#ifndef EXAM_OWN_EINT1_HANDLER
#define EXAM_OWN_EINT1_HANDLER 0
#endif
#ifndef EXAM_OWN_EINT2_HANDLER
#define EXAM_OWN_EINT2_HANDLER 0
#endif
#ifndef EXAM_OWN_SVC_HANDLER
#define EXAM_OWN_SVC_HANDLER 0
#endif

/*
 * The default RIT setting supplies the 10 ms service used by confirmed
 * button input and joystick checks. Set EXAM_RIT_DIRECT_MODE to 1 only when
 * the question asks you to program RICOMPVAL, RIMASK, RICOUNTER or RICTRL.
 */
#ifndef EXAM_RIT_DIRECT_MODE
#define EXAM_RIT_DIRECT_MODE 0
#endif

#define RIT_SCHEDULER 1
#define RIT_RAW       2
#if EXAM_RIT_DIRECT_MODE
#define CA_RIT_MODE RIT_RAW
#else
#define CA_RIT_MODE RIT_SCHEDULER
#endif

/* Internal limits and defaults. Units are written in each name. */
#define CA_ENABLE_LEDS       1
#define CA_ENABLE_BUTTONS    1
#define CA_ENABLE_JOYSTICK   1
#define CA_ENABLE_ADC        1
#define CA_ENABLE_DAC        1
#define CA_RIT_TICK_MS       10u
#define CA_BUTTON_CONFIRM_MS 50u
#define CA_JOYSTICK_POLL_MS  50u
#define CA_ADC_MAX_CLOCK_HZ  13000000u
#define CA_DAC_MAX_UPDATE_HZ 1000000u

/* Keep foreground polling alive by default. Set to 1 only when the answer
 * deliberately wants WFI and has an enabled interrupt that can wake it. */
#ifndef CA_IDLE_USE_WFI
#define CA_IDLE_USE_WFI 0
#endif

#ifndef CA_TRAP_DIVIDE_BY_ZERO
#define CA_TRAP_DIVIDE_BY_ZERO 0
#endif
#ifndef CA_TRAP_UNALIGNED
#define CA_TRAP_UNALIGNED 0
#endif
#ifndef CA_ENABLE_CONFIGURABLE_FAULTS
#define CA_ENABLE_CONFIGURABLE_FAULTS 1
#endif

#if (CA_BUTTON_CONFIRM_MS % CA_RIT_TICK_MS) != 0
#error CA_BUTTON_CONFIRM_MS must be a multiple of CA_RIT_TICK_MS
#endif

#endif
