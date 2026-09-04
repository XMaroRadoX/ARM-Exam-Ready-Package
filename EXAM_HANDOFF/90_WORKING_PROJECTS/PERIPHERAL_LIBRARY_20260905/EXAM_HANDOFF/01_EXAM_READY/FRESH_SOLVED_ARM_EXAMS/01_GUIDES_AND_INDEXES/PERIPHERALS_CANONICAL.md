# Peripherals with the Official Combined Exam API

These lessons use only `01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API`.
The declarations in `Source/exam_api/exam_api.h` are authoritative. Copy the
whole project before editing it. The exam paper still wins when it supplies a
different function or explicitly requires direct registers.

## Lesson 1: Project, main(), and waiting

Start with `sample.uvprojx`. Put foreground code in `Source/sample.c` and assembly in
`Source/ASM_funct.s`. Edit an existing IRQ source when the question needs that
vector; never add a second definition of the same handler. When using a complete
maintained solved answer, keep its handlers and static state together in
`sample.c` and remove conflicting template handler definitions as described in
[the integration guide](USING_SOLVED_ANSWERS_WITH_OFFICIAL_TEMPLATE.md).

```c
#include "LPC17xx.h"
#include "exam_api.h"

int main(void)
{
  exam_init();
  /* Initialize only the peripherals named by the paper. */
  for (;;) {
    __WFI();
  }
}
```

`exam_init()` prepares the core support and LEDs. It does not start every timer,
RIT, SysTick, ADC conversion, button debounce, or joystick workflow.

## Lesson 2: LEDs

Single-LED calls use printed board labels **4 through 11**. For example,
`exam_led_on(11u)` lights LD11. Whole-display masks keep their original bit order.

| Board label | GPIO pin | Display bit | Mask |
|---|---|---|---|
| LD4 | P2.7 | 7 | 0x80 |
| LD5 | P2.6 | 6 | 0x40 |
| LD6 | P2.5 | 5 | 0x20 |
| LD7 | P2.4 | 4 | 0x10 |
| LD8 | P2.3 | 3 | 0x08 |
| LD9 | P2.2 | 2 | 0x04 |
| LD10 | P2.1 | 1 | 0x02 |
| LD11 | P2.0 | 0 | 0x01 |

**Numbering change:** older single-LED API calls used indexes 0..7. Convert each
old index to `11 - old_index`; do not change whole-display masks. Values 4..7
are valid under both contracts but select different LEDs. The low-level
professor functions retain their original index convention.

```c
exam_led_on(4u);       /* LED4 */
exam_led_one_hot(8u);  /* only LED8; returns EXAM_OK, not a bit mask */
exam_led_write(0x81u); /* LED4 and LED11 */
```

Check the returned status for single-LED calls; labels outside 4..11 leave the display unchanged. `exam_led_write()` writes the full
logical byte atomically; `exam_led_read()` returns that logical byte and
`exam_led_clear()` turns all eight off.

## Lesson 3: Raw buttons

The three buttons are active-low in hardware but `exam_button_is_pressed()`
returns one when pressed. Initialize once and acknowledge the matching source.

```c
exam_buttons_init();

void EINT0_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_INT0);
  exam_events_set(1u);
}
```

Use `EXAM_BUTTON_KEY1` in `EINT1_IRQHandler` and `EXAM_BUTTON_KEY2` in
`EINT2_IRQHandler`. Acknowledge before doing anything that can take time.

## Lesson 4: Interrupt ownership

There must be exactly one strong definition for each vector. In the supplied
project, customize the existing IRQ file for a new peripheral example. For a
complete maintained answer, follow the integration guide and keep its state and
handlers together. The handler should:

1. Snapshot and acknowledge the pending source.
2. Copy only the data needed by foreground code.
3. Set an event bit if later work is required.
4. Return without sorting, delaying, printing, or generating a waveform table.

Set NVIC priority explicitly only when the question needs an ordering. Smaller
priority numbers are higher priority.

## Lesson 5: Timer0-Timer3

The helpers configure MR0 with `PR = 0` using the selected timer's actual PCLK.
Configuration stops and resets the timer; start it separately.

```c
exam_timer_config_ms(EXAM_TIMER0, 500u, EXAM_TIMER_PERIODIC);
exam_timer_start(EXAM_TIMER0);

void TIMER0_IRQHandler(void)
{
  uint32_t pending = exam_timer_ack(EXAM_TIMER0);
  if ((pending & 1u) != 0u) exam_events_set(1u);
}
```

Use `EXAM_TIMER_ONE_SHOT` for a single timeout. Use direct registers for MR1-MR3,
capture, counter input, MAT output, or a custom prescaler. The modulo mode resets
at MR0 without an IRQ; it is not an unlimited free-running timer.

## Lesson 6: Button debouncing

Choose one periodic source. This example samples every 10 ms and confirms after
50 ms using RIT.

```c
exam_buttons_init();
exam_debounce_config(10u, 50u);
exam_rit_config_ms(10u);
exam_rit_start();

void EINT1_IRQHandler(void)
{
  (void)exam_debounce_begin(EXAM_BUTTON_KEY1);
}

void RIT_IRQHandler(void)
{
  exam_rit_ack();
  exam_debounce_tick();
}
```

Foreground code consumes `EXAM_BUTTON_EVENT_KEY1` from
`exam_button_events_take()`. Do not drive the same debounce from two clocks.

## Lesson 7: SysTick

`exam_systick_config_ms()` and `exam_systick_config_ticks()` configure and start
SysTick immediately. The hardware acknowledges SysTick automatically.

```c
exam_systick_config_ms(10u);

void SysTick_Handler(void)
{
  exam_events_set(1u);
}
```

The tick count must fit the 24-bit LOAD register after subtracting one. Stop it
with `exam_systick_stop()` when the question is complete.

## Lesson 8: RIT

RIT configuration does not start the peripheral.

```c
exam_rit_config_ms(50u);
exam_rit_start();

void RIT_IRQHandler(void)
{
  exam_rit_ack();
  exam_events_set(1u);
}
```

Use `exam_rit_stop()` and `exam_rit_reset()` explicitly. Advanced masked compare
behavior remains direct-register work.

## Lesson 9: Joystick

Joystick bits are normalized to one when pressed. Poll it periodically and
compare two samples.

```c
uint32_t previous = 0u;
exam_joystick_init();
for (;;) {
  uint32_t current = exam_joystick_read();
  uint32_t pressed = exam_joystick_pressed_edges(previous, current);
  previous = current;
  if ((pressed & EXAM_JOY_SELECT) != 0u) exam_led_toggle(11u);
}
```

The five masks are `EXAM_JOY_SELECT`, `DOWN`, `LEFT`, `RIGHT`, and `UP`.

## Lesson 10: ADC / potentiometer

The API reads potentiometer channel 5 one conversion at a time.

```c
uint16_t sample;
exam_adc_init();
exam_adc_start();
if (exam_adc_take(&sample) != 0u) {
  exam_adc_show_high8(sample);
  exam_adc_start();
}
```

When using the ADC interrupt, the existing `ADC_IRQHandler` calls
`exam_adc_irq_capture()`. `exam_adc_take()` returns zero until a fresh completed
sample has been captured.

## Lesson 11: DAC / speaker

The DAC accepts samples from 0 through 1023.

```c
exam_dac_init();
(void)exam_dac_write(512);
```

For a waveform, configure one timer, acknowledge MR0 in its handler, advance a
bounded table index, and call `exam_dac_write()` once. The API deliberately does
not hide the timer inside a playback service.

## Lesson 12: IRQ-to-main events

`exam_events_set()` is suitable for publishing bit events from a handler.
Foreground code atomically consumes selected bits with `exam_events_take()`.

```c
enum { EVENT_SAMPLE = 1u << 0 };

void TIMER0_IRQHandler(void)
{
  if ((exam_timer_ack(EXAM_TIMER0) & 1u) != 0u) {
    exam_events_set(EVENT_SAMPLE);
  }
}
```

Use `volatile` for asynchronously changed objects. Protect a compound snapshot
with `exam_critical_enter()` and `exam_critical_exit()`, then do slow work after
leaving the critical section.

## Lesson 13: Combining peripherals

Write an ownership table before coding. Each row names the resource, its setup,
its one handler, the data it publishes, and the foreground consumer. A typical
ADC-to-DAC question might assign Timer0 to sampling, ADC to conversion, and DAC
to output. Assembly should receive ordinary values or pointers and should not
silently reconfigure C-owned hardware.

Initialize in dependency order: `exam_init()`, input/output peripherals, event
state, timing configuration, then timing start. On shutdown, stop the producer
before clearing its pending event or reusing the resource.

## Lesson 14: Choose the correct level

| What the paper asks | Correct level |
|---|---|
| Supplied API helper is permitted | Use the exact `exam_api.h` declaration |
| Professor supplies a named function | Use that exact prototype and behavior |
| Register fields, MR1-MR3, capture, or vector mechanics are assessed | Use direct registers in the existing owner file |
| Pure computation is requested in assembly | Keep hardware in C and expose one exact AAPCS function |
| SVC or fault handler is requested | Enable or implement only the required handler; avoid duplicate ownership |

Never mix two interfaces for the same timer, interrupt, or peripheral.
