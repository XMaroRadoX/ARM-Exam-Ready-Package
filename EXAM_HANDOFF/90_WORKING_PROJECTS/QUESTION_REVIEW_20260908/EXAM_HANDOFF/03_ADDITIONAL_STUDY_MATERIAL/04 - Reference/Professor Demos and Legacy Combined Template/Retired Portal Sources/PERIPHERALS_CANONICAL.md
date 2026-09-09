# LPC1768 Peripherals from Zero

> **Compatibility notice:** this handbook was generated for the retired
> two-file experiment and is not the API contract for new work. Use
> `../../../02_STARTING_TEMPLATES/Official Combined Exam API Reference/EXAM_API_QUICK_REFERENCE.md`
> and its `Source/exam_api/exam_api.h` instead. The examples below remain only
> as archived study material until they are rewritten for the restored API.

If a paper requires a professor function, a particular interrupt handler, or
direct registers, use that exact interface instead of translating the question
into an API exercise.

## Lesson 1 — Project, `main()`, and waiting

Edit `Answer/main.c` and `Answer/assembly.s`. Call `exam_init()` once before any
peripheral call. Initialize shared state before starting a timer or input source.
Keep `main()` responsible for long work; callbacks only capture an event.

```c
#include "exam_api.h"

int main(void)
{
  exam_init();
  exam_leds_clear();
  for (;;) {
    /* Process foreground state here. */
    exam_idle();
  }
}
```

`exam_idle()` is non-blocking by default. It uses `WFI` only when the template
configuration enables that policy and an interrupt can wake the processor.

## Lesson 2 — LEDs

Logical LED indexes are 0–7; mask bit `n` controls logical LED `n`. Use
`exam_led_from_board_label()` when the paper names physical labels 4–11.

```c
#include "exam_api.h"

int main(void)
{
  uint8_t index;
  exam_init();
  exam_leds_write(0x81u);                 /* Logical LEDs 0 and 7. */
  if (exam_led_from_board_label(8u, &index) == EXAM_OK) {
    exam_led_toggle(index);
  }
  exam_leds_bar(7u, 10u);                 /* Rounded 0..10 display. */
  for (;;) exam_idle();
}
```

Check `EXAM_RANGE` for invalid indexes, labels, and bar ranges. Direct GPIO is
appropriate only when the paper tests pin mapping or register writes.

## Lesson 3 — Raw buttons

Buttons are active-low electrically, but API state is normalized: down means
true. `exam_buttons_start()` supplies debounced press and release callbacks.
`exam_button_irq_start()` exposes one external interrupt for a question that
requires an application-owned handler.

```c
#include "exam_api.h"

static volatile uint32_t button_event;

static void on_button(exam_button_t button, exam_button_event_t event)
{
  if (event == EXAM_PRESS) button_event |= 1u << (uint32_t)button;
}

int main(void)
{
  exam_init();
  exam_buttons_confirmation_ms(50u);
  if (exam_buttons_start(on_button) != EXAM_OK) exam_leds_fill();
  for (;;) {
    uint32_t saved = exam_critical_enter();
    uint32_t pending = button_event;
    button_event = 0u;
    exam_critical_exit(saved);
    if (pending != 0u) exam_leds_write((uint8_t)pending);
    exam_idle();
  }
}
```

Use `exam_buttons_down()` for a held-level snapshot and the pressed/released
edge helpers only with a callback's `current` and `changed` masks.

## Lesson 4 — Interrupt ownership

Every vector has exactly one owner. `exam_config.h` defaults Timer0–Timer2 to
student handlers and Timer3, RIT, SysTick, ADC, and EINT to platform handlers.
An API operation returns `EXAM_BUSY` when the selected resource is student-owned.

For direct timer handlers, read the interrupt register once, clear only the
observed write-one-to-clear bits, and publish a small event:

```c
#include "LPC17xx.h"
#include "exam_api.h"

#define EVENT_TIMER0 (1u << 0)

void TIMER0_IRQHandler(void)
{
  uint32_t pending = LPC_TIM0->IR;
  LPC_TIM0->IR = pending & 0x3Fu;
  if ((pending & 1u) != 0u) exam_events_set(EVENT_TIMER0);
}
```

Never configure the same resource through both the API and direct registers.

## Lesson 5 — Timer0–Timer3

Use Timer3 with callback helpers under the default ownership. Use Timer0–Timer2
for direct-handler exam questions. The callback receives the timer and the
captured interrupt flags.

```c
#include "exam_api.h"

static void every_half_second(exam_timer_t timer, uint32_t flags)
{
  if (timer == EXAM_TIMER_3 && exam_timer_match_happened(flags, 0u)) {
    exam_led_toggle(0u);
  }
}

int main(void)
{
  exam_init();
  if (exam_timer_periodic_ms(EXAM_TIMER_3, 500u,
                             every_half_second) != EXAM_OK) {
    exam_leds_fill();
  }
  for (;;) exam_idle();
}
```

For a stopwatch, call `exam_timer_free_running_start()` and subtract unsigned
timestamps; unsigned subtraction remains correct across one counter wrap. For a
one-shot timeout, configure `exam_timer_match()` with interrupt, reset, and stop
actions, then call `exam_timer_start()`.

## Lesson 6 — Button debouncing

The canonical input service already debounces all three buttons using the RIT
scheduler. The application chooses the confirmation interval and reacts to one
press or release callback. Debounce state machines belong in a recipe only when
the paper explicitly asks you to implement them.

```c
#include "exam_api.h"

static void on_button(exam_button_t button, exam_button_event_t event)
{
  if (event != EXAM_PRESS) return;
  if (button == EXAM_BUTTON_INT0) exam_led_toggle(0u);
  if (button == EXAM_BUTTON_KEY1) exam_led_toggle(1u);
  if (button == EXAM_BUTTON_KEY2) exam_led_toggle(2u);
}

int main(void)
{
  exam_init();
  exam_buttons_confirmation_ms(50u);
  if (exam_buttons_start(on_button) != EXAM_OK) exam_leds_fill();
  for (;;) exam_idle();
}
```

Do not delay inside an EINT handler. In a direct-register answer, disable or
mask the selected source, sample on a periodic tick, confirm stable press and
release, clear the flag correctly, then re-enable it.

## Lesson 7 — SysTick

SysTick is a 24-bit core timer. `exam_systick_periodic_ms()` validates the
requested period and starts the platform-owned tick. Read its monotonic tick
count with `exam_systick_ticks()`.

```c
#include "exam_api.h"

int main(void)
{
  uint32_t previous;
  exam_init();
  if (exam_systick_periodic_ms(10u) != EXAM_OK) exam_leds_fill();
  previous = exam_systick_ticks();
  for (;;) {
    uint32_t now = exam_systick_ticks();
    if ((uint32_t)(now - previous) >= 100u) {
      previous += 100u;
      exam_led_toggle(0u);
    }
  }
}
```

For direct SysTick setup, compute `LOAD = cycles - 1`, check the 24-bit limit,
and remember that the Cortex-M3 automatically clears the exception condition.

## Lesson 8 — RIT

The API-owned RIT is the shared 10 ms scheduler behind button and joystick
services. `exam_rit_start()` starts it, `exam_rit_ticks()` exposes elapsed
scheduler ticks, and `exam_rit_stop()` stops it. It has no user callback.

```c
#include "exam_api.h"

int main(void)
{
  uint32_t previous;
  exam_init();
  if (exam_rit_start() != EXAM_OK) exam_leds_fill();
  previous = exam_rit_ticks();
  for (;;) {
    uint32_t now = exam_rit_ticks();
    if ((uint32_t)(now - previous) >= 50u) {
      previous += 50u;
      exam_led_toggle(0u);
    }
  }
}
```

If `EXAM_RIT_DIRECT_MODE` or `EXAM_OWN_RIT_HANDLER` is enabled, use the direct
RIT registers and handler required by the paper; API scheduler calls must fail
instead of silently changing ownership.

## Lesson 9 — Joystick

Joystick state is a normalized mask. The callback reports `current` held bits
and `changed` bits. Intersect them for new presses or releases.

```c
#include "exam_api.h"

static void on_joystick(uint32_t current, uint32_t changed)
{
  uint32_t pressed = exam_joystick_pressed_edges(current, changed);
  if ((pressed & EXAM_JOY_UP) != 0u) exam_led_on(7u);
  if ((pressed & EXAM_JOY_DOWN) != 0u) exam_led_on(0u);
  if ((pressed & EXAM_JOY_SELECT) != 0u) exam_leds_clear();
}

int main(void)
{
  exam_init();
  exam_joystick_reset_first();
  if (exam_joystick_start(on_joystick) != EXAM_OK) exam_leds_fill();
  for (;;) exam_idle();
}
```

Use `exam_joystick_down()` for a held-level snapshot and
`exam_joystick_first()` when the problem explicitly needs the first movement.

## Lesson 10 — ADC / potentiometer

Start the potentiometer once, then request a fresh 12-bit sample. The read call
returns `EXAM_NOT_READY` until a conversion completes; it does not invent a
cached value. Scale only after a successful result.

```c
#include "exam_api.h"

int main(void)
{
  uint16_t raw;
  exam_init();
  if (exam_potentiometer_start() != EXAM_OK) exam_leds_fill();
  for (;;) {
    if (exam_potentiometer_read_raw(&raw) == EXAM_OK) {
      exam_leds_write((uint8_t)(raw >> 4));
    }
  }
}
```

Use `exam_potentiometer_read_percent()` for 0–100 scaling and
`exam_adc_read_raw(channel, &raw)` for an already configured ADC channel. If the
paper specifies `ADC_IRQHandler`, ADGDR capture, or register fields, implement
those directly and read ADGDR exactly once per completed conversion.

## Lesson 11 — DAC / speaker

`exam_dac_write_raw()` accepts 0–1023. `exam_dac_write_percent()` accepts
0–100. `exam_dac_play()` sends a finite sample table using a timer, and
`exam_dac_stop()` releases that playback. It does not loop automatically.

```c
#include "exam_api.h"

static const uint16_t tone[] = {512u, 900u, 512u, 124u};

int main(void)
{
  exam_init();
  if (exam_dac_play(tone, 4u, 8000u, EXAM_TIMER_3) != EXAM_OK) {
    exam_leds_fill();
  }
  for (;;) exam_idle();
}
```

Output frequency is `sample_hz / sample_count` for one table cycle. Use a
recipe-owned state machine to replay, pause, or sequence tables. Call
`exam_dac_silence()` when zero output is required.

## Lesson 12 — IRQ-to-main events

An interrupt should acknowledge its hardware source, capture the minimum data,
and set an event bit. `exam_events_take(mask)` atomically returns and clears only
the requested bits.

```c
#include "exam_api.h"

#define EVENT_SAMPLE (1u << 0)

static void timer_event(exam_timer_t timer, uint32_t flags)
{
  if (timer == EXAM_TIMER_3 && exam_timer_match_happened(flags, 0u)) {
    exam_events_set(EVENT_SAMPLE);
  }
}

int main(void)
{
  exam_init();
  exam_timer_periodic_ms(EXAM_TIMER_3, 100u, timer_event);
  for (;;) {
    if ((exam_events_take(EVENT_SAMPLE) & EVENT_SAMPLE) != 0u) {
      exam_led_toggle(0u);
    }
    exam_idle();
  }
}
```

Use `volatile` for independently observed shared state. Protect multi-step
updates with `exam_critical_enter()` and restore the returned PRIMASK using
`exam_critical_exit()`.

## Lesson 13 — Combining peripherals

List owners before code: input source, time source, output, callback/handler,
and foreground algorithm. Initialize state, then inputs and outputs, then start
timing last. This example maps the potentiometer to LEDs on a Timer3 event.

```c
#include "exam_api.h"

#define EVENT_SAMPLE (1u << 0)

static void timer_event(exam_timer_t timer, uint32_t flags)
{
  if (timer == EXAM_TIMER_3 && exam_timer_match_happened(flags, 0u)) {
    exam_events_set(EVENT_SAMPLE);
  }
}

int main(void)
{
  uint8_t percent;
  exam_init();
  if (exam_potentiometer_start() != EXAM_OK) exam_leds_fill();
  if (exam_timer_periodic_ms(EXAM_TIMER_3, 50u, timer_event) != EXAM_OK) {
    exam_leds_fill();
  }
  for (;;) {
    if ((exam_events_take(EVENT_SAMPLE) & EVENT_SAMPLE) != 0u &&
        exam_potentiometer_read_percent(&percent) == EXAM_OK) {
      exam_leds_bar(percent, 100u);
    }
    exam_idle();
  }
}
```

Long algorithms, table generation, sorting, filtering, and printing remain in
`main()`. Do not block or start another ownership-changing operation in a callback.

## Lesson 14 — Choose the correct level

Use the Exam API when the paper permits a helper and the selected resource is
API-owned. Use professor functions when the statement supplies their names or
semantics. Use direct registers and a strong handler when the configuration,
acknowledgement, vector, or exact timing is being tested.

| Question wording | Correct level |
|---|---|
| “Using the supplied function…” | Professor function with the exact prototype |
| “Configure MR0/MCR/CCR…” | Direct registers and the required handler |
| “Periodically update…” with helpers permitted | Exam API callback on an API-owned timer |
| “Write an assembly routine…” | `Answer/assembly.s` with AAPCS register and stack rules |
| “Use Timer0_IRQHandler…” | Student-owned Timer0; do not also request the Timer0 API callback |

When C calls assembly, arguments 1–4 use R0–R3, later words start at the caller's
stack, R4–R11 are callee-saved, SP is eight-byte aligned at public call
boundaries, and a 32-bit scalar returns in R0.

## Build and evidence boundary

Compile both Keil targets after changing ownership or handlers. A zero-error,
zero-warning build proves syntax, types, symbols, and linking. It does not prove
physical GPIO, interrupt timing, ADC, DAC, or speaker behavior on a board.
