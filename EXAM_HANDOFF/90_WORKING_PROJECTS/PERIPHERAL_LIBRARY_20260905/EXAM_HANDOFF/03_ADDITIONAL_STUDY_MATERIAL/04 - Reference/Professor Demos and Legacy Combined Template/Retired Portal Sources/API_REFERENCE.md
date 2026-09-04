# Complete `exam_api` reference

This is the complete beginner-facing API from the official two-file template. The header remains authoritative.

## Start and ownership rules

- Call `exam_init()` once at the beginning of `main()`.
- `exam_timer_periodic_ms()`, `exam_timer_periodic_hz()`, `exam_timer_free_running_start()`, `exam_rit_start()`, `exam_systick_periodic_ms()`, `exam_buttons_start()`, `exam_joystick_start()` and `exam_dac_play()` start their respective service.
- `exam_timer_match()` configures a match but does not start the timer; call `exam_timer_start()` after all required matches are configured.
- A callback does not create another native IRQ handler. Keep exactly one standard handler owner per peripheral.
- Use direct registers or the professor function when the question explicitly requires them; the helper API is not a substitute for exact register work.
- Only use `__WFI()` or an idle mode that sleeps after at least one enabled interrupt source has been started.

## How data moves through the API

- **Value:** `exam_led_on(0u)` copies the value into the call.
- **Output pointer:** `exam_potentiometer_read_raw(&raw)` passes the address where the result is written. Use the result only after `EXAM_OK`.
- **Callback:** `exam_buttons_start(on_button)` passes the function name without parentheses so the service can call it later.
- **Mask:** `pressed & EXAM_JOY_SELECT` tests one bit while preserving the other state bits.
- **Array:** pass a pointer plus an element count; keep asynchronously used data `static` or global.
- **Status:** check the returned `exam_status_t` before assuming setup or a read succeeded.

The current joystick callback receives `(current, changed)`. This is not the separate combined-template `(previous, current)` contract.

For C-to-assembly calls, the first four scalar/pointer arguments use R0–R3, later arguments use the stack, and a 32-bit result returns in R0.

## Current-source guarantee

Every function, explanation and example in this page is generated against the current official two-file header. Generation fails if the current declarations and documentation differ. Obsolete project-local API names are excluded from this student-facing reference.
## Public functions

### Core

#### `exam_init()`

**Exact declaration:** `void exam_init(void)`

Initialize the system clock, LEDs, fault support and API state. Call once at the start of main.

```c
int main(void) {
  exam_init();
  for (;;) exam_idle();
}
```

#### `exam_idle()`

**Exact declaration:** `void exam_idle(void)`

Run the configured idle policy. It is a no-op by default; a build option may make it use WFI.

```c
for (;;) {
  exam_idle();  /* No-op by default; may use WFI if configured. */
}
```

### LEDs

#### `exam_led_set()`

**Exact declaration:** `exam_status_t exam_led_set(uint8_t index, bool on)`

Set one logical LED index 0–7 on or off; returns EXAM_RANGE for an invalid index.

```c
exam_status_t status = exam_led_set(2u, true);
if (status != EXAM_OK) { /* index was not 0..7 */ }
```

#### `exam_led_on()`

**Exact declaration:** `exam_status_t exam_led_on(uint8_t index)`

Turn on one logical LED index 0–7.

```c
(void)exam_led_on(0u);  /* Turn logical LED 0 on. */
```

#### `exam_led_off()`

**Exact declaration:** `exam_status_t exam_led_off(uint8_t index)`

Turn off one logical LED index 0–7.

```c
(void)exam_led_off(0u); /* Turn logical LED 0 off. */
```

#### `exam_led_toggle()`

**Exact declaration:** `exam_status_t exam_led_toggle(uint8_t index)`

Toggle one logical LED index 0–7.

```c
(void)exam_led_toggle(3u); /* Flip logical LED 3. */
```

#### `exam_led_from_board_label()`

**Exact declaration:** `exam_status_t exam_led_from_board_label(uint8_t label, uint8_t *index)`

Translate physical board label 4–11 to logical index 0–7 through an output pointer.

```c
uint8_t led_index;
if (exam_led_from_board_label(4u, &led_index) == EXAM_OK)
  (void)exam_led_on(led_index);
```

#### `exam_leds_write()`

**Exact declaration:** `exam_status_t exam_leds_write(uint8_t mask)`

Write all eight logical LEDs from an 8-bit mask.

```c
(void)exam_leds_write(0x55u); /* LEDs 0,2,4,6 on. */
```

#### `exam_leds_read()`

**Exact declaration:** `uint8_t exam_leds_read(void)`

Return the current logical eight-LED mask.

```c
uint8_t current_leds = exam_leds_read();
```

#### `exam_leds_clear()`

**Exact declaration:** `void exam_leds_clear(void)`

Turn all user LEDs off.

```c
exam_leds_clear(); /* All eight user LEDs off. */
```

#### `exam_leds_fill()`

**Exact declaration:** `void exam_leds_fill(void)`

Turn all user LEDs on.

```c
exam_leds_fill(); /* All eight user LEDs on. */
```

#### `exam_leds_bar()`

**Exact declaration:** `exam_status_t exam_leds_bar(uint32_t value, uint32_t maximum)`

Display value/maximum as an eight-LED bar graph.

```c
(void)exam_leds_bar(75u, 100u); /* Show 75% as a bar. */
```

### Buttons

#### `exam_buttons_start()`

**Exact declaration:** `exam_status_t exam_buttons_start(exam_button_callback_t callback)`

Start RIT-backed debounced processing for INT0, KEY1 and KEY2 and register one callback.

```c
static void on_button(exam_button_t button, exam_button_event_t event) {
  if (button == EXAM_BUTTON_INT0 && event == EXAM_PRESS)
    exam_events_set(1u << 0);
}
/* After exam_init(): */
exam_status_t status = exam_buttons_start(on_button);
```

#### `exam_button_irq_start()`

**Exact declaration:** `exam_status_t exam_button_irq_start(exam_button_t button)`

Enable the native external interrupt for one button when the ownership mode allows it.

```c
/* Only when the selected IRQ ownership mode permits it. */
exam_status_t status = exam_button_irq_start(EXAM_BUTTON_INT0);
```

#### `exam_buttons_confirmation_ms()`

**Exact declaration:** `void exam_buttons_confirmation_ms(uint32_t milliseconds)`

Set the debounce confirmation interval in milliseconds.

```c
exam_buttons_confirmation_ms(20u); /* Require 20 ms stable input. */
```

#### `exam_button_is_down()`

**Exact declaration:** `uint8_t exam_button_is_down(exam_button_t button)`

Return whether one logical button is currently pressed.

```c
if (exam_button_is_down(EXAM_BUTTON_KEY1)) {
  (void)exam_led_on(1u);
}
```

#### `exam_buttons_down()`

**Exact declaration:** `uint32_t exam_buttons_down(void)`

Return the current logical button mask.

```c
uint32_t down = exam_buttons_down();
if (down & (1u << EXAM_BUTTON_KEY2)) { /* KEY2 is held. */ }
```

#### `exam_button_pressed_edges()`

**Exact declaration:** `uint32_t exam_button_pressed_edges(uint32_t current, uint32_t changed)`

From current and changed masks, keep only newly pressed button bits.

```c
uint32_t pressed = exam_button_pressed_edges(current, changed);
if (pressed & (1u << EXAM_BUTTON_KEY1)) { /* new KEY1 press */ }
```

#### `exam_button_released_edges()`

**Exact declaration:** `uint32_t exam_button_released_edges(uint32_t current, uint32_t changed)`

From current and changed masks, keep only newly released button bits.

```c
uint32_t released = exam_button_released_edges(current, changed);
if (released & (1u << EXAM_BUTTON_KEY1)) { /* new KEY1 release */ }
```

### Joystick

#### `exam_joystick_start()`

**Exact declaration:** `exam_status_t exam_joystick_start(exam_joystick_callback_t callback)`

Start RIT-backed joystick scanning and register one callback receiving current and changed masks.

```c
static void on_joystick(uint32_t current, uint32_t changed) {
  uint32_t pressed = exam_joystick_pressed_edges(current, changed);
  if (pressed & EXAM_JOY_SELECT) exam_events_set(1u << 1);
}
/* After exam_init(): */
exam_status_t status = exam_joystick_start(on_joystick);
```

#### `exam_joystick_down()`

**Exact declaration:** `uint32_t exam_joystick_down(void)`

Return the current logical joystick direction/select mask.

```c
uint32_t joystick = exam_joystick_down();
if (joystick & EXAM_JOY_UP) { /* UP is held. */ }
```

#### `exam_joystick_pressed_edges()`

**Exact declaration:** `uint32_t exam_joystick_pressed_edges(uint32_t current, uint32_t changed)`

From current and changed masks, keep only newly pressed joystick bits.

```c
uint32_t pressed = exam_joystick_pressed_edges(current, changed);
if (pressed & EXAM_JOY_RIGHT) { /* new RIGHT press */ }
```

#### `exam_joystick_released_edges()`

**Exact declaration:** `uint32_t exam_joystick_released_edges(uint32_t current, uint32_t changed)`

From current and changed masks, keep only newly released joystick bits.

```c
uint32_t released = exam_joystick_released_edges(current, changed);
if (released & EXAM_JOY_RIGHT) { /* RIGHT was released */ }
```

#### `exam_joystick_first()`

**Exact declaration:** `uint32_t exam_joystick_first(void)`

Return the first joystick movement recorded by the helper.

```c
uint32_t first = exam_joystick_first();
if (first == EXAM_JOY_LEFT) { /* LEFT was first. */ }
```

#### `exam_joystick_reset_first()`

**Exact declaration:** `void exam_joystick_reset_first(void)`

Clear the stored first joystick movement.

```c
exam_joystick_reset_first(); /* Start recording a new first move. */
```

### Timers

#### `exam_timer_periodic_ms()`

**Exact declaration:** `exam_status_t exam_timer_periodic_ms(exam_timer_t timer, uint32_t milliseconds, exam_timer_callback_t callback)`

Configure and start Timer0–Timer3 as a periodic interrupt in milliseconds and register its callback.

```c
static void on_timer(exam_timer_t timer, uint32_t flags) {
  (void)timer; (void)flags;
  exam_events_set(1u << 2);
}
/* Timer3 is API-owned in the supplied configuration. */
exam_status_t status = exam_timer_periodic_ms(EXAM_TIMER_3, 1000u, on_timer);
```

#### `exam_timer_periodic_hz()`

**Exact declaration:** `exam_status_t exam_timer_periodic_hz(exam_timer_t timer, uint32_t hertz, exam_timer_callback_t callback)`

Configure and start Timer0–Timer3 as a periodic interrupt at the requested hertz and register its callback.

```c
static void on_sample_tick(exam_timer_t timer, uint32_t flags) {
  (void)timer; (void)flags;
  exam_events_set(1u << 3);
}
/* Timer3 is API-owned in the supplied configuration. */
exam_status_t status = exam_timer_periodic_hz(EXAM_TIMER_3, 100u, on_sample_tick);
```

#### `exam_timer_free_running_start()`

**Exact declaration:** `exam_status_t exam_timer_free_running_start(exam_timer_t timer, uint8_t divider, uint32_t prescaler)`

Set clock divider and prescaler, reset the counter, then start a genuine free-running timer.

```c
/* PCLK divider 4, PR=24: TC advances every 1 us at 100 MHz CCLK. */
exam_status_t status = exam_timer_free_running_start(EXAM_TIMER_3, 4u, 24u);
```

#### `exam_timer_clock_divider()`

**Exact declaration:** `exam_status_t exam_timer_clock_divider(exam_timer_t timer, uint8_t divider)`

Set the timer peripheral-clock divider; use before starting or while safely stopped.

```c
(void)exam_timer_stop(EXAM_TIMER_2);
exam_status_t status = exam_timer_clock_divider(EXAM_TIMER_2, 4u);
```

#### `exam_timer_prescaler()`

**Exact declaration:** `exam_status_t exam_timer_prescaler(exam_timer_t timer, uint32_t prescaler)`

Set the timer PR value; TC advances at PCLK/(PR+1).

```c
(void)exam_timer_stop(EXAM_TIMER_2);
exam_status_t status = exam_timer_prescaler(EXAM_TIMER_2, 24999u);
```

#### `exam_timer_match()`

**Exact declaration:** `exam_status_t exam_timer_match(exam_timer_t timer, uint8_t match, uint32_t ticks, uint32_t actions)`

Configure MR0–MR3 ticks and interrupt/reset/stop action bits; this call does not itself start the timer.

```c
/* Stop first; configure MR0 for interrupt+reset, then start. */
(void)exam_timer_stop(EXAM_TIMER_0);
(void)exam_timer_reset(EXAM_TIMER_0);
exam_status_t status = exam_timer_match(
    EXAM_TIMER_0, 0u, 25000u,
    EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET);
if (status == EXAM_OK) (void)exam_timer_start(EXAM_TIMER_0);
```

#### `exam_timer_start()`

**Exact declaration:** `exam_status_t exam_timer_start(exam_timer_t timer)`

Start the selected standard timer.

```c
/* Start only after clock, prescaler and all matches are configured. */
exam_status_t status = exam_timer_start(EXAM_TIMER_0);
```

#### `exam_timer_stop()`

**Exact declaration:** `exam_status_t exam_timer_stop(exam_timer_t timer)`

Stop the selected standard timer.

```c
exam_status_t status = exam_timer_stop(EXAM_TIMER_0);
```

#### `exam_timer_reset()`

**Exact declaration:** `exam_status_t exam_timer_reset(exam_timer_t timer)`

Reset the selected standard timer counter.

```c
(void)exam_timer_stop(EXAM_TIMER_0);
exam_status_t status = exam_timer_reset(EXAM_TIMER_0);
```

#### `exam_timer_read()`

**Exact declaration:** `uint32_t exam_timer_read(exam_timer_t timer)`

Read the selected timer counter; an invalid timer returns zero.

```c
uint32_t elapsed_ticks = exam_timer_read(EXAM_TIMER_2);
```

#### `exam_timer_match_happened()`

**Exact declaration:** `uint8_t exam_timer_match_happened(uint32_t flags, uint8_t match)`

Test one MR0–MR3 pending bit in the callback flag snapshot.

```c
static void on_timer(exam_timer_t timer, uint32_t flags) {
  (void)timer;
  if (exam_timer_match_happened(flags, 0u)) exam_events_set(1u << 4);
}
```

#### `exam_timer_capture_happened()`

**Exact declaration:** `uint8_t exam_timer_capture_happened(uint32_t flags, uint8_t capture)`

Test one CR0–CR1 pending bit in the callback flag snapshot.

```c
static void on_timer(exam_timer_t timer, uint32_t flags) {
  (void)timer;
  if (exam_timer_capture_happened(flags, 0u)) exam_events_set(1u << 5);
}
```

### RIT and SysTick

#### `exam_rit_start()`

**Exact declaration:** `exam_status_t exam_rit_start(void)`

Start the shared RIT scheduler explicitly.

```c
exam_status_t status = exam_rit_start();
if (status == EXAM_OK) { /* RIT ticks can now advance. */ }
```

#### `exam_rit_stop()`

**Exact declaration:** `void exam_rit_stop(void)`

Stop the shared RIT scheduler.

```c
exam_rit_stop();
```

#### `exam_rit_ticks()`

**Exact declaration:** `uint32_t exam_rit_ticks(void)`

Return the RIT scheduler tick count.

```c
uint32_t now = exam_rit_ticks();
```

#### `exam_systick_periodic_ms()`

**Exact declaration:** `exam_status_t exam_systick_periodic_ms(uint32_t milliseconds)`

Configure and start periodic SysTick in milliseconds; the 24-bit hardware bound is validated below.

```c
/* Starts SysTick with a 1 ms period. */
exam_status_t status = exam_systick_periodic_ms(1u);
```

#### `exam_systick_ticks()`

**Exact declaration:** `uint32_t exam_systick_ticks(void)`

Return the SysTick software tick count.

```c
uint32_t start = exam_systick_ticks();
while ((exam_systick_ticks() - start) < 100u) { /* wait 100 ticks */ }
```

### ADC and potentiometer

#### `exam_potentiometer_start()`

**Exact declaration:** `exam_status_t exam_potentiometer_start(void)`

Initialize ADC channel 5 for the board potentiometer and start its first software conversion.

```c
exam_status_t status = exam_potentiometer_start();
```

#### `exam_potentiometer_read_raw()`

**Exact declaration:** `exam_status_t exam_potentiometer_read_raw(uint16_t *value)`

Read the potentiometer as a 12-bit raw sample through an output pointer.

```c
uint16_t raw;
if (exam_potentiometer_read_raw(&raw) == EXAM_OK) {
  /* raw is now 0..4095 */
}
```

#### `exam_potentiometer_read_percent()`

**Exact declaration:** `exam_status_t exam_potentiometer_read_percent(uint8_t *percent)`

Read the potentiometer scaled and rounded to 0–100 percent.

```c
uint8_t percent;
if (exam_potentiometer_read_percent(&percent) == EXAM_OK)
  (void)exam_leds_bar(percent, 100u);
```

#### `exam_adc_read_raw()`

**Exact declaration:** `exam_status_t exam_adc_read_raw(uint8_t channel, uint16_t *value)`

Read ADC channel 0–7 as a 12-bit raw value through an output pointer.

```c
uint16_t raw;
if (exam_adc_read_raw(3u, &raw) == EXAM_OK) {
  /* ADC channel 3 sample is in raw. */
}
```

### DAC and sound

#### `exam_dac_write_raw()`

**Exact declaration:** `exam_status_t exam_dac_write_raw(uint16_t value)`

Initialize the DAC if needed and write a raw 10-bit value 0–1023.

```c
exam_status_t status = exam_dac_write_raw(512u); /* Mid-scale. */
```

#### `exam_dac_write_percent()`

**Exact declaration:** `exam_status_t exam_dac_write_percent(uint8_t percent)`

Write a DAC level from 0–100 percent, scaled to the 10-bit range.

```c
exam_status_t status = exam_dac_write_percent(25u);
```

#### `exam_dac_silence()`

**Exact declaration:** `void exam_dac_silence(void)`

Initialize the DAC if needed and drive the speaker output to its silence level.

```c
exam_dac_silence();
```

#### `exam_dac_play()`

**Exact declaration:** `exam_status_t exam_dac_play(const uint16_t *samples, uint32_t count, uint32_t sample_hz, exam_timer_t timer)`

Play the supplied sample table once through the DAC at `sample_hz`, then stop the timer and silence the output. The sample array must remain valid until playback finishes. Restart playback from foreground code when deliberate looping is required.

```c
static const uint16_t wave[] = {0u, 256u, 512u, 768u, 1023u, 768u, 512u, 256u};
exam_status_t status = exam_dac_play(
    wave, (uint32_t)(sizeof wave / sizeof wave[0]), 8000u, EXAM_TIMER_3);
```

#### `exam_dac_stop()`

**Exact declaration:** `exam_status_t exam_dac_stop(void)`

Stop helper-owned DAC sample playback.

```c
exam_status_t status = exam_dac_stop();
```

### Events, critical sections and self-test

#### `exam_events_set()`

**Exact declaration:** `void exam_events_set(uint32_t bits)`

Atomically set foreground event bits, normally from an interrupt callback.

```c
/* Safe from a short callback/ISR. */
exam_events_set(1u << 0);
```

#### `exam_events_take()`

**Exact declaration:** `uint32_t exam_events_take(uint32_t mask)`

Atomically return and clear the requested foreground event bits.

```c
uint32_t events = exam_events_take((1u << 0) | (1u << 1));
if (events & (1u << 0)) { /* foreground work */ }
```

#### `exam_critical_enter()`

**Exact declaration:** `uint32_t exam_critical_enter(void)`

Disable interrupts and return the previous PRIMASK value for later restoration.

```c
uint32_t saved = exam_critical_enter();
shared_value++;
exam_critical_exit(saved);
```

#### `exam_critical_exit()`

**Exact declaration:** `void exam_critical_exit(uint32_t saved_primask)`

Restore the PRIMASK value returned by exam_critical_enter.

```c
uint32_t saved = exam_critical_enter();
/* short protected update */
exam_critical_exit(saved);
```

#### `exam_self_test()`

**Exact declaration:** `uint32_t exam_self_test(void)`

Run the non-destructive board/API self-test and return its result bitmask.

```c
uint32_t failures = exam_self_test();
if (failures == 0u) { /* non-destructive checks passed */ }
```

## Public types

- `typedef board_status_t exam_status_t;`
- `typedef board_button_t exam_button_t;`
- `typedef button_event_t exam_button_event_t;`
- `typedef adc_sample_t exam_adc_sample_t;`
- `typedef svc_context_t exam_svc_context_t;`
- `typedef fault_snapshot_t exam_fault_snapshot_t;`
- `typedef enum { EXAM_TIMER_0 = 0, EXAM_TIMER_1 = 1, EXAM_TIMER_2 = 2, EXAM_TIMER_3 = 3 } exam_timer_t;`
- `typedef void (*exam_button_callback_t)(exam_button_t button, exam_button_event_t event);`
- `typedef void (*exam_joystick_callback_t)(uint32_t current, uint32_t changed);`
- `typedef void (*exam_timer_callback_t)(exam_timer_t timer, uint32_t flags);`

## Public constants

- `#define EXAM_API_H`
- `#define EXAM_OK        BOARD_OK`
- `#define EXAM_INVALID   BOARD_INVALID`
- `#define EXAM_BUSY      BOARD_BUSY`
- `#define EXAM_RANGE     BOARD_RANGE`
- `#define EXAM_NOT_READY BOARD_NOT_READY`
- `#define EXAM_NOT_ENABLED BOARD_NOT_ENABLED`
- `#define EXAM_BUTTON_INT0 BOARD_BUTTON_INT0`
- `#define EXAM_BUTTON_KEY1 BOARD_BUTTON_KEY1`
- `#define EXAM_BUTTON_KEY2 BOARD_BUTTON_KEY2`
- `#define EXAM_PRESS       BUTTON_EVENT_PRESS`
- `#define EXAM_RELEASE     BUTTON_EVENT_RELEASE`
- `#define EXAM_JOY_SELECT JOYSTICK_SELECT`
- `#define EXAM_JOY_DOWN   JOYSTICK_DOWN`
- `#define EXAM_JOY_LEFT   JOYSTICK_LEFT`
- `#define EXAM_JOY_RIGHT  JOYSTICK_RIGHT`
- `#define EXAM_JOY_UP     JOYSTICK_UP`
- `#define EXAM_TIMER_INTERRUPT TIMER_ACTION_INTERRUPT`
- `#define EXAM_TIMER_RESET     TIMER_ACTION_RESET`
- `#define EXAM_TIMER_STOP      TIMER_ACTION_STOP`

## Public fault globals

- `extern volatile exam_fault_snapshot_t fault_snapshot;`
- `extern volatile uint8_t fault_snapshot_valid;`
