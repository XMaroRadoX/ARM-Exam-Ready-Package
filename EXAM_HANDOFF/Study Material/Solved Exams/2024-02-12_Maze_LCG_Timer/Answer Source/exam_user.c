/*
 * ========================================================================
 * 1_WRITE_C_HERE.c
 * This is the C file you normally edit during the exam.
 * ========================================================================
 *
 * The peripheral drivers are already linked as a library. Put calls in this
 * order: prototypes, shared variables, one-time setup, foreground loop, then
 * short callbacks. See Documentation/PERIPHERAL_RECIPES.md for complete
 * copyable combinations. Do not copy driver source into this file.
 */
#include "exam_user.h"

/* STEP 1: declare every assembly function that C calls. */
extern uint32_t exam_asm_example(uint32_t value);

/* STEP 2: shared interrupt/main data. Interrupt-written values are volatile. */
static volatile exam_button_t last_button;
static volatile uint32_t last_joystick;
static volatile uint32_t last_timer_flags;

/* STEP 3: one-time setup. Uncomment only what the question needs. */
void exam_user_init(void)
{
  /* External buttons with 50 ms confirmation:
   * exam_buttons_start(exam_button_event);
   */

  /* Joystick changes and first movement:
   * exam_joystick_start(exam_joystick_event);
   * exam_joystick_reset_first();
   */

  /* Timer 0 interrupt every 1000 ms:
   * exam_timer_every_ms(0, 1000, exam_timer_event);
   */

  /* Free-running Timer 1:
   * exam_timer_prescaler(1, 0);
   * exam_timer_reset(1);
   * exam_timer_start(1);
   */

  /* Potentiometer (fit JP12):
   * exam_pot_start();
   */

  /* Analog output/speaker (fit JP2):
   * exam_dac_percent(50);
   */

  /* Quick assembly connection check. Remove it before the real solution:
   * exam_led_write((uint8_t)exam_asm_example(41u));
   */
}

/* STEP 4: repeated foreground work. */
void exam_user_loop(void)
{
  uint32_t pending = exam_events_take(0xFFFFFFFFu);

  if (pending & EXAM_EVENT_BUTTON) {
    /* Example: if (last_button == EXAM_BUTTON_INT0) exam_led_toggle(4u); */
    (void)last_button;
  }
  if (pending & EXAM_EVENT_JOYSTICK) {
    /* Test masks with &: more than one direction may be held. */
    (void)last_joystick;
  }
  if (pending & EXAM_EVENT_TIMER) {
    /* Match flags are bits 0..3; capture flags are bits 4..5. */
    (void)last_timer_flags;
  }
}

void exam_button_event(exam_button_t button, exam_button_event_t event)
{
  if (event == EXAM_PRESS) {
    last_button = button;
    exam_events_set(EXAM_EVENT_BUTTON);
  }
}

void exam_joystick_event(uint32_t current, uint32_t changed)
{
  (void)changed;
  last_joystick = current;
  exam_events_set(EXAM_EVENT_JOYSTICK);
}

void exam_timer_event(uint8_t timer, uint32_t flags)
{
  (void)timer;
  last_timer_flags = flags;
  exam_events_set(EXAM_EVENT_TIMER);
}

/* Called by the 10 ms scheduler. Leave empty unless you need a tiny task. */
void exam_user_10ms_hook(void)
{
}

/*
 * EXACT HANDLER SHAPES
 * --------------------
 * Set the matching EXAM_OWN_*_HANDLER switch to 1 before adding a handler.
 * Clear only the flags that were pending. Hardware flags are usually W1C.
 *
 * void TIMER0_IRQHandler(void)
 * {
 *   uint32_t pending = LPC_TIM0->IR;
 *   LPC_TIM0->IR = pending;
 *   // short required action
 * }
 *
 * void EINT0_IRQHandler(void)
 * {
 *   LPC_SC->EXTINT = 1u;
 *   // short required action
 * }
 */
