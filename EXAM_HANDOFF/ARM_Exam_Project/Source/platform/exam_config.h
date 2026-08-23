#ifndef EXAM_CONFIG_H
#define EXAM_CONFIG_H

/* A value of 1 transfers the corresponding vector from the built-in handler
 * to the application. Each interrupt vector must have exactly one owner. */
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

/* Scheduler mode supplies the 10 ms button and joystick service. Direct mode
 * exposes RICOMPVAL, RIMASK, RICOUNTER and RICTRL to application code. */
#ifndef EXAM_RIT_DIRECT_MODE
#define EXAM_RIT_DIRECT_MODE 0
#endif

/* Optional startup selection. The default keeps every exam-specific resource
 * unclaimed. Set a flag to 1 when that resource is part of the answer. */
#ifndef EXAM_AUTO_START_BUTTONS
#define EXAM_AUTO_START_BUTTONS 0
#endif
#ifndef EXAM_AUTO_START_JOYSTICK
#define EXAM_AUTO_START_JOYSTICK 0
#endif
#ifndef EXAM_AUTO_START_TIMER0
#define EXAM_AUTO_START_TIMER0 0
#endif
#ifndef EXAM_AUTO_START_TIMER1
#define EXAM_AUTO_START_TIMER1 0
#endif
#ifndef EXAM_AUTO_START_TIMER2
#define EXAM_AUTO_START_TIMER2 0
#endif
#ifndef EXAM_AUTO_START_TIMER3
#define EXAM_AUTO_START_TIMER3 0
#endif
#ifndef EXAM_AUTO_START_RIT
#define EXAM_AUTO_START_RIT 0
#endif
#ifndef EXAM_AUTO_START_SYSTICK
#define EXAM_AUTO_START_SYSTICK 0
#endif
#ifndef EXAM_AUTO_START_ADC
#define EXAM_AUTO_START_ADC 0
#endif
#ifndef EXAM_AUTO_START_DAC
#define EXAM_AUTO_START_DAC 0
#endif

/* Automatically started timers are free-running at the selected PCLK and PR.
 * Periodic matches still belong in the answer because their periods are
 * question-specific. */
#define EXAM_AUTO_TIMER_CLOCK_DIVIDER 4u
#define EXAM_AUTO_TIMER_PRESCALER     0u
#define EXAM_AUTO_SYSTICK_PERIOD_MS   10u

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

/* A value of 1 enables WFI while idle; an enabled interrupt must provide wakeup. */
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

#if EXAM_RIT_DIRECT_MODE && (EXAM_AUTO_START_BUTTONS || EXAM_AUTO_START_JOYSTICK || EXAM_AUTO_START_RIT)
#error RIT direct mode cannot share the RIT scheduler used by automatic input startup
#endif
#if EXAM_AUTO_START_BUTTONS && (EXAM_OWN_EINT0_HANDLER || EXAM_OWN_EINT1_HANDLER || EXAM_OWN_EINT2_HANDLER)
#error Automatic buttons require the template EINT handlers
#endif
#if EXAM_AUTO_START_SYSTICK && EXAM_OWN_SYSTICK_HANDLER
#error Automatic SysTick requires the template SysTick handler
#endif
#if EXAM_AUTO_START_ADC && EXAM_OWN_ADC_HANDLER
#error Automatic ADC startup requires the template ADC handler
#endif

#endif
