# Official Combined Exam API - Complete Reference

This document is generated from the current `exam_api.h` declarations and the canonical explanations used by the offline portal. Older templates are not an API authority.

## Start Here

```c
#include "exam_api.h"
#include "LPC17xx.h"

int main(void) {
  exam_init();
  /* Initialize only the peripherals required by the question. */
  for (;;) { __WFI(); }
}
```

`exam_init()` initializes system and LED support and clears API software state. It does not initialize or start every peripheral.

## Ownership and Data Flow

- Use exactly one owner for each peripheral and each IRQ vector.
- Configure shared state first, clear pending hardware state, enable interrupts, and start the time source last.
- In an IRQ: acknowledge the real source, capture a small value or set an event, then return.
- In `main()`: atomically take the event/value and perform longer processing or display work.
- Timer and RIT configuration do not start their counters. Successful SysTick configuration starts SysTick immediately.
- `volatile` provides visibility, not atomic compound updates; use the event or critical-section helpers.

## How to Read Suggested Values

- **Observed in reviewed solutions:** the value or pattern appears in a maintained solved exam. Follow the linked exam context; do not reuse a number blindly.
- **Recommended maintained recipe:** a package teaching default, clearly separated from literal past-paper evidence.
- **Safe illustration or API contract:** valid for the current template but not claimed as a past-paper answer.

## Status Values

| Value | Meaning |
| --- | --- |
| `EXAM_OK` | The operation completed successfully. |
| `EXAM_BAD_ARGUMENT` | An enum value, pointer-dependent setup, or mode argument is invalid. |
| `EXAM_OUT_OF_RANGE` | A numeric value cannot be represented or accepted by the hardware helper. |
| `EXAM_NOT_READY` | Required configuration or a usable clock value is not available yet. |

## Public Types

| Type | Meaning |
| --- | --- |
| `exam_status_t` | Status returned by validated configuration and output helpers. |
| `exam_button_t` | EXAM_BUTTON_INT0, EXAM_BUTTON_KEY1, or EXAM_BUTTON_KEY2. |
| `exam_timer_t` | EXAM_TIMER0 through EXAM_TIMER3. |
| `exam_timer_mode_t` | Periodic, one-shot, or modulo-without-MR0-interrupt operation. |
| `exam_exception_frame_t` | The eight words automatically stacked by the Cortex-M3 on exception entry. |
| `exam_fault_snapshot_t` | The stacked frame plus Cortex-M3 fault-status registers captured before the fault loop. |

## Public Constants

| Constant | Meaning |
| --- | --- |
| `EXAM_BUTTON_EVENT_INT0` | Bit 0 in the debounced button-event word. |
| `EXAM_BUTTON_EVENT_KEY1` | Bit 1 in the debounced button-event word. |
| `EXAM_BUTTON_EVENT_KEY2` | Bit 2 in the debounced button-event word. |
| `EXAM_JOY_SELECT` | Bit 0 returned by exam_joystick_read(). |
| `EXAM_JOY_DOWN` | Bit 1 returned by exam_joystick_read(). |
| `EXAM_JOY_LEFT` | Bit 2 returned by exam_joystick_read(). |
| `EXAM_JOY_RIGHT` | Bit 3 returned by exam_joystick_read(). |
| `EXAM_JOY_UP` | Bit 4 returned by exam_joystick_read(). |
| `EXAM_ENABLE_FAULT_HANDLERS` | Set to 1 for the complete target to emit the API fault wrappers; default 0. |
| `EXAM_ENABLE_SVC_HANDLER` | Set to 1 for the complete target to emit the API SVC wrapper; default 0. |
| `EXAM_MATCH_INTERRUPT` | Bit 0: request an interrupt on the selected match. |
| `EXAM_MATCH_RESET` | Bit 1: reset TC on the selected match. |
| `EXAM_MATCH_STOP` | Bit 2: stop TC on the selected match. Combine with |; zero disables all three actions. |

## Public Fault Globals

| Global | Meaning |
| --- | --- |
| `exam_fault_snapshot` | Volatile debugger-readable state written by exam_fault_capture_from_exception(). |
| `exam_fault_snapshot_valid` | Set to 1 only after the complete snapshot has been stored. |

## Current API Compared with Retired Helpers


## Timer operation and ownership

| Call | Counter effect | Configuration and interrupt effect |
|---|---|---|
| General timer config_ticks/ms/hz | TC=PC=0; PR=0; stopped | Owns MR0, preserves MR1..3 and capture/output setup; clears IR and NVIC pending. Interrupt modes enable NVIC and assign priority equal to timer number. |
| General timer start | Count from current TC/PC | Retains configuration and pending flags; does not reset. |
| General timer stop | Pause TC/PC | Retains configuration and pending flags; does not disable NVIC. |
| General timer reset | TC=PC=0; stopped | Retains configuration; does not acknowledge IR or disable NVIC. |
| General timer ack | No counter change | Read IR once, clear those hardware flags, return saved bits 0..5. Does not explicitly clear NVIC pending. |
| RIT config | Counter=0; stopped | Select core clock, clear mask and hardware/controller pending, enable interrupt. |
| RIT reset | Counter=0; retains running state | Does not acknowledge the interrupt or change the interval. |
| SysTick config | Clear current count; starts immediately | Set reload and enable core-clock counting and its interrupt. |
- Core conveniences absent: exam_idle, exam_self_test. Use __WFI directly when sleeping is appropriate; the template does not claim a board self-test API.
- Retired LED names absent: exam_led_from_board_label, exam_led_set, exam_leds_bar, exam_leds_clear, exam_leds_fill, exam_leds_read, exam_leds_write.
- Retired button names absent: exam_button_irq_start, exam_button_is_down, exam_button_pressed_edges, exam_button_released_edges, exam_buttons_confirmation_ms, exam_buttons_down, exam_buttons_start.
- Retired joystick names absent: exam_joystick_down, exam_joystick_first, exam_joystick_reset_first, exam_joystick_start. The current API stores no key-repeat policy.
- Retired ADC and potentiometer names absent: exam_adc_read_raw, exam_potentiometer_read_percent, exam_potentiometer_read_raw, exam_potentiometer_start.
- Retired DAC names absent: exam_dac_play, exam_dac_silence, exam_dac_stop, exam_dac_write_percent, exam_dac_write_raw. Playback scheduling belongs to question code.
- Retired RIT and SysTick names absent: exam_rit_ticks, exam_systick_periodic_ms, exam_systick_ticks.
- Retired general-timer names absent: exam_timer_clock_divider, exam_timer_free_running_start, exam_timer_match, exam_timer_periodic_hz, exam_timer_periodic_ms, exam_timer_prescaler.
- The current API has no callback-registration layer. Put question-specific work in the existing IRQ source or publish an event to main.
- EXAM_TIMER_FREE_RUNNING is only a compatibility alias for EXAM_TIMER_MODULO_NO_IRQ, not a true unrestricted 32-bit free-running mode.
- Restored capabilities: individual matches, prescaler and divider controls under the new config_match/set_prescaler/set_clock_divider contracts; pure match/capture predicates; joystick released_edges(previous,current). Callback schedulers remain absent. ADC/DAC existing low-level flow already covers reading/writing; percentage scaling belongs in examples.

## Complete Function Reference

### Core

Initialize the board support and reset the API's shared software state.

#### `exam_init`

Initialize the LPC1768 system clock and LED support, then clear every software flag and cached API state.

**Declaration**

```c
void exam_init(void);
```

- **Preconditions:** Call once near the start of main(), before any other exam_ helper.
- **Returns:** No value.
- **Side effects:** Calls SystemInit() and LED_init(); clears general events, button events, ADC freshness, debounce state, and the fault-snapshot valid flag. It does not initialize or start buttons, timers, SysTick, RIT, joystick, ADC, or DAC.
- **Call context:** Foreground initialization only. It briefly masks interrupts while resetting shared software state.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Once` | First API call in main(); initialize only required peripherals afterward. | Current template contract |

**Scenario: Use three raw button interrupts to select LED states**

Observed structure in the reviewed 2023-09-18 digit-addition solution. Sources: `2023-09-18-q2`.

```c
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  (void)exam_led_on(4u);
  (void)exam_led_off(5u);
}

exam_init();
exam_led_clear();
exam_buttons_init();
```

**Minimal example**

```c
#include "exam_api.h"
#include "LPC17xx.h"

int main(void) {
  exam_init();
  exam_buttons_init();
  for (;;) { __WFI(); }
}
```

> **Common mistake:** Assuming exam_init() starts every peripheral or calling it again after interrupts are active and thereby erasing pending software events.

**Exam use:** Start every API-based answer here, then initialize only the peripherals the question actually uses.

### LEDs

Control the eight board LEDs through the professor-compatible LED driver.

#### `exam_led_on`

Turn on one LED using its printed board label, 4 through 11.

**Declaration**

```c
exam_status_t exam_led_on(uint8_t board_label);
```

- **Preconditions:** exam_init() must have initialized the LED driver.
- **Returns:** EXAM_OK, or EXAM_OUT_OF_RANGE when board_label is outside 4..11; invalid calls leave the display unchanged.
- **Side effects:** Sets one LED bit and preserves the other seven LED states.
- **Call context:** Safe from foreground or a short IRQ; the helper protects the shared LED shadow value with a short critical section.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `board_label` | in | Printed board label 4..11. LD11 maps to P2.0; LD4 maps to P2.7. Other values are rejected without changing the LEDs. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `4, 5, 6, 7, 11` | Physical board labels used by migrated button, timer, and result scenarios. | Observed in reviewed solutions — `2023-09-18-q2`, `2023-02-07-q2` |

**Scenario: Publish a half-second Timer0 event to the foreground**

Observed in the reviewed 2024-02-28 shortest-path solution. Sources: `2024-02-28-q2`.

```c
#define EVENT_HALF_SECOND (1u << 0)

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
}
```

**Scenario: Use three raw button interrupts to select LED states**

Observed structure in the reviewed 2023-09-18 digit-addition solution. Sources: `2023-09-18-q2`.

```c
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  (void)exam_led_on(4u);
  (void)exam_led_off(5u);
}

exam_init();
exam_led_clear();
exam_buttons_init();
```

**Minimal example**

```c
if (exam_led_on(8u) != EXAM_OK) { /* handle invalid board label */ }
```

> **Common mistake:** Using old 0..7 API indexes. Single-LED calls now take labels 4..11; migrate an old index to 11 - index. Values 4..7 have changed meaning.

**Exam use:** Use when the question says to set one LED without disturbing the rest.

#### `exam_led_off`

Turn off one board LED while preserving every other LED.

**Declaration**

```c
exam_status_t exam_led_off(uint8_t board_label);
```

- **Preconditions:** Call exam_init() first.
- **Returns:** EXAM_OK, or EXAM_OUT_OF_RANGE when board_label is outside 4..11; invalid calls leave the display unchanged.
- **Side effects:** Clears the selected bit in the LED output and shadow state.
- **Call context:** Safe from foreground or a short IRQ; uses a bounded critical section.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `board_label` | in | Printed board label 4..11, not a GPIO bit index. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `4, 5, 6, 7` | Clear individual status LEDs without disturbing the rest. | Observed in reviewed solutions — `2023-09-18-q2`, `2023-02-07-q2` |

**Scenario: Use three raw button interrupts to select LED states**

Observed structure in the reviewed 2023-09-18 digit-addition solution. Sources: `2023-09-18-q2`.

```c
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  (void)exam_led_on(4u);
  (void)exam_led_off(5u);
}

exam_init();
exam_led_clear();
exam_buttons_init();
```

**Minimal example**

```c
(void)exam_led_off(8u);
```

> **Common mistake:** Calling exam_led_clear() when only one LED should be turned off.

**Exam use:** Pair with exam_led_on() for explicit state control.

#### `exam_led_toggle`

Invert one LED based on the driver shadow state.

**Declaration**

```c
exam_status_t exam_led_toggle(uint8_t board_label);
```

- **Preconditions:** Call exam_init() first.
- **Returns:** EXAM_OK, or EXAM_OUT_OF_RANGE when board_label is outside 4..11; invalid calls leave the display unchanged.
- **Side effects:** Reads and updates the selected LED bit atomically with respect to interrupt code using the same helper.
- **Call context:** Bounded and suitable for a timer IRQ when toggling is the complete required action.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `board_label` | in | Printed board label 4..11, not a GPIO bit index. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `11` | Simple heartbeat or confirmed-button indicator. | Recommended package recipe |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Minimal example**

```c
if ((pending & 1u) != 0u) { (void)exam_led_toggle(11u); }
```

> **Common mistake:** Reimplementing toggle as separate exam_led_read() and exam_led_write() calls, which creates a read-modify-write race.

**Exam use:** Useful for periodic blink questions; acknowledge the timer before toggling.

#### `exam_led_one_hot`

Show exactly one lit LED selected by its printed board label.

**Declaration**

```c
exam_status_t exam_led_one_hot(uint8_t board_label);
```

- **Preconditions:** Call exam_init() first.
- **Returns:** EXAM_OK, or EXAM_OUT_OF_RANGE when board_label is outside 4..11; invalid calls leave the display unchanged.
- **Side effects:** Replaces the complete eight-bit LED output with 1u << (11u - board_label).
- **Call context:** Bounded call; safe in foreground or a short handler.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `board_label` | in | Printed board label 4..11 of the only LED to light. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `4..11` | Select by the printed board label. A logical position 0..7 converts to label 11 - position. | API range |

**Scenario: Build and preserve a one-hot LED selection**

Safe current-API illustration. Use it when the question represents a selected position on LEDs; the exact position comes from the question logic.

```c
uint8_t previous = exam_led_read();
(void)exam_led_one_hot(8u);  /* Physical LD8; pattern 0x08. */
/* The helper returns a status, not the selected bit mask. */
/* Restore the previous API-controlled pattern when required. */
exam_led_write(previous);
```

**Minimal example**

```c
(void)exam_led_one_hot(8u); /* Only LD8; pattern 0x08. */
```

> **Common mistake:** Passing a bit mask instead of a board label: 0x10 is not LD7. Pass 7 for LD7, or use exam_led_write(0x10u) for its mask.

**Exam use:** Use for moving-dot and selected-position displays.

#### `exam_led_write`

Write the complete eight-bit LED pattern.

**Declaration**

```c
void exam_led_write(uint8_t value);
```

- **Preconditions:** Call exam_init() first.
- **Returns:** No value.
- **Side effects:** Replaces all eight LED states and updates the professor-driver shadow value.
- **Call context:** Uses a short critical section; keep higher-level formatting outside an IRQ.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `value` | in | Eight-bit display mask: bit n controls LD(11 - n). Bit 0 is LD11; bit 7 is LD4. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `0x00` | Clear all LEDs. | Observed in reviewed solutions |
| `0xFF` | Show an error/all-on state. | Observed in reviewed solutions — `2024-02-28-q2`, `2026-06-25-arm1-q2` |
| `sample >> 4` | Map a 12-bit ADC result to eight LEDs. | Observed in reviewed solutions — `2026-02-03-arm1-q2` |

**Scenario: Continuously convert the potentiometer and show its high byte**

Observed in the three reviewed 2026-02-03 ADC solutions. Sources: `2026-02-03-arm1-q2`, `2026-02-03-arm3-q2`.

```c
void ADC_IRQHandler(void) {
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
}
```

**Scenario: Build and preserve a one-hot LED selection**

Safe current-API illustration. Use it when the question represents a selected position on LEDs; the exact position comes from the question logic.

```c
uint8_t previous = exam_led_read();
(void)exam_led_one_hot(8u);  /* Physical LD8; pattern 0x08. */
/* The helper returns a status, not the selected bit mask. */
/* Restore the previous API-controlled pattern when required. */
exam_led_write(previous);
```

**Minimal example**

```c
exam_led_write((uint8_t)(value & 0xFFu));
```

> **Common mistake:** Expecting the call to preserve LEDs whose bits are zero.

**Exam use:** Use when an eight-bit result or ADC high byte must be displayed directly.

#### `exam_led_read`

Read the API's current eight-bit LED shadow value.

**Declaration**

```c
uint8_t exam_led_read(void);
```

- **Preconditions:** Call exam_init() before relying on the returned state.
- **Returns:** The last LED pattern maintained by the LED driver as uint8_t.
- **Side effects:** None; it reads the software shadow, not the physical voltage on the LED pins.
- **Call context:** Safe from foreground or IRQ code; the read is protected by a short critical section.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Returned uint8_t` | Save the current API-controlled LED mask; do not invent a physical input value. | API contract |

**Scenario: Build and preserve a one-hot LED selection**

Safe current-API illustration. Use it when the question represents a selected position on LEDs; the exact position comes from the question logic.

```c
uint8_t previous = exam_led_read();
(void)exam_led_one_hot(8u);  /* Physical LD8; pattern 0x08. */
/* The helper returns a status, not the selected bit mask. */
/* Restore the previous API-controlled pattern when required. */
exam_led_write(previous);
```

**Minimal example**

```c
uint8_t before = exam_led_read();
```

> **Common mistake:** Treating the returned shadow value as an independent hardware input measurement.

**Exam use:** Use to inspect API-controlled LED state, not to build a non-atomic toggle sequence.

#### `exam_led_clear`

Turn off all eight LEDs.

**Declaration**

```c
void exam_led_clear(void);
```

- **Preconditions:** Call exam_init() first.
- **Returns:** No value.
- **Side effects:** Writes the complete LED output value 0.
- **Call context:** Equivalent to exam_led_write(0u) and uses the same bounded critical section.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `No argument` | Start from a known all-off display before showing a result. | Observed throughout reviewed solutions |

**Scenario: Publish a half-second Timer0 event to the foreground**

Observed in the reviewed 2024-02-28 shortest-path solution. Sources: `2024-02-28-q2`.

```c
#define EVENT_HALF_SECOND (1u << 0)

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
}
```

**Scenario: Use three raw button interrupts to select LED states**

Observed structure in the reviewed 2023-09-18 digit-addition solution. Sources: `2023-09-18-q2`.

```c
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  (void)exam_led_on(4u);
  (void)exam_led_off(5u);
}

exam_init();
exam_led_clear();
exam_buttons_init();
```

**Minimal example**

```c
exam_led_clear();
```

> **Common mistake:** Using it when only one selected LED should be cleared.

**Exam use:** Call before presenting a new result when the question requires a blank state.

### Buttons

Use raw external interrupts or the API's time-source-independent debounce state machine.

#### `exam_buttons_init`

Configure INT0, KEY1, and KEY2 as falling-edge external interrupts and reset button/debounce state.

**Declaration**

```c
void exam_buttons_init(void);
```

- **Preconditions:** Call exam_init() first and keep exactly one EINT0, EINT1, and EINT2 handler in the project.
- **Returns:** No value.
- **Side effects:** Clears EXTINT bits 0..2 and pending NVIC state, calls BUTTON_init(), resets debounce state and button events, and enables the button interrupt setup supplied by the template.
- **Call context:** Foreground initialization only; call before waiting for button interrupts.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Once` | Before enabling raw or debounced INT0/KEY1/KEY2 workflows. | Observed throughout button-based solutions |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Scenario: Use three raw button interrupts to select LED states**

Observed structure in the reviewed 2023-09-18 digit-addition solution. Sources: `2023-09-18-q2`.

```c
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  (void)exam_led_on(4u);
  (void)exam_led_off(5u);
}

exam_init();
exam_led_clear();
exam_buttons_init();
```

**Minimal example**

```c
exam_init();
exam_buttons_init();
```

> **Common mistake:** Defining a second EINT handler or assuming initialization also implements the question-specific handler action.

**Exam use:** Choose raw acknowledgement or the debounce workflow in each existing EINT handler.

#### `exam_button_ack`

Acknowledge one LPC1768 external-interrupt button source.

**Declaration**

```c
void exam_button_ack(exam_button_t button);
```

- **Preconditions:** The selected button should have been initialized with exam_buttons_init().
- **Returns:** No value.
- **Side effects:** Writes the selected write-one-to-clear bit in LPC_SC->EXTINT.
- **Call context:** Designed for the matching EINT handler; acknowledge before leaving a raw-button handler.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `button` | in | EXAM_BUTTON_INT0, EXAM_BUTTON_KEY1, or EXAM_BUTTON_KEY2. Invalid values are ignored. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `EXAM_BUTTON_INT0 / KEY1 / KEY2` | Use the enum matching the active EINT0/EINT1/EINT2 handler. | Observed in reviewed solutions — `2023-09-18-q2`, `2024-09-16-q2` |

**Scenario: Use three raw button interrupts to select LED states**

Observed structure in the reviewed 2023-09-18 digit-addition solution. Sources: `2023-09-18-q2`.

```c
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  (void)exam_led_on(4u);
  (void)exam_led_off(5u);
}

exam_init();
exam_led_clear();
exam_buttons_init();
```

**Minimal example**

```c
void EINT0_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_INT0); }
```

> **Common mistake:** Returning from an EINT handler without clearing its EXTINT flag, causing immediate retriggering.

**Exam use:** For debouncing, call exam_debounce_begin() instead; it performs the acknowledgement itself.

#### `exam_button_is_pressed`

Read the current active-low GPIO level of one board button.

**Declaration**

```c
uint8_t exam_button_is_pressed(exam_button_t button);
```

- **Preconditions:** The pin must currently be usable as GPIO; exam_debounce_begin() temporarily establishes this for a debounced press.
- **Returns:** 1 when pressed, 0 when released or when button is invalid.
- **Side effects:** None.
- **Call context:** A single bounded GPIO read. It does not debounce or acknowledge an interrupt.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `button` | in | One valid exam_button_t value. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `1 pressed, 0 released` | Read a level only while the pin is usable as GPIO; it is not an edge event. | API contract |

**Scenario: Use three raw button interrupts to select LED states**

Observed structure in the reviewed 2023-09-18 digit-addition solution. Sources: `2023-09-18-q2`.

```c
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  (void)exam_led_on(4u);
  (void)exam_led_off(5u);
}

exam_init();
exam_led_clear();
exam_buttons_init();
```

**Minimal example**

```c
if (exam_button_is_pressed(EXAM_BUTTON_KEY1)) { /* held now */ }
```

> **Common mistake:** Treating a held level as a one-time press event.

**Exam use:** Use raw levels only when the paper wants level polling; use debounced events for one action per press.

#### `exam_debounce_config`

Set the number of periodic samples required to confirm a button press.

**Declaration**

```c
exam_status_t exam_debounce_config(uint32_t sample_period_ms, uint32_t confirmation_ms);
```

- **Preconditions:** Call exam_init() first. Configure the timer, SysTick, or RIT that will call exam_debounce_tick() at sample_period_ms.
- **Returns:** EXAM_OK; EXAM_BAD_ARGUMENT for either zero duration; EXAM_OUT_OF_RANGE if the rounded sample count cannot fit uint32_t.
- **Side effects:** Clears pending debounced events and cancels/restores every active debounce before installing the new threshold.
- **Call context:** Foreground configuration; do not continuously reconfigure from an IRQ.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `sample_period_ms` | in | Actual interval in milliseconds between calls to exam_debounce_tick(); must be greater than 0. |
| `confirmation_ms` | in | Positive confirmation setting converted to ceil(confirmation_ms/sample_period_ms) consecutive pressed samples. This is a sample-count threshold, not a minimum wall-clock duration. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `10 ms sample, 50 ms confirmation` | Five stable samples; a conservative default for the supplied board buttons. | Recommended maintained recipe, not a literal past-paper constant |
| `10 ms sample, 30 ms confirmation` | Three stable samples when faster response is preferred. | Safe illustrative alternative, not observed in solved exams |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Scenario: Use SysTick instead of RIT for the same debounce interval**

Safe API-derived alternative; not an observed solved-exam combination.

```c
exam_buttons_init();
if (exam_debounce_config(10u, 50u) == EXAM_OK)
  (void)exam_systick_config_ms(10u); /* starts immediately */

void SysTick_Handler(void) {
  exam_debounce_tick(); /* SysTick acknowledgement is automatic */
}
```

**Minimal example**

```c
(void)exam_debounce_config(10u, 30u); /* three stable samples */
```

> **Common mistake:** Passing the confirmation time as the tick period while the real tick uses a different interval.

**Exam use:** The API owns the sample count; your periodic interrupt owns timing. Five samples at10ms confirm roughly40..50ms after the initial edge, depending on sample phase; delayed servicing can extend this. A sampled release immediately rearms, as in the existing flow.

#### `exam_debounce_begin`

Begin debouncing a button after its external interrupt fires.

**Declaration**

```c
exam_status_t exam_debounce_begin(exam_button_t button);
```

- **Preconditions:** Call exam_buttons_init() and exam_debounce_config() first.
- **Returns:** EXAM_OK; EXAM_BAD_ARGUMENT for an invalid button; EXAM_NOT_READY if debounce timing was not configured.
- **Side effects:** Disables the matching EINT NVIC source, changes the pin temporarily to GPIO, acknowledges EXTINT, and starts or preserves the per-button debounce state.
- **Call context:** Call from the matching EINT handler. A periodic handler must then call exam_debounce_tick().

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `button` | in | The button whose EINT handler is currently running. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Matching button enum` | Begin from the corresponding EINT handler, for example KEY1 in EINT1_IRQHandler. | Current template workflow |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Minimal example**

```c
void EINT1_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_KEY1); }
```

> **Common mistake:** Calling exam_button_ack() and then starting a second competing debounce mechanism.

**Exam use:** The interrupt is re-enabled only after exam_debounce_tick() observes release.

#### `exam_debounce_tick`

Advance every active button debounce state by one configured sample interval.

**Declaration**

```c
void exam_debounce_tick(void);
```

- **Preconditions:** exam_debounce_config() must describe the real tick interval; active buttons are created by exam_debounce_begin().
- **Returns:** No value.
- **Side effects:** Records one event after enough stable pressed samples. On release it restores the EINT pin, clears pending state, and re-enables the matching NVIC interrupt.
- **Call context:** Call exactly once per sample from one periodic IRQ source. The loop is bounded over three buttons.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Every 10 ms` | Must exactly match sample_period_ms used by exam_debounce_config. | Recommended maintained recipe |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Scenario: Use SysTick instead of RIT for the same debounce interval**

Safe API-derived alternative; not an observed solved-exam combination.

```c
exam_buttons_init();
if (exam_debounce_config(10u, 50u) == EXAM_OK)
  (void)exam_systick_config_ms(10u); /* starts immediately */

void SysTick_Handler(void) {
  exam_debounce_tick(); /* SysTick acknowledgement is automatic */
}
```

**Minimal example**

```c
void SysTick_Handler(void) { exam_debounce_tick(); }
```

> **Common mistake:** Calling it from multiple timers or at an interval different from sample_period_ms.

**Exam use:** Keep the handler short; consume the recorded event later in main.

#### `exam_button_events_take`

Atomically obtain and clear all confirmed debounced button events.

**Declaration**

```c
uint32_t exam_button_events_take(void);
```

- **Preconditions:** Use the complete debounce flow to produce events.
- **Returns:** A bit mask containing EXAM_BUTTON_EVENT_INT0, EXAM_BUTTON_EVENT_KEY1, and/or EXAM_BUTTON_EVENT_KEY2; zero means no new event.
- **Side effects:** Clears all button event bits returned by this call.
- **Call context:** Intended for the foreground loop. Events arriving after the protected snapshot remain pending for the next call.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `EXAM_BUTTON_EVENT_INT0 / KEY1 / KEY2` | Take once into a local mask, then test every required event bit. | Current template workflow |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Minimal example**

```c
uint32_t e = exam_button_events_take();
if ((e & EXAM_BUTTON_EVENT_KEY1) != 0u) { /* once per press */ }
```

> **Common mistake:** Calling it repeatedly in separate if expressions and clearing events before later tests see them.

**Exam use:** Take once into a local variable, then test every required bit.

### Timers

Configure Timer0 through Timer3 with MR0 convenience calls or independent match channels and explicit peripheral-clock controls.

#### `exam_timer_config_ticks`

Configure Timer0..Timer3 MR0 from an exact peripheral-clock tick count.

**Declaration**

```c
exam_status_t exam_timer_config_ticks(exam_timer_t timer, uint32_t ticks, exam_timer_mode_t mode);
```

- **Preconditions:** Call exam_init() first and keep one matching TIMERn_IRQHandler when the selected mode enables MR0 interrupts.
- **Returns:** EXAM_OK; EXAM_BAD_ARGUMENT for invalid timer/mode; EXAM_OUT_OF_RANGE when ticks is zero.
- **Side effects:** Powers the timer, stops and resets it, selects timer mode, sets PR=0 and MR0=ticks, clears IR/NVIC pending state, and enables the NVIC source except in modulo-no-IRQ mode. It does not start the timer.
- **Call context:** Foreground configuration. Do not race reconfiguration against another owner of the same timer.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3. |
| `ticks` | in | MR0 count in timer PCLK ticks; 1..0xFFFFFFFF. |
| `mode` | in | EXAM_TIMER_PERIODIC, EXAM_TIMER_ONE_SHOT, or EXAM_TIMER_MODULO_NO_IRQ. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `0xFF` | Short modulo counter used as a seed/input source. | Observed in reviewed solution — `2023-02-07-q2` |
| `0xFFFF` | 16-bit-style modulo counter without MR0 IRQ. | Observed in reviewed solutions — `2025-01-29-arm1-q2`, `2025-01-29-arm2-q2`, `2025-01-29-arm3-q2` |
| `UINT32_MAX` | Longest modulo interval available through MR0. | Observed in reviewed solutions — `2024-02-12-q2`, `2026-06-25-arm1-q2` |
| `1263 / 1592` | Periodic DAC update intervals for the 2025 sine/cosine solutions; do not reuse without the same clock/math. | Observed in reviewed solutions — `2025-02-12-arm1-q2`, `2025-02-12-arm2-q2` |

**Scenario: Use a long modulo timer as an unpredictable user-timing seed**

UINT32_MAX is observed in the reviewed 2024 maze and 2026 game solutions; 0xFF and 0xFFFF appear in earlier timer questions. Sources: `2024-02-12-q2`, `2026-06-25-arm1-q2`.

```c
exam_init();
if (exam_timer_config_ticks(EXAM_TIMER1, UINT32_MAX,
                            EXAM_TIMER_MODULO_NO_IRQ) == EXAM_OK)
  exam_timer_start(EXAM_TIMER1);

/* Read when the user acts; TC is a raw tick value. */
uint32_t seed = exam_timer_read(EXAM_TIMER1);
```

**Scenario: Stream validated DAC samples from a periodic timer**

The 1263-tick Timer0 schedule, samples centered around 500, and zero termination are observed in the reviewed 2025 sine solution. Sources: `2025-02-12-arm1-q2`.

```c
static const uint16_t wave[] = {500u, 620u, 500u, 380u};
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
  exam_timer_start(EXAM_TIMER0);
```

**Scenario: Periodic waveform timer plus one-shot duration timer**

Observed structure in both reviewed 2026-02-18 three-timer solutions; thresholds are calculated by the paper's algorithm rather than guessed constants. Sources: `2026-02-18-arm1-q2`, `2026-02-18-arm2-q2`.

```c
exam_timer_stop(EXAM_TIMER1);
exam_timer_reset(EXAM_TIMER1);
exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                        EXAM_TIMER_PERIODIC);
exam_timer_stop(EXAM_TIMER2);
exam_timer_reset(EXAM_TIMER2);
exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                        EXAM_TIMER_ONE_SHOT);
exam_timer_start(EXAM_TIMER1);
exam_timer_start(EXAM_TIMER2);
```

**Minimal example**

```c
(void)exam_timer_config_ticks(EXAM_TIMER0, 25000u, EXAM_TIMER_PERIODIC);
exam_timer_start(EXAM_TIMER0);
```

> **Common mistake:** Forgetting exam_timer_start() or assuming ticks use the CPU clock instead of the timer's PCLK.

**Exam use:** Prefer ms or Hz helpers unless the question gives an exact tick count.

#### `exam_timer_config_ms`

Configure Timer0..Timer3 MR0 from a millisecond period using that timer's actual PCLK.

**Declaration**

```c
exam_status_t exam_timer_config_ms(exam_timer_t timer, uint32_t milliseconds, exam_timer_mode_t mode);
```

- **Preconditions:** Call exam_init() first. Provide the matching IRQ handler for interrupting modes.
- **Returns:** EXAM_OK; EXAM_BAD_ARGUMENT for invalid timer/mode; EXAM_OUT_OF_RANGE for zero or unrepresentable period; EXAM_NOT_READY if the clock cannot be resolved.
- **Side effects:** Rounds the clock conversion to the nearest tick, then performs the same stopped/reset configuration as exam_timer_config_ticks(). It does not start the timer.
- **Call context:** Foreground configuration; one module must own the selected timer.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3. |
| `milliseconds` | in | Requested period in milliseconds; must be greater than 0 and convert to 1..0xFFFFFFFF ticks. |
| `mode` | in | Periodic, one-shot, or modulo-no-IRQ mode. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `50 ms` | Controller/scheduler tick. | Observed in reviewed solutions — `2026-02-18-arm1-q2` |
| `250 ms` | Toggle interval yielding a 500 ms full blink cycle. | Observed in reviewed solution — `2025-01-29-arm1-q2` |
| `500 ms` | Half-second display step. | Observed in reviewed solutions — `2024-02-28-q2`, `2025-01-29-arm2-q2` |
| `2000 / 2500 / 3000 ms` | Slow result display or rhythm interval, selected by the paper. | Observed in reviewed solutions — `2023-07-04-q2`, `2025-07-01-arm2-q3`, `2025-07-01-arm1-q3` |

**Scenario: Publish a half-second Timer0 event to the foreground**

Observed in the reviewed 2024-02-28 shortest-path solution. Sources: `2024-02-28-q2`.

```c
#define EVENT_HALF_SECOND (1u << 0)

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
}
```

**Minimal example**

```c
if (exam_timer_config_ms(EXAM_TIMER1, 100u, EXAM_TIMER_PERIODIC) == EXAM_OK)
  exam_timer_start(EXAM_TIMER1);
```

> **Common mistake:** Configuring 100 ms and expecting the counter to run before calling exam_timer_start().

**Exam use:** This is the default timer helper for periods stated in milliseconds.

#### `exam_timer_config_hz`

Configure a Timer0..Timer3 periodic interval from a requested frequency.

**Declaration**

```c
exam_status_t exam_timer_config_hz(exam_timer_t timer, uint32_t hertz, exam_timer_mode_t mode);
```

- **Preconditions:** Call exam_init() first and provide the matching handler for interrupting modes.
- **Returns:** EXAM_OK; EXAM_BAD_ARGUMENT for invalid timer/mode; EXAM_OUT_OF_RANGE for zero, above-PCLK, or unrepresentable values; EXAM_NOT_READY if the clock cannot be resolved.
- **Side effects:** Rounds PCLK/hertz to the nearest tick and leaves the selected timer configured but stopped.
- **Call context:** Foreground configuration only.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3. |
| `hertz` | in | Requested events per second; 1..timer PCLK. |
| `mode` | in | Periodic, one-shot, or modulo-no-IRQ mode. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `1000 Hz` | Illustrative 1 kHz sample/update rate when the question specifies frequency rather than period. | Safe API example, not observed in reviewed solutions |

**Scenario: Configure a 1 kHz periodic update when frequency is given**

Safe API illustration. Reviewed solutions use tick and millisecond forms instead of exam_timer_config_hz.

```c
if (exam_timer_config_hz(EXAM_TIMER2, 1000u,
                         EXAM_TIMER_PERIODIC) == EXAM_OK) {
  exam_timer_start(EXAM_TIMER2);
}
```

**Minimal example**

```c
(void)exam_timer_config_hz(EXAM_TIMER2, 1000u, EXAM_TIMER_PERIODIC);
exam_timer_start(EXAM_TIMER2);
```

> **Common mistake:** Passing a period such as 10 when the parameter means 10 events per second.

**Exam use:** Use for sample rates and waveform update frequencies stated in Hz.

#### `exam_timer_start`

Start a previously configured hardware timer.

**Declaration**

```c
void exam_timer_start(exam_timer_t timer);
```

- **Preconditions:** Successfully configure the same timer first.
- **Returns:** No value.
- **Side effects:** Writes TCR=1 for the selected timer; it does not reset TC first.
- **Call context:** Start last, after shared state and interrupt ownership are ready.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3; invalid values are ignored. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Same timer just configured` | Start last, after state and handler ownership are ready. | Observed throughout timer-based solutions |

**Scenario: Publish a half-second Timer0 event to the foreground**

Observed in the reviewed 2024-02-28 shortest-path solution. Sources: `2024-02-28-q2`.

```c
#define EVENT_HALF_SECOND (1u << 0)

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
}
```

**Scenario: Use a long modulo timer as an unpredictable user-timing seed**

UINT32_MAX is observed in the reviewed 2024 maze and 2026 game solutions; 0xFF and 0xFFFF appear in earlier timer questions. Sources: `2024-02-12-q2`, `2026-06-25-arm1-q2`.

```c
exam_init();
if (exam_timer_config_ticks(EXAM_TIMER1, UINT32_MAX,
                            EXAM_TIMER_MODULO_NO_IRQ) == EXAM_OK)
  exam_timer_start(EXAM_TIMER1);

/* Read when the user acts; TC is a raw tick value. */
uint32_t seed = exam_timer_read(EXAM_TIMER1);
```

**Scenario: Stream validated DAC samples from a periodic timer**

The 1263-tick Timer0 schedule, samples centered around 500, and zero termination are observed in the reviewed 2025 sine solution. Sources: `2025-02-12-arm1-q2`.

```c
static const uint16_t wave[] = {500u, 620u, 500u, 380u};
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
  exam_timer_start(EXAM_TIMER0);
```

**Scenario: Periodic waveform timer plus one-shot duration timer**

Observed structure in both reviewed 2026-02-18 three-timer solutions; thresholds are calculated by the paper's algorithm rather than guessed constants. Sources: `2026-02-18-arm1-q2`, `2026-02-18-arm2-q2`.

```c
exam_timer_stop(EXAM_TIMER1);
exam_timer_reset(EXAM_TIMER1);
exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                        EXAM_TIMER_PERIODIC);
exam_timer_stop(EXAM_TIMER2);
exam_timer_reset(EXAM_TIMER2);
exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                        EXAM_TIMER_ONE_SHOT);
exam_timer_start(EXAM_TIMER1);
exam_timer_start(EXAM_TIMER2);
```

**Scenario: Configure a 1 kHz periodic update when frequency is given**

Safe API illustration. Reviewed solutions use tick and millisecond forms instead of exam_timer_config_hz.

```c
if (exam_timer_config_hz(EXAM_TIMER2, 1000u,
                         EXAM_TIMER_PERIODIC) == EXAM_OK) {
  exam_timer_start(EXAM_TIMER2);
}
```

**Minimal example**

```c
exam_timer_start(EXAM_TIMER0);
```

> **Common mistake:** Starting before configuration or expecting start to reset an old counter value.

**Exam use:** Use exam_timer_reset() explicitly when a fresh zero origin is required after prior use.

#### `exam_timer_stop`

Stop one hardware timer without clearing its counter.

**Declaration**

```c
void exam_timer_stop(exam_timer_t timer);
```

- **Preconditions:** None beyond a valid timer selection.
- **Returns:** No value.
- **Side effects:** Writes TCR=0; TC retains its current value.
- **Call context:** Bounded register write; coordinate with the timer's single owner.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3; invalid values are ignored. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Timer0/1/2` | Freeze or terminate a periodic/one-shot workflow before reading or resetting. | Observed in reviewed solutions — `2025-01-29-arm1-q2`, `2026-02-18-arm1-q2` |

**Scenario: Use a long modulo timer as an unpredictable user-timing seed**

UINT32_MAX is observed in the reviewed 2024 maze and 2026 game solutions; 0xFF and 0xFFFF appear in earlier timer questions. Sources: `2024-02-12-q2`, `2026-06-25-arm1-q2`.

```c
exam_init();
if (exam_timer_config_ticks(EXAM_TIMER1, UINT32_MAX,
                            EXAM_TIMER_MODULO_NO_IRQ) == EXAM_OK)
  exam_timer_start(EXAM_TIMER1);

/* Read when the user acts; TC is a raw tick value. */
uint32_t seed = exam_timer_read(EXAM_TIMER1);
```

**Scenario: Stream validated DAC samples from a periodic timer**

The 1263-tick Timer0 schedule, samples centered around 500, and zero termination are observed in the reviewed 2025 sine solution. Sources: `2025-02-12-arm1-q2`.

```c
static const uint16_t wave[] = {500u, 620u, 500u, 380u};
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
  exam_timer_start(EXAM_TIMER0);
```

**Scenario: Periodic waveform timer plus one-shot duration timer**

Observed structure in both reviewed 2026-02-18 three-timer solutions; thresholds are calculated by the paper's algorithm rather than guessed constants. Sources: `2026-02-18-arm1-q2`, `2026-02-18-arm2-q2`.

```c
exam_timer_stop(EXAM_TIMER1);
exam_timer_reset(EXAM_TIMER1);
exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                        EXAM_TIMER_PERIODIC);
exam_timer_stop(EXAM_TIMER2);
exam_timer_reset(EXAM_TIMER2);
exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                        EXAM_TIMER_ONE_SHOT);
exam_timer_start(EXAM_TIMER1);
exam_timer_start(EXAM_TIMER2);
```

**Minimal example**

```c
exam_timer_stop(EXAM_TIMER0);
uint32_t elapsed = exam_timer_read(EXAM_TIMER0);
```

> **Common mistake:** Assuming stop also resets TC to zero.

**Exam use:** Stop first when taking a stable final interval measurement.

#### `exam_timer_reset`

Reset a timer counter to zero and leave it stopped.

**Declaration**

```c
void exam_timer_reset(exam_timer_t timer);
```

- **Preconditions:** The timer may be configured or unconfigured, but must be a valid timer enum.
- **Returns:** No value.
- **Side effects:** Pulses the reset bit through TCR=2 then writes TCR=0.
- **Call context:** Bounded register operation; it does not acknowledge IR flags.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3; invalid values are ignored. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Stop → reset → configure → start` | Reliable restart sequence when changing a timer role or threshold. | Observed in reviewed solutions — `2026-02-18-arm1-q2` |

**Scenario: Periodic waveform timer plus one-shot duration timer**

Observed structure in both reviewed 2026-02-18 three-timer solutions; thresholds are calculated by the paper's algorithm rather than guessed constants. Sources: `2026-02-18-arm1-q2`, `2026-02-18-arm2-q2`.

```c
exam_timer_stop(EXAM_TIMER1);
exam_timer_reset(EXAM_TIMER1);
exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                        EXAM_TIMER_PERIODIC);
exam_timer_stop(EXAM_TIMER2);
exam_timer_reset(EXAM_TIMER2);
exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                        EXAM_TIMER_ONE_SHOT);
exam_timer_start(EXAM_TIMER1);
exam_timer_start(EXAM_TIMER2);
```

**Minimal example**

```c
exam_timer_reset(EXAM_TIMER1);
exam_timer_start(EXAM_TIMER1);
```

> **Common mistake:** Expecting the timer to resume automatically after reset.

**Exam use:** Reset, then start, when measuring a new interval with the same configuration.

#### `exam_timer_read`

Read the current TC count from one hardware timer.

**Declaration**

```c
uint32_t exam_timer_read(exam_timer_t timer);
```

- **Preconditions:** Configure/start the timer when a meaningful elapsed value is required.
- **Returns:** Current 32-bit TC value, or 0 for an invalid timer.
- **Side effects:** None.
- **Call context:** A single register read. The counter may advance immediately after the value is read.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Raw TC ticks` | Use directly as a pseudo-random seed/input only when the question permits; otherwise convert using PCLK. | Observed in reviewed solutions — `2023-02-07-q2`, `2026-06-25-arm1-q2` |

**Scenario: Use a long modulo timer as an unpredictable user-timing seed**

UINT32_MAX is observed in the reviewed 2024 maze and 2026 game solutions; 0xFF and 0xFFFF appear in earlier timer questions. Sources: `2024-02-12-q2`, `2026-06-25-arm1-q2`.

```c
exam_init();
if (exam_timer_config_ticks(EXAM_TIMER1, UINT32_MAX,
                            EXAM_TIMER_MODULO_NO_IRQ) == EXAM_OK)
  exam_timer_start(EXAM_TIMER1);

/* Read when the user acts; TC is a raw tick value. */
uint32_t seed = exam_timer_read(EXAM_TIMER1);
```

**Minimal example**

```c
uint32_t now = exam_timer_read(EXAM_TIMER3);
```

> **Common mistake:** Interpreting TC directly as milliseconds when PR=0 means it counts PCLK ticks.

**Exam use:** Convert using the selected timer's clock when the paper asks for physical time.

#### `exam_timer_ack`

Snapshot and clear all active Timer match/capture interrupt flags.

**Declaration**

```c
uint32_t exam_timer_ack(exam_timer_t timer);
```

- **Preconditions:** Call from the selected timer's single IRQ handler.
- **Returns:** Bits 0..5 from IR before clearing: MR0, MR1, MR2, MR3, CR0, and CR1; returns 0 for invalid timer or no pending source.
- **Side effects:** Clears every returned IR bit by writing the saved mask back to IR.
- **Call context:** IRQ-oriented and bounded. Save the return value once, then test all enabled sources.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `1u << 0` | Test returned MR0 bit after taking the pending mask once. | Observed throughout timer IRQ solutions |

**Scenario: Publish a half-second Timer0 event to the foreground**

Observed in the reviewed 2024-02-28 shortest-path solution. Sources: `2024-02-28-q2`.

```c
#define EVENT_HALF_SECOND (1u << 0)

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
}
```

**Scenario: Stream validated DAC samples from a periodic timer**

The 1263-tick Timer0 schedule, samples centered around 500, and zero termination are observed in the reviewed 2025 sine solution. Sources: `2025-02-12-arm1-q2`.

```c
static const uint16_t wave[] = {500u, 620u, 500u, 380u};
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
  exam_timer_start(EXAM_TIMER0);
```

**Scenario: Configure a 1 kHz periodic update when frequency is given**

Safe API illustration. Reviewed solutions use tick and millisecond forms instead of exam_timer_config_hz.

```c
if (exam_timer_config_hz(EXAM_TIMER2, 1000u,
                         EXAM_TIMER_PERIODIC) == EXAM_OK) {
  exam_timer_start(EXAM_TIMER2);
}
```

**Minimal example**

```c
uint32_t pending = exam_timer_ack(EXAM_TIMER0);
if ((pending & (1u << 0)) != 0u) { /* MR0 work */ }
```

> **Common mistake:** Calling it separately for MR0 and MR1; the first call clears both and the second sees zero.

**Exam use:** Acknowledge first, then publish a small event or perform the short required action.

#### `exam_timer_is_running`

Test the enable bit of one hardware timer.

**Declaration**

```c
uint8_t exam_timer_is_running(exam_timer_t timer);
```

- **Preconditions:** None.
- **Returns:** 1 when TCR bit 0 is set; 0 when stopped or timer is invalid.
- **Side effects:** None.
- **Call context:** Single bounded register read.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `0 or 1` | Guard against starting overlapping Timer1/Timer2 note workflows. | Observed in reviewed solutions — `2026-02-18-arm1-q2`, `2026-02-18-arm2-q2` |

**Scenario: Periodic waveform timer plus one-shot duration timer**

Observed structure in both reviewed 2026-02-18 three-timer solutions; thresholds are calculated by the paper's algorithm rather than guessed constants. Sources: `2026-02-18-arm1-q2`, `2026-02-18-arm2-q2`.

```c
exam_timer_stop(EXAM_TIMER1);
exam_timer_reset(EXAM_TIMER1);
exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                        EXAM_TIMER_PERIODIC);
exam_timer_stop(EXAM_TIMER2);
exam_timer_reset(EXAM_TIMER2);
exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                        EXAM_TIMER_ONE_SHOT);
exam_timer_start(EXAM_TIMER1);
exam_timer_start(EXAM_TIMER2);
```

**Minimal example**

```c
if (!exam_timer_is_running(EXAM_TIMER0)) exam_timer_start(EXAM_TIMER0);
```

> **Common mistake:** Using this result to infer that the timer was configured correctly or that an IRQ is enabled.

**Exam use:** It answers only whether the counter enable bit is set.

#### `exam_timer_config_match`

Configure one match channel without disturbing the others or starting the timer.

**Declaration**

```c
exam_status_t exam_timer_config_match(exam_timer_t timer, uint8_t match, uint32_t ticks, uint32_t actions);
```

- **Preconditions:** Call exam_init once, then a successful exam_timer_config_ticks/ms/hz for this timer. It must remain powered and stopped, with neither TCR enable nor reset set.
- **Returns:** EXAM_OK on success; EXAM_BAD_ARGUMENT for an invalid timer/index/action/divider; EXAM_NOT_READY if uninitialized, unpowered, running or held in reset. Invalid calls leave peripheral configuration unchanged. Zero ticks: EXAM_OUT_OF_RANGE.
- **Side effects:** Writes only the selected MR and its three MCR bits; acknowledges only its old IR flag. Enables NVIC if INTERRUPT is selected, preserving priority and pending state for other sources. Preserves TC, PC, PR, CCR, EMR and other matches.
- **Call context:** Foreground stopped-timer setup. A short critical section restores the original interrupt mask.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3 |
| `match` | in | 0..3 selects MR0..MR3 |
| `ticks` | in | 1..UINT32_MAX counter ticks; zero returns EXAM_OUT_OF_RANGE |
| `actions` | in | 0..7: any OR combination of EXAM_MATCH_INTERRUPT, EXAM_MATCH_RESET, EXAM_MATCH_STOP |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `See parameter ranges` | Do not assume this helper clears another channel's reset/stop action. A reset on an earlier match can prevent later matches. | Current implementation contract |

**Scenario: One timer with four independent match notifications**

Teaching example; inspect matches[0..3] after each cycle.

```c
#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
```

**Minimal example**

```c
#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
```

> **Common mistake:** Do not assume this helper clears another channel's reset/stop action. A reset on an earlier match can prevent later matches.

**Exam use:** Keep exact paper tick values. This example uses teaching values; at a 100 MHz core, PR=24 and divider=4 yield a 1 MHz counter.

#### `exam_timer_set_prescaler`

Set the prescaler of an initialized stopped timer.

**Declaration**

```c
exam_status_t exam_timer_set_prescaler(exam_timer_t timer, uint32_t prescaler);
```

- **Preconditions:** Call exam_init once, then a successful exam_timer_config_ticks/ms/hz for this timer. It must remain powered and stopped, with neither TCR enable nor reset set.
- **Returns:** EXAM_OK on success; EXAM_BAD_ARGUMENT for an invalid timer/index/action/divider; EXAM_NOT_READY if uninitialized, unpowered, running or held in reset. Invalid calls leave peripheral configuration unchanged.
- **Side effects:** Writes PR and clears PC; preserves TC, matches, flags, NVIC and clock selection.
- **Call context:** Foreground stopped-timer setup. A short critical section restores the original interrupt mask.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3 |
| `prescaler` | in | 0..UINT32_MAX; TC advances once per PR+1 peripheral clocks |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `See parameter ranges` | Apply after standard configuration, which always sets PR=0. PR=24 means 25 peripheral clocks per counter tick. | Current implementation contract |

**Scenario: One timer with four independent match notifications**

Teaching example; inspect matches[0..3] after each cycle.

```c
#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
```

**Minimal example**

```c
#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
```

> **Common mistake:** Apply after standard configuration, which always sets PR=0. PR=24 means 25 peripheral clocks per counter tick.

**Exam use:** Keep exact paper tick values. This example uses teaching values; at a 100 MHz core, PR=24 and divider=4 yield a 1 MHz counter.

#### `exam_timer_set_clock_divider`

Select the peripheral clock divider of one stopped timer.

**Declaration**

```c
exam_status_t exam_timer_set_clock_divider(exam_timer_t timer, uint8_t divider);
```

- **Preconditions:** Call exam_init once, then a successful exam_timer_config_ticks/ms/hz for this timer. It must remain powered and stopped, with neither TCR enable nor reset set.
- **Returns:** EXAM_OK on success; EXAM_BAD_ARGUMENT for an invalid timer/index/action/divider; EXAM_NOT_READY if uninitialized, unpowered, running or held in reset. Invalid calls leave peripheral configuration unchanged.
- **Side effects:** Changes only this timer's two PCLKSEL bits; preserves counters, match/capture configuration, other clocks and interrupt state.
- **Call context:** Foreground stopped-timer setup. A short critical section restores the original interrupt mask.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `timer` | in | EXAM_TIMER0..EXAM_TIMER3 |
| `divider` | in | 1, 2, 4 or 8; all other values rejected |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `See parameter ranges` | Changing PCLK after millisecond/hertz configuration changes the resulting period. Recompute or use explicit ticks. Counter frequency is core_clock/divider/(PR+1). | Current implementation contract |

**Scenario: One timer with four independent match notifications**

Teaching example; inspect matches[0..3] after each cycle.

```c
#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
```

**Minimal example**

```c
#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
```

> **Common mistake:** Changing PCLK after millisecond/hertz configuration changes the resulting period. Recompute or use explicit ticks. Counter frequency is core_clock/divider/(PR+1).

**Exam use:** Keep exact paper tick values. This example uses teaching values; at a 100 MHz core, PR=24 and divider=4 yield a 1 MHz counter.

#### `exam_timer_match_happened`

Test match status in an already saved interrupt snapshot.

**Declaration**

```c
uint8_t exam_timer_match_happened(uint32_t flags, uint8_t match);
```

- **Preconditions:** No hardware setup is needed to test a value.
- **Returns:** 1 when bit 0+index is set; otherwise 0.
- **Side effects:** None: no register reads, no acknowledgement, no NVIC changes.
- **Call context:** IRQ or foreground, pure function.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `flags` | in | Saved result from one exam_timer_ack(timer) call |
| `match` | in | 0..3; invalid indexes return zero |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `index 0..3` | Tests snapshot bit 0+index | LPC1768 timer IR mapping |

**Scenario: One timer with four independent match notifications**

Teaching example; inspect matches[0..3] after each cycle.

```c
#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
```

**Minimal example**

```c
#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}
```

> **Common mistake:** Acknowledging a second time loses the first snapshot. Testing a capture flag does not configure a capture pin or CCR.

**Exam use:** Simultaneous sources may set several bits; use independent tests.

#### `exam_timer_capture_happened`

Test capture status in an already saved interrupt snapshot.

**Declaration**

```c
uint8_t exam_timer_capture_happened(uint32_t flags, uint8_t capture);
```

- **Preconditions:** No hardware setup is needed to test a value.
- **Returns:** 1 when bit 4+index is set; otherwise 0.
- **Side effects:** None: no register reads, no acknowledgement, no NVIC changes.
- **Call context:** IRQ or foreground, pure function.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `flags` | in | Saved result from one exam_timer_ack(timer) call |
| `capture` | in | 0..1; invalid indexes return zero |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `index 0..1` | Tests snapshot bit 4+index | LPC1768 timer IR mapping |

**Scenario: Capture an edge using CAP0.0**

Teaching example with explicit pin and capture configuration.

```c
#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint32_t last_capture, capture_count;
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_capture_happened(flags,0u)) { last_capture=LPC_TIM0->CR0; ++capture_count; }
}
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0,UINT32_MAX,EXAM_TIMER_MODULO_NO_IRQ));
  require(exam_timer_config_match(EXAM_TIMER0,0u,UINT32_MAX,0u));
  /* P1.26 function 3 is CAP0.0; capture TC on rising edges and interrupt. */
  LPC_PINCON->PINSEL3=(LPC_PINCON->PINSEL3 & ~(3u<<20)) | (3u<<20);
  LPC_GPIO1->FIODIR &= ~(1u<<26);
  LPC_TIM0->CCR=(LPC_TIM0->CCR & ~7u) | 5u;
  (void)exam_timer_ack(EXAM_TIMER0);NVIC_ClearPendingIRQ(TIMER0_IRQn);
  NVIC_EnableIRQ(TIMER0_IRQn);exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}

```

**Minimal example**

```c
#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
volatile uint32_t last_capture, capture_count;
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_capture_happened(flags,0u)) { last_capture=LPC_TIM0->CR0; ++capture_count; }
}
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0,UINT32_MAX,EXAM_TIMER_MODULO_NO_IRQ));
  require(exam_timer_config_match(EXAM_TIMER0,0u,UINT32_MAX,0u));
  /* P1.26 function 3 is CAP0.0; capture TC on rising edges and interrupt. */
  LPC_PINCON->PINSEL3=(LPC_PINCON->PINSEL3 & ~(3u<<20)) | (3u<<20);
  LPC_GPIO1->FIODIR &= ~(1u<<26);
  LPC_TIM0->CCR=(LPC_TIM0->CCR & ~7u) | 5u;
  (void)exam_timer_ack(EXAM_TIMER0);NVIC_ClearPendingIRQ(TIMER0_IRQn);
  NVIC_EnableIRQ(TIMER0_IRQn);exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
```

> **Common mistake:** Acknowledging a second time loses the first snapshot. Testing a capture flag does not configure a capture pin or CCR.

**Exam use:** Simultaneous sources may set several bits; use independent tests.

### SysTick

Start or stop the Cortex-M3 system tick for short periodic work.

#### `exam_systick_config_ticks`

Configure and immediately start SysTick with an exact core-clock tick period.

**Declaration**

```c
exam_status_t exam_systick_config_ticks(uint32_t ticks);
```

- **Preconditions:** Provide exactly one SysTick_Handler and initialize shared state before calling.
- **Returns:** EXAM_OK or EXAM_OUT_OF_RANGE.
- **Side effects:** Stops SysTick, writes LOAD=ticks-1, clears VAL, then enables core-clock counting and its interrupt immediately.
- **Call context:** Foreground configuration. SysTick exception entry clears its pending condition automatically; there is no API acknowledgement call.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `ticks` | in | Period in core-clock ticks, 1..0x01000000 inclusive. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `0x100000` | DFS scheduling tick used by the 2024 SysTick solution. | Observed in reviewed solution — `2024-07-09-q2` |

**Scenario: Start the exact SysTick interval used by the 2024 DFS solution**

Observed in the reviewed 2024-07-09 DFS/SysTick solution. Sources: `2024-07-09-q2`.

```c
exam_init();
if (exam_systick_config_ticks(0x100000u) != EXAM_OK) {
  exam_led_write(0xFFu);
}
/* Successful configuration has already started SysTick. */
```

**Minimal example**

```c
(void)exam_systick_config_ticks(SystemFrequency / 1000u);
```

> **Common mistake:** Calling a nonexistent acknowledge helper or forgetting that configuration starts SysTick immediately.

**Exam use:** Use for compact periodic scheduling when the 24-bit reload limit is sufficient.

#### `exam_systick_config_ms`

Configure and immediately start SysTick from a millisecond period.

**Declaration**

```c
exam_status_t exam_systick_config_ms(uint32_t milliseconds);
```

- **Preconditions:** Call exam_init() first and provide the single SysTick_Handler.
- **Returns:** EXAM_OK or EXAM_OUT_OF_RANGE.
- **Side effects:** Rounds SystemFrequency*milliseconds/1000 to ticks and starts SysTick immediately.
- **Call context:** Foreground configuration; handler acknowledgement is automatic.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `milliseconds` | in | Period in milliseconds; must be greater than 0 and fit the 24-bit SysTick reload range after conversion. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `10 ms` | Alternative debounce tick source; configuration starts SysTick immediately. | Recommended workflow value, not observed in reviewed solutions |

**Scenario: Use SysTick instead of RIT for the same debounce interval**

Safe API-derived alternative; not an observed solved-exam combination.

```c
exam_buttons_init();
if (exam_debounce_config(10u, 50u) == EXAM_OK)
  (void)exam_systick_config_ms(10u); /* starts immediately */

void SysTick_Handler(void) {
  exam_debounce_tick(); /* SysTick acknowledgement is automatic */
}
```

**Minimal example**

```c
if (exam_systick_config_ms(10u) != EXAM_OK) { /* period too large */ }
```

> **Common mistake:** Calling a separate start function; none exists because successful configuration already starts it.

**Exam use:** A 10 ms tick pairs naturally with exam_debounce_config(10, confirmation_ms).

#### `exam_systick_stop`

Disable SysTick counting and its interrupt.

**Declaration**

```c
void exam_systick_stop(void);
```

- **Preconditions:** None.
- **Returns:** No value.
- **Side effects:** Writes SysTick->CTRL=0; LOAD remains programmed but inactive.
- **Call context:** Bounded register write.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `No argument` | Stop only when no other feature depends on SysTick. | API ownership rule |

**Scenario: Start the exact SysTick interval used by the 2024 DFS solution**

Observed in the reviewed 2024-07-09 DFS/SysTick solution. Sources: `2024-07-09-q2`.

```c
exam_init();
if (exam_systick_config_ticks(0x100000u) != EXAM_OK) {
  exam_led_write(0xFFu);
}
/* Successful configuration has already started SysTick. */
```

**Scenario: Use SysTick instead of RIT for the same debounce interval**

Safe API-derived alternative; not an observed solved-exam combination.

```c
exam_buttons_init();
if (exam_debounce_config(10u, 50u) == EXAM_OK)
  (void)exam_systick_config_ms(10u); /* starts immediately */

void SysTick_Handler(void) {
  exam_debounce_tick(); /* SysTick acknowledgement is automatic */
}
```

**Minimal example**

```c
exam_systick_stop();
```

> **Common mistake:** Stopping SysTick when another feature, such as debounce, still depends on its ticks.

**Exam use:** Keep one owner for the shared SysTick resource.

### RIT

Configure and control the LPC1768 Repetitive Interrupt Timer.

#### `exam_rit_config_ticks`

Configure RIT with an exact tick count and leave it stopped.

**Declaration**

```c
exam_status_t exam_rit_config_ticks(uint32_t ticks);
```

- **Preconditions:** Call exam_init() first and keep exactly one RIT_IRQHandler.
- **Returns:** EXAM_OK or EXAM_OUT_OF_RANGE when ticks is zero.
- **Side effects:** Calls the professor init_RIT(ticks) helper. Configuration does not enable RIT.
- **Call context:** Foreground setup; call exam_rit_start() after state and handler ownership are ready.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `ticks` | in | RIT compare interval in ticks; 1..0xFFFFFFFF. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `SystemFrequency / 100` | Ten-millisecond interval when RIT runs at CCLK. | Derived equivalent of observed 10 ms usage |

**Scenario: Configure and restart a 10 ms RIT interval in ticks**

Safe tick-form equivalent of the 10 ms RIT polling interval observed in the 2025 and 2026 joystick solutions. Confirm the RIT clock before deriving ticks. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
uint32_t rit_ticks = SystemFrequency / 100u; /* 10 ms only when RIT uses CCLK */
if (exam_rit_config_ticks(rit_ticks) == EXAM_OK) {
  exam_rit_reset();
  exam_rit_start();
}
/* Later, after every RIT consumer has finished: */
exam_rit_stop();
```

**Minimal example**

```c
(void)exam_rit_config_ticks(SystemFrequency / 100u);
exam_rit_start();
```

> **Common mistake:** Expecting configuration to start the RIT interrupt stream.

**Exam use:** Prefer exam_rit_config_ms() when the required interval is stated in milliseconds.

#### `exam_rit_config_ms`

Configure RIT from a millisecond interval and leave it stopped.

**Declaration**

```c
exam_status_t exam_rit_config_ms(uint32_t milliseconds);
```

- **Preconditions:** Call exam_init() first and provide the one RIT_IRQHandler.
- **Returns:** EXAM_OK or EXAM_OUT_OF_RANGE for zero or an unrepresentable interval.
- **Side effects:** Rounds SystemFrequency*milliseconds/1000 and delegates to exam_rit_config_ticks(); it does not start RIT.
- **Call context:** Foreground configuration.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `milliseconds` | in | Period in milliseconds; must convert to 1..0xFFFFFFFF SystemFrequency ticks. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `10 ms` | Joystick polling and input-edge sampling. | Observed in reviewed solutions — `2025-07-01-arm1-q3`, `2025-07-01-arm2-q3`, `2026-06-25-arm1-q2`, `2026-06-25-arm2-q2` |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Scenario: Poll joystick press edges every 10 ms**

Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
static uint32_t previous_joystick;
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
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();
```

**Minimal example**

```c
(void)exam_rit_config_ms(10u);
exam_rit_start();
```

> **Common mistake:** Confusing RIT configuration with SysTick configuration; RIT requires an explicit start.

**Exam use:** Useful as an independent periodic source for joystick polling or debounce.

#### `exam_rit_start`

Enable a previously configured RIT.

**Declaration**

```c
void exam_rit_start(void);
```

- **Preconditions:** Successfully call one RIT configuration helper first.
- **Returns:** No value.
- **Side effects:** Calls enable_RIT().
- **Call context:** Start after the RIT handler and shared state are ready.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `After successful configuration` | Start only after the handler and sampled state are initialized. | Observed in reviewed solutions |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Scenario: Poll joystick press edges every 10 ms**

Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
static uint32_t previous_joystick;
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
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();
```

**Scenario: Configure and restart a 10 ms RIT interval in ticks**

Safe tick-form equivalent of the 10 ms RIT polling interval observed in the 2025 and 2026 joystick solutions. Confirm the RIT clock before deriving ticks. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
uint32_t rit_ticks = SystemFrequency / 100u; /* 10 ms only when RIT uses CCLK */
if (exam_rit_config_ticks(rit_ticks) == EXAM_OK) {
  exam_rit_reset();
  exam_rit_start();
}
/* Later, after every RIT consumer has finished: */
exam_rit_stop();
```

**Minimal example**

```c
exam_rit_start();
```

> **Common mistake:** Starting before configuration or allowing two features to reconfigure the same RIT.

**Exam use:** RIT is a single shared peripheral; assign it one timing responsibility.

#### `exam_rit_stop`

Disable RIT without changing its documented configuration.

**Declaration**

```c
void exam_rit_stop(void);
```

- **Preconditions:** None.
- **Returns:** No value.
- **Side effects:** Calls disable_RIT().
- **Call context:** Bounded peripheral-control call.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `No argument` | Stop when every RIT consumer has finished. | API ownership rule |

**Scenario: Configure and restart a 10 ms RIT interval in ticks**

Safe tick-form equivalent of the 10 ms RIT polling interval observed in the 2025 and 2026 joystick solutions. Confirm the RIT clock before deriving ticks. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
uint32_t rit_ticks = SystemFrequency / 100u; /* 10 ms only when RIT uses CCLK */
if (exam_rit_config_ticks(rit_ticks) == EXAM_OK) {
  exam_rit_reset();
  exam_rit_start();
}
/* Later, after every RIT consumer has finished: */
exam_rit_stop();
```

**Minimal example**

```c
exam_rit_stop();
```

> **Common mistake:** Stopping RIT while debounce or joystick sampling still depends on it.

**Exam use:** Stop only when every consumer of that tick source is finished.

#### `exam_rit_reset`

Reset the RIT counter through the professor driver.

**Declaration**

```c
void exam_rit_reset(void);
```

- **Preconditions:** RIT should already be configured when its compare interval must remain meaningful.
- **Returns:** No value.
- **Side effects:** Calls reset_RIT().
- **Call context:** Bounded peripheral-control call; it is distinct from interrupt acknowledgement.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `No argument` | Restart the counter origin; this does not replace IRQ acknowledgement. | API contract |

**Scenario: Configure and restart a 10 ms RIT interval in ticks**

Safe tick-form equivalent of the 10 ms RIT polling interval observed in the 2025 and 2026 joystick solutions. Confirm the RIT clock before deriving ticks. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
uint32_t rit_ticks = SystemFrequency / 100u; /* 10 ms only when RIT uses CCLK */
if (exam_rit_config_ticks(rit_ticks) == EXAM_OK) {
  exam_rit_reset();
  exam_rit_start();
}
/* Later, after every RIT consumer has finished: */
exam_rit_stop();
```

**Minimal example**

```c
exam_rit_reset();
```

> **Common mistake:** Using reset instead of exam_rit_ack() inside RIT_IRQHandler.

**Exam use:** Use acknowledgement for every IRQ; use reset only when the question needs a new timing origin.

#### `exam_rit_ack`

Acknowledge the active RIT interrupt.

**Declaration**

```c
void exam_rit_ack(void);
```

- **Preconditions:** Call from the single RIT_IRQHandler.
- **Returns:** No value.
- **Side effects:** Sets RICTRL bit 0 to clear the interrupt flag.
- **Call context:** IRQ-only in normal use; call before returning from the handler.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `First line of RIT_IRQHandler` | Clear the hardware source before sampling or publishing events. | Observed in reviewed solutions — `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2` |

**Scenario: Debounced KEY1 press using a 10 ms RIT tick**

Recommended maintained package recipe. The past exams repeatedly require deterministic button handling, but this exact 10/50 pair is not claimed as a literal paper constant.

```c
/* main setup */
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
}
```

**Scenario: Poll joystick press edges every 10 ms**

Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
static uint32_t previous_joystick;
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
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();
```

**Scenario: Configure and restart a 10 ms RIT interval in ticks**

Safe tick-form equivalent of the 10 ms RIT polling interval observed in the 2025 and 2026 joystick solutions. Confirm the RIT clock before deriving ticks. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
uint32_t rit_ticks = SystemFrequency / 100u; /* 10 ms only when RIT uses CCLK */
if (exam_rit_config_ticks(rit_ticks) == EXAM_OK) {
  exam_rit_reset();
  exam_rit_start();
}
/* Later, after every RIT consumer has finished: */
exam_rit_stop();
```

**Minimal example**

```c
void RIT_IRQHandler(void) { exam_rit_ack(); exam_debounce_tick(); }
```

> **Common mistake:** Omitting acknowledgement and immediately re-entering the handler.

**Exam use:** Acknowledge first, then perform only bounded tick work.

### Joystick

Read the five active-low joystick controls and derive press and release edges.

#### `exam_joystick_init`

Configure P1.25..P1.29 as unmasked GPIO inputs for the five-way joystick.

**Declaration**

```c
void exam_joystick_init(void);
```

- **Preconditions:** Call exam_init() first.
- **Returns:** No value.
- **Side effects:** Calls joystick_init(), selects GPIO function and default pin mode, sets input direction, and clears the FIO mask for all five controls.
- **Call context:** Foreground initialization only.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Once` | Before the first state sample and before starting the 10 ms RIT poll. | Observed in reviewed solutions |

**Scenario: Poll joystick press edges every 10 ms**

Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
static uint32_t previous_joystick;
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
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();
```

**Minimal example**

```c
exam_joystick_init();
uint32_t previous = exam_joystick_read();
```

> **Common mistake:** Leaving FIO pins masked, which makes inversion look like every control is pressed.

**Exam use:** Initialize once, then sample periodically if the question needs press edges.

#### `exam_joystick_read`

Return the current pressed-state mask for all five active-low joystick controls.

**Declaration**

```c
uint32_t exam_joystick_read(void);
```

- **Preconditions:** Call exam_joystick_init() first.
- **Returns:** Bits EXAM_JOY_SELECT, DOWN, LEFT, RIGHT, and UP; a set bit means currently pressed. The API supports all 8 directions as combinations of four direction bits, plus a separate centre SELECT press. Diagonals are UP | LEFT, UP | RIGHT, DOWN | LEFT, and DOWN | RIGHT (use the EXAM_JOY_ prefix for each flag). There are no separate diagonal constants and no four-direction restriction in the API. Both inputs must be activated by the board or simulator. Follow the exam question: implement four directions when it asks for four, and diagonals when required.
- **Side effects:** None.
- **Call context:** Single bounded GPIO read; it returns levels, not debounced events.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `0..0x1F mask` | Store the first reading as previous; later readings are current. | Observed in reviewed solutions |

**Scenario: Poll joystick press edges every 10 ms**

Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
static uint32_t previous_joystick;
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
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();
```

**Minimal example**

```c
uint32_t current = exam_joystick_read();
uint32_t diagonal = EXAM_JOY_UP | EXAM_JOY_RIGHT;
if ((current & diagonal) == diagonal) {
    /* UP and RIGHT are both held. */
}
```

> **Common mistake:** Inverting the returned mask again even though the helper already converts active-low input to pressed=1.

**Exam use:** Test the current held-state mask for a diagonal; the two controls may become pressed in different samples, so requiring both pressed-edge bits together can miss it. A held-state test remains true while held; implement one-action or repeat behavior separately as required by the paper.

#### `exam_joystick_pressed_edges`

Derive controls that changed from released to pressed between two joystick samples.

**Declaration**

```c
uint32_t exam_joystick_pressed_edges(uint32_t previous, uint32_t current);
```

- **Preconditions:** Supply successive values returned by exam_joystick_read().
- **Returns:** current & ~previous limited to the five EXAM_JOY_* bits.
- **Side effects:** None.
- **Call context:** Pure bounded computation; it does not store history or implement key repeat.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `previous` | in | Earlier pressed-state mask; bits outside the five joystick bits are ignored. |
| `current` | in | New pressed-state mask; bits outside the five joystick bits are ignored. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `previous, current` | Returns new press bits only; then assign previous=current. | Observed in reviewed solutions — `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2` |

**Scenario: Poll joystick press edges every 10 ms**

Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
static uint32_t previous_joystick;
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
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();
```

**Scenario: Press lights LD11; hold retains it; release clears it**

Teaching example; raw comparisons without debounce or repeat.

```c
#include "exam_api.h"
volatile uint32_t held, pressed, released;
int main(void) {
  uint32_t previous, current;
  exam_init();
  exam_joystick_init();
  previous = exam_joystick_read();
  for (;;) {
    current = exam_joystick_read();
    pressed = exam_joystick_pressed_edges(previous, current);
    released = exam_joystick_released_edges(previous, current);
    held = current;
    if (pressed & EXAM_JOY_SELECT) exam_led_write(1u);
    if (released & EXAM_JOY_SELECT) exam_led_clear();
    previous = current;
  }
}
```

**Minimal example**

```c
uint32_t current = exam_joystick_read();
uint32_t pressed = exam_joystick_pressed_edges(previous, current);
previous = current;
```

> **Common mistake:** Reversing previous and current or forgetting to update previous after each sample.

**Exam use:** The question owns sampling rate, debounce, prolonged-pressure, and repeat policy.

#### `exam_joystick_released_edges`

Find five-bit joystick controls released since the previous sample.

**Declaration**

```c
uint32_t exam_joystick_released_edges(uint32_t previous, uint32_t current);
```

- **Preconditions:** None for mask comparison; initialize joystick before raw hardware reads.
- **Returns:** previous & ~current & 0x1F; high bits are ignored.
- **Side effects:** None; no hardware access or hidden state.
- **Call context:** Pure function; caller chooses sampling and repeat policy.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `previous` | in | Earlier active-high pressed mask |
| `current` | in | Current active-high pressed mask |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `0x01..0x10; combined masks` | SELECT/DOWN/LEFT/RIGHT/UP; no hidden repeat | Current joystick bit mapping |

**Scenario: Press lights LD11; hold retains it; release clears it**

Teaching example; raw comparisons without debounce or repeat.

```c
#include "exam_api.h"
volatile uint32_t held, pressed, released;
int main(void) {
  uint32_t previous, current;
  exam_init();
  exam_joystick_init();
  previous = exam_joystick_read();
  for (;;) {
    current = exam_joystick_read();
    pressed = exam_joystick_pressed_edges(previous, current);
    released = exam_joystick_released_edges(previous, current);
    held = current;
    if (pressed & EXAM_JOY_SELECT) exam_led_write(1u);
    if (released & EXAM_JOY_SELECT) exam_led_clear();
    previous = current;
  }
}
```

**Minimal example**

```c
#include "exam_api.h"
volatile uint32_t held, pressed, released;
int main(void) {
  uint32_t previous, current;
  exam_init();
  exam_joystick_init();
  previous = exam_joystick_read();
  for (;;) {
    current = exam_joystick_read();
    pressed = exam_joystick_pressed_edges(previous, current);
    released = exam_joystick_released_edges(previous, current);
    held = current;
    if (pressed & EXAM_JOY_SELECT) exam_led_write(1u);
    if (released & EXAM_JOY_SELECT) exam_led_clear();
    previous = current;
  }
}
```

> **Common mistake:** The argument order is (previous, current), matching pressed_edges. The retired (current, changed) convention is incompatible.

**Exam use:** Initialize previous from the current read to avoid synthesizing startup edges. Raw edge detection is not debounce.

### ADC

Start one channel-5 conversion, capture it in the IRQ, and consume the fresh 12-bit result in main.

#### `exam_adc_init`

Initialize ADC channel 5 on P1.31 and clear the API's cached result state.

**Declaration**

```c
void exam_adc_init(void);
```

- **Preconditions:** Call exam_init() first and keep exactly one ADC_IRQHandler.
- **Returns:** No value.
- **Side effects:** Clears cached ADC value/freshness under a critical section, then calls ADC_init().
- **Call context:** Foreground initialization only.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Channel 5 / P1.31` | The fixed potentiometer input supported by this API. | Current hardware contract |

**Scenario: Continuously convert the potentiometer and show its high byte**

Observed in the three reviewed 2026-02-03 ADC solutions. Sources: `2026-02-03-arm1-q2`, `2026-02-03-arm3-q2`.

```c
void ADC_IRQHandler(void) {
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
}
```

**Minimal example**

```c
exam_adc_init();
exam_adc_start();
```

> **Common mistake:** Reading a result immediately after initialization without starting and completing a conversion.

**Exam use:** The supported simple workflow is one conversion at a time on the potentiometer channel.

#### `exam_adc_start`

Start one ADC conversion using the configured channel-5 driver.

**Declaration**

```c
void exam_adc_start(void);
```

- **Preconditions:** Call exam_adc_init() first and do not start another conversion until the intended workflow is ready for it.
- **Returns:** No value.
- **Side effects:** Calls ADC_start_conversion().
- **Call context:** Normally called from foreground or a bounded scheduler action; completion arrives through ADC_IRQHandler.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `One conversion` | Start once after init and again only after consuming the previous sample. | Observed in reviewed solutions — `2026-02-03-arm1-q2` |

**Scenario: Continuously convert the potentiometer and show its high byte**

Observed in the three reviewed 2026-02-03 ADC solutions. Sources: `2026-02-03-arm1-q2`, `2026-02-03-arm3-q2`.

```c
void ADC_IRQHandler(void) {
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
}
```

**Minimal example**

```c
exam_adc_start();
```

> **Common mistake:** Starting repeatedly without consuming or deliberately replacing the previous fresh sample.

**Exam use:** Use the sequence start -> IRQ capture -> take.

#### `exam_adc_irq_capture`

Capture a completed 12-bit ADC result into the API's interrupt-to-main mailbox.

**Declaration**

```c
void exam_adc_irq_capture(void);
```

- **Preconditions:** ADC must be initialized and the call should be made by the single ADC_IRQHandler.
- **Returns:** No value.
- **Side effects:** Reads ADGDR. When DONE bit 31 is set, stores result bits 15:4 and marks the sample fresh; otherwise leaves cached state unchanged.
- **Call context:** IRQ helper; bounded and contains no foreground processing.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `ADGDR DONE=1` | Capture only completed 12-bit values; the helper ignores incomplete reads. | Current hardware contract |

**Scenario: Continuously convert the potentiometer and show its high byte**

Observed in the three reviewed 2026-02-03 ADC solutions. Sources: `2026-02-03-arm1-q2`, `2026-02-03-arm3-q2`.

```c
void ADC_IRQHandler(void) {
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
}
```

**Minimal example**

```c
void ADC_IRQHandler(void) { exam_adc_irq_capture(); }
```

> **Common mistake:** Reading/scaling the ADC in multiple owners or omitting the capture call from the IRQ.

**Exam use:** Capture in the handler and perform display, scaling, or algorithm work in main.

#### `exam_adc_take`

Atomically take the newest captured ADC sample if one is fresh.

**Declaration**

```c
uint8_t exam_adc_take(uint16_t *result);
```

- **Preconditions:** Use exam_adc_init(), exam_adc_start(), and exam_adc_irq_capture() to produce samples.
- **Returns:** 1 when a fresh sample was copied and consumed; 0 for null result or when no fresh sample is available.
- **Side effects:** Clears the fresh flag only when a sample is returned. Does not modify *result when returning 0.
- **Call context:** Foreground consumer; the critical section prevents a torn mailbox update.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `result` | out | Non-null pointer receiving a 12-bit value 0..4095 when the function returns 1. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `0..4095` | Valid 12-bit result only when the function returns 1. | API range and observed workflow — `2026-02-03-arm1-q2`, `2026-02-03-arm2-q2`, `2026-02-03-arm3-q2` |

**Scenario: Continuously convert the potentiometer and show its high byte**

Observed in the three reviewed 2026-02-03 ADC solutions. Sources: `2026-02-03-arm1-q2`, `2026-02-03-arm3-q2`.

```c
void ADC_IRQHandler(void) {
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
}
```

**Minimal example**

```c
uint16_t sample;
if (exam_adc_take(&sample)) exam_adc_show_high8(sample);
```

> **Common mistake:** Using sample after a zero return, when the output variable was not updated.

**Exam use:** Test the return value before processing the result.

#### `exam_adc_show_high8`

Display ADC result bits 11:4 on the eight LEDs.

**Declaration**

```c
void exam_adc_show_high8(uint16_t result);
```

- **Preconditions:** Initialize LEDs with exam_init(); normally pass a successful exam_adc_take() result.
- **Returns:** No value.
- **Side effects:** Replaces the complete LED display through exam_led_write().
- **Call context:** Keep it in foreground when called as part of the ADC mailbox workflow.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `result` | in | ADC result; only the low 12 bits are used before shifting right by four. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `result >> 4` | Display ADC bits 11:4 as 0..255 on LEDs. | Observed conversion pattern — `2026-02-03-arm1-q2` |

**Scenario: Continuously convert the potentiometer and show its high byte**

Observed in the three reviewed 2026-02-03 ADC solutions. Sources: `2026-02-03-arm1-q2`, `2026-02-03-arm3-q2`.

```c
void ADC_IRQHandler(void) {
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
}
```

**Minimal example**

```c
uint16_t sample;
if (exam_adc_take(&sample)) exam_adc_show_high8(sample);
```

> **Common mistake:** Calling it with an uninitialized value when exam_adc_take() returned zero.

**Exam use:** This is the direct 12-bit-to-8-bit display required by many potentiometer exercises.

### DAC

Initialize P0.26 as AOUT and write a validated 10-bit sample.

#### `exam_dac_init`

Configure P0.26 as DAC AOUT with deterministic zero output and fast-mode BIAS=0.

**Declaration**

```c
void exam_dac_init(void);
```

- **Preconditions:** Call exam_init() first.
- **Returns:** No value.
- **Side effects:** Selects the DAC pin function, sets P0.26 direction, and writes DACR=0.
- **Call context:** Foreground initialization only.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Initial sample 0` | Start from silence/zero output before waveform playback. | Observed in reviewed solutions — `2026-02-18-arm1-q2` |

**Scenario: Stream validated DAC samples from a periodic timer**

The 1263-tick Timer0 schedule, samples centered around 500, and zero termination are observed in the reviewed 2025 sine solution. Sources: `2025-02-12-arm1-q2`.

```c
static const uint16_t wave[] = {500u, 620u, 500u, 380u};
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
  exam_timer_start(EXAM_TIMER0);
```

**Minimal example**

```c
exam_dac_init();
(void)exam_dac_write(512);
```

> **Common mistake:** Writing samples before selecting the DAC function on P0.26.

**Exam use:** Initialize once before waveform or loudspeaker output.

#### `exam_dac_write`

Write one validated 10-bit DAC sample while preserving DACR.BIAS.

**Declaration**

```c
exam_status_t exam_dac_write(int32_t sample);
```

- **Preconditions:** Call exam_dac_init() first.
- **Returns:** EXAM_OK or EXAM_OUT_OF_RANGE for a negative value or a value above 1023.
- **Side effects:** Updates DACR VALUE bits 15:6 and preserves BIAS bit 16.
- **Call context:** Bounded register write suitable for a short periodic waveform-update handler when that is the required owner.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `sample` | in | Signed integer sample in the inclusive range 0..1023. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `0` | Silence/terminate output. | Observed in reviewed solutions — `2025-02-12-arm1-q2`, `2026-02-18-arm1-q2` |
| `500` | Midscale DC offset around which signed waveform terms are centered. | Observed in 2025 sine/cosine solutions — `2025-02-12-arm1-q2`, `2025-02-12-arm2-q2` |
| `0..1023` | Only accepted hardware sample range. | API range |

**Scenario: Stream validated DAC samples from a periodic timer**

The 1263-tick Timer0 schedule, samples centered around 500, and zero termination are observed in the reviewed 2025 sine solution. Sources: `2025-02-12-arm1-q2`.

```c
static const uint16_t wave[] = {500u, 620u, 500u, 380u};
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
  exam_timer_start(EXAM_TIMER0);
```

**Scenario: Periodic waveform timer plus one-shot duration timer**

Observed structure in both reviewed 2026-02-18 three-timer solutions; thresholds are calculated by the paper's algorithm rather than guessed constants. Sources: `2026-02-18-arm1-q2`, `2026-02-18-arm2-q2`.

```c
exam_timer_stop(EXAM_TIMER1);
exam_timer_reset(EXAM_TIMER1);
exam_timer_config_ticks(EXAM_TIMER1, waveform_threshold,
                        EXAM_TIMER_PERIODIC);
exam_timer_stop(EXAM_TIMER2);
exam_timer_reset(EXAM_TIMER2);
exam_timer_config_ticks(EXAM_TIMER2, duration_threshold,
                        EXAM_TIMER_ONE_SHOT);
exam_timer_start(EXAM_TIMER1);
exam_timer_start(EXAM_TIMER2);
```

**Minimal example**

```c
(void)exam_dac_write(wave[index]);
```

> **Common mistake:** Passing an 8-bit value without intentionally scaling it, or allowing signed waveform values to go negative.

**Exam use:** Clamp or offset the algorithm's result into 0..1023 before writing.

### Events

Transfer bit flags safely between interrupt handlers and foreground code, or protect a short compound update.

#### `exam_events_set`

Atomically OR application-defined bits into the general interrupt-to-main event word.

**Declaration**

```c
void exam_events_set(uint32_t bits);
```

- **Preconditions:** Define non-overlapping event masks in question code and call exam_init() before use.
- **Returns:** No value.
- **Side effects:** Adds bits to the private event word without clearing existing events.
- **Call context:** Designed for short IRQ publication; uses a nested-safe PRIMASK save/restore critical section.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `bits` | in | One or more question-defined event bits to publish; zero has no effect. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `1u << 0` | Typical first application event bit; assign one non-overlapping bit per event. | Observed event pattern — `2024-02-28-q2`, `2026-06-25-arm1-q2` |

**Scenario: Publish a half-second Timer0 event to the foreground**

Observed in the reviewed 2024-02-28 shortest-path solution. Sources: `2024-02-28-q2`.

```c
#define EVENT_HALF_SECOND (1u << 0)

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
}
```

**Scenario: Poll joystick press edges every 10 ms**

Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
static uint32_t previous_joystick;
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
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();
```

**Minimal example**

```c
#define EVENT_TICK (1u << 0)
void TIMER0_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER0); exam_events_set(EVENT_TICK); }
```

> **Common mistake:** Using the same bit for unrelated events or doing long foreground work directly in the IRQ instead.

**Exam use:** Publish state in the handler; take and process it in main.

#### `exam_events_take`

Atomically obtain and clear selected application event bits.

**Declaration**

```c
uint32_t exam_events_take(uint32_t mask);
```

- **Preconditions:** Events are normally produced with exam_events_set().
- **Returns:** The subset of mask that was pending at the protected snapshot.
- **Side effects:** Clears exactly the returned selected bits; unrelated event bits are preserved.
- **Call context:** Foreground consumer. New IRQ events published after the snapshot remain pending.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `mask` | in | Bits to test and consume. Bits outside mask remain pending. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Combined event mask` | Take once, then test all returned bits in foreground. | Observed event pattern — `2024-02-28-q2`, `2026-06-25-arm1-q2` |

**Scenario: Publish a half-second Timer0 event to the foreground**

Observed in the reviewed 2024-02-28 shortest-path solution. Sources: `2024-02-28-q2`.

```c
#define EVENT_HALF_SECOND (1u << 0)

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
}
```

**Scenario: Poll joystick press edges every 10 ms**

Observed in the reviewed 2025 rhythm and 2026 Bulls-and-Cows/Mastermind solutions. Sources: `2025-07-01-arm1-q3`, `2026-06-25-arm1-q2`.

```c
static uint32_t previous_joystick;
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
if (exam_rit_config_ms(10u) == EXAM_OK) exam_rit_start();
```

**Minimal example**

```c
uint32_t events = exam_events_take(EVENT_TICK | EVENT_ADC);
```

> **Common mistake:** Taking the same bit in multiple places and making event ownership nondeterministic.

**Exam use:** Take a combined mask once per loop, then branch on the local result.

#### `exam_critical_enter`

Save PRIMASK, disable maskable interrupts, and issue a data-memory barrier.

**Declaration**

```c
uint32_t exam_critical_enter(void);
```

- **Preconditions:** Use only for a very short compound access that cannot use a higher-level atomic helper.
- **Returns:** The previous PRIMASK value that must be passed unchanged to exam_critical_exit().
- **Side effects:** Masks normal interrupts while preserving whether they were already masked.
- **Call context:** No blocking work, loops, peripheral waits, or early returns may occur before the matching exit.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Returned PRIMASK key` | Save exactly; never replace it with a guessed 0 or 1. | Observed protected snapshot pattern — `2026-06-25-arm1-q2` |

**Scenario: Take a two-word IRQ snapshot without tearing**

The protected snapshot pattern is observed in the reviewed 2026 game solutions. Sources: `2026-06-25-arm1-q2`.

```c
uint32_t saved = exam_critical_enter();
uint32_t edges = joystick_press_edges;
joystick_press_edges = 0u;
exam_critical_exit(saved);
/* Process edges after interrupts are restored. */
```

**Minimal example**

```c
uint32_t key = exam_critical_enter();
shared_pair.a = a; shared_pair.b = b;
exam_critical_exit(key);
```

> **Common mistake:** Calling __enable_irq() unconditionally afterward or losing the saved PRIMASK on an early return.

**Exam use:** Prefer exam_events_set/take for bit events; use this only for a short multi-step shared update.

#### `exam_critical_exit`

Restore the exact PRIMASK state saved by exam_critical_enter().

**Declaration**

```c
void exam_critical_exit(uint32_t saved_primask);
```

- **Preconditions:** Must pair with an earlier exam_critical_enter() on the same control path.
- **Returns:** No value.
- **Side effects:** Issues a data-memory barrier and restores prior interrupt masking, including an already-masked state.
- **Call context:** Call promptly after the protected operations.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `saved_primask` | in | Unmodified return value from the matching exam_critical_enter() call. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `saved` | Pass the unchanged value returned by the matching enter call. | Observed protected snapshot pattern — `2026-06-25-arm1-q2` |

**Scenario: Take a two-word IRQ snapshot without tearing**

The protected snapshot pattern is observed in the reviewed 2026 game solutions. Sources: `2026-06-25-arm1-q2`.

```c
uint32_t saved = exam_critical_enter();
uint32_t edges = joystick_press_edges;
joystick_press_edges = 0u;
exam_critical_exit(saved);
/* Process edges after interrupts are restored. */
```

**Minimal example**

```c
uint32_t key = exam_critical_enter();
/* bounded shared update */
exam_critical_exit(key);
```

> **Common mistake:** Passing 0 instead of the saved value and accidentally enabling interrupts inside an outer critical region.

**Exam use:** Every path after enter must reach exactly one matching exit.

### Faults

Configure Cortex-M3 fault trapping and preserve a debugger-readable exception snapshot when fault wrappers are enabled.

#### `exam_faults_configure`

Enable or disable configurable Cortex-M3 faults and the divide-by-zero and unaligned-access traps.

**Declaration**

```c
void exam_faults_configure(uint8_t enable_configurable_faults, uint8_t trap_divide_by_zero, uint8_t trap_unaligned);
```

- **Preconditions:** If the API must own fault handlers, define EXAM_ENABLE_FAULT_HANDLERS=1 for the complete Keil target, not only in main.c.
- **Returns:** No value.
- **Side effects:** Updates SCB->SHCSR and SCB->CCR, then executes DSB and ISB.
- **Call context:** Foreground setup before deliberately testing faults.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `enable_configurable_faults` | in | Nonzero enables MemManage, BusFault, and UsageFault; zero disables them. |
| `trap_divide_by_zero` | in | Nonzero sets CCR.DIV_0_TRP; zero clears it. |
| `trap_unaligned` | in | Nonzero sets CCR.UNALIGN_TRP; zero clears it. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `1, 1, 1` | Enable configurable faults plus divide-by-zero and unaligned traps for a deliberate debugger exercise. | Safe illustrative configuration, not used by reviewed solutions |
| `0, 0, 0` | Disable those optional traps. | API behavior |

**Scenario: Capture a deliberate divide-by-zero fault for debugger inspection**

Safe debugger scenario based on the current opt-in fault API; not used by the reviewed solved exams.

```c
/* Define EXAM_ENABLE_FAULT_HANDLERS=1 for the whole target. */
exam_init();
exam_fault_snapshot_clear();
exam_faults_configure(1u, 1u, 1u);
/* A deliberate divide-by-zero now reaches the wrapper and never returns.
   Inspect exam_fault_snapshot only when exam_fault_snapshot_valid == 1. */
```

**Minimal example**

```c
exam_fault_snapshot_clear();
exam_faults_configure(1u, 1u, 1u);
```

> **Common mistake:** Enabling traps without enabling/providing the intended handlers, or defining two owners for the same fault vector.

**Exam use:** Fault capture stops forever for debugger inspection; it is not a recovery mechanism.

#### `exam_fault_snapshot_clear`

Mark the debugger fault snapshot as invalid before a new test.

**Declaration**

```c
void exam_fault_snapshot_clear(void);
```

- **Preconditions:** None.
- **Returns:** No value.
- **Side effects:** Atomically writes exam_fault_snapshot_valid=0; stored snapshot words are not erased.
- **Call context:** Foreground setup before triggering a fault.

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Before each deliberate fault` | Marks old debugger state invalid without zeroing every field. | Recommended debugger workflow |

**Scenario: Capture a deliberate divide-by-zero fault for debugger inspection**

Safe debugger scenario based on the current opt-in fault API; not used by the reviewed solved exams.

```c
/* Define EXAM_ENABLE_FAULT_HANDLERS=1 for the whole target. */
exam_init();
exam_fault_snapshot_clear();
exam_faults_configure(1u, 1u, 1u);
/* A deliberate divide-by-zero now reaches the wrapper and never returns.
   Inspect exam_fault_snapshot only when exam_fault_snapshot_valid == 1. */
```

**Minimal example**

```c
exam_fault_snapshot_clear();
```

> **Common mistake:** Assuming the snapshot structure itself is zero-filled after this call.

**Exam use:** Check the valid flag in the debugger before trusting snapshot fields.

#### `exam_fault_capture_from_exception`

Copy the stacked exception frame and Cortex-M3 fault registers into persistent debugger state, then stop forever.

**Declaration**

```c
void exam_fault_capture_from_exception(exam_exception_frame_t *frame, uint32_t exc_return);
```

- **Preconditions:** Normally reached only through the optional API fault wrappers or an equivalent correct naked assembly wrapper.
- **Returns:** Does not return.
- **Side effects:** Fills exam_fault_snapshot, sets exam_fault_snapshot_valid after barriers, and loops on __NOP() forever.
- **Call context:** Fault-handler terminal path. Do not call as a normal C function to simulate recovery.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `frame` | in | Non-null pointer to the hardware-stacked r0-r3, r12, lr, pc, and xPSR frame. |
| `exc_return` | in | LR/EXC_RETURN value supplied by the naked fault wrapper. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Wrapper-provided frame and EXC_RETURN` | Never invent these arguments in normal foreground code. | Exception ABI contract |

**Scenario: Capture a deliberate divide-by-zero fault for debugger inspection**

Safe debugger scenario based on the current opt-in fault API; not used by the reviewed solved exams.

```c
/* Define EXAM_ENABLE_FAULT_HANDLERS=1 for the whole target. */
exam_init();
exam_fault_snapshot_clear();
exam_faults_configure(1u, 1u, 1u);
/* A deliberate divide-by-zero now reaches the wrapper and never returns.
   Inspect exam_fault_snapshot only when exam_fault_snapshot_valid == 1. */
```

**Minimal example**

```c
/* Enable EXAM_ENABLE_FAULT_HANDLERS for the whole target; wrappers call this automatically. */
```

> **Common mistake:** Calling it with an ordinary local struct or expecting execution to resume.

**Exam use:** Inspect exception_number, frame.pc, CFSR, HFSR, BFAR, and MMFAR in the debugger.

### SVC

Decode an SVC immediate and pass the stacked exception frame to an overridable dispatcher.

#### `exam_svc_capture_from_exception`

Decode the SVC immediate from the instruction before stacked PC and dispatch the service with the stacked frame.

**Declaration**

```c
void exam_svc_capture_from_exception(exam_exception_frame_t *frame);
```

- **Preconditions:** Use the optional API SVC wrapper or an equivalent correct wrapper. The stacked PC must follow a 16-bit SVC instruction.
- **Returns:** No direct C return; results are communicated through the stacked frame.
- **Side effects:** Reads byte PC[-2] as the service number and calls exam_svc_dispatch(service_number, frame).
- **Call context:** SVC-handler bridge; keep dispatch work bounded and define one SVC owner.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `frame` | in/out | Hardware-stacked exception frame. The dispatcher may alter fields such as r0 to return a service result. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Wrapper-provided frame` | The bridge reads the SVC immediate at stacked PC minus two bytes. | Cortex-M3 exception contract |

**Scenario: Return an SVC service result through stacked r0**

Illustrative current-API adaptation of the SVC topic in the reviewed 2023-02-24 exam. Sources: `2023-02-24-q2`.

```c
/* Define EXAM_ENABLE_SVC_HANDLER=1 for the whole target. */
void exam_svc_dispatch(uint8_t service_number,
                       exam_exception_frame_t *frame) {
  if (service_number == 1u) {
    frame->r0 = frame->r0 + frame->r1;
  }
}
```

**Minimal example**

```c
/* With EXAM_ENABLE_SVC_HANDLER=1, SVC_Handler calls this bridge automatically. */
```

> **Common mistake:** Reading the immediate from frame->pc instead of the SVC instruction immediately before it.

**Exam use:** Override exam_svc_dispatch(), not the capture bridge, for question-specific services.

#### `exam_svc_dispatch`

Provide the weak overridable hook that implements question-specific SVC services.

**Declaration**

```c
void exam_svc_dispatch(uint8_t service_number, exam_exception_frame_t *frame);
```

- **Preconditions:** Provide one strong definition with the exact prototype when the question uses the API SVC bridge.
- **Returns:** No direct C return.
- **Side effects:** The default weak implementation does nothing. A user override may update the stacked frame or controlled application state.
- **Call context:** Runs in handler mode; keep services bounded and avoid blocking peripheral work.

| Parameter | Direction | Meaning and valid values |
| --- | --- | --- |
| `service_number` | in | 8-bit immediate encoded by the SVC instruction. |
| `frame` | in/out | Pointer to the hardware-stacked frame; update frame fields to return results. |

**Typical exam values**

| Suggested value | When to use | Evidence |
| --- | --- | --- |
| `Service 1` | Illustrative add service returning through stacked r0; actual service numbers come from the paper. | Safe illustration based on the 2023 SVC topic — `2023-02-24-q2` |

**Scenario: Return an SVC service result through stacked r0**

Illustrative current-API adaptation of the SVC topic in the reviewed 2023-02-24 exam. Sources: `2023-02-24-q2`.

```c
/* Define EXAM_ENABLE_SVC_HANDLER=1 for the whole target. */
void exam_svc_dispatch(uint8_t service_number,
                       exam_exception_frame_t *frame) {
  if (service_number == 1u) {
    frame->r0 = frame->r0 + frame->r1;
  }
}
```

**Minimal example**

```c
void exam_svc_dispatch(uint8_t n, exam_exception_frame_t *f) {
  if (n == 1u) f->r0 = f->r0 + f->r1;
}
```

> **Common mistake:** Defining a mismatched prototype or also defining a competing SVC_Handler.

**Exam use:** Return a scalar service result by writing frame->r0.
