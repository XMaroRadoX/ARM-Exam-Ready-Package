# Exam API reference

This is the public beginner layer from `exam_api.h`. The function names state
their unit whenever time or frequency is involved. Calls returning
`exam_status_t` should produce `EXAM_OK` in the normal configuration.

## Status results

| Result | Meaning | Action |
|---|---|---|
| `EXAM_OK` | The request was accepted. | Continue. |
| `EXAM_INVALID` | Null pointer or invalid argument combination. | Check the call. |
| `EXAM_BUSY` | The resource is already claimed or its exact handler is owned. | Use another resource or the raw-handler recipe. |
| `EXAM_RANGE` | Timer, channel, value, period or rate is out of range. | Correct the number. |
| `EXAM_NOT_READY` | No fresh input result is available yet. | Try again in the foreground loop. |

Ignoring a returned status is legal C, but checking setup calls gives a useful
breakpoint when an answer owns the same interrupt vector.

## Program control

| Signature | Effect and conditions |
|---|---|
| `void exam_init(void)` | Internal main calls this once. It initializes the clock, LEDs and fault support only. Do not call it again. |
| `void exam_idle(void)` | Default is one `NOP`, so polling continues. It uses `WFI` only when `CA_IDLE_USE_WFI` is 1. |
| `uint32_t exam_self_test(void)` | Runs non-hardware configuration checks. Zero means no detected automatic failure; it does not prove board wiring. |

## LEDs

| Signature | Effect and conditions |
|---|---|
| `exam_status_t exam_led_on(uint8_t printed_number)` | Turns on printed LED 4..11. |
| `exam_status_t exam_led_off(uint8_t printed_number)` | Turns off printed LED 4..11. |
| `exam_status_t exam_led_toggle(uint8_t printed_number)` | Toggles printed LED 4..11. |
| `exam_status_t exam_led_write(uint8_t mask)` | Writes all eight LED bits; bit 0 controls P2.0/printed LED4. |
| `uint8_t exam_led_read(void)` | Returns the last eight-bit LED value. |
| `void exam_leds_off(void)` | Turns all eight LEDs off. |

Example: `exam_led_write(0xA5);`

## External buttons

| Signature | Effect and ownership |
|---|---|
| `exam_status_t exam_buttons_start(exam_button_callback_t callback)` | Starts confirmed INT0/KEY1/KEY2 events and claims the normal 10 ms RIT service. Returns `EXAM_BUSY` in exact/direct RIT mode. |
| `exam_status_t exam_button_irq_start(exam_button_t button)` | Configures and enables one exact EINT vector. It does not start debounce, a callback or RIT. |
| `void exam_buttons_confirmation_ms(uint32_t milliseconds)` | Changes the confirmation period. Use a multiple of the 10 ms scheduler tick. |
| `uint8_t exam_button_pressed(exam_button_t button)` | Polls one active-low button and returns 1 while held. No interrupt is required. |
| `uint32_t exam_buttons_pressed(void)` | Returns a mask for all three active-low external buttons. |

Buttons are `EXAM_BUTTON_INT0`, `EXAM_BUTTON_KEY1` and
`EXAM_BUTTON_KEY2`. Callback events are `EXAM_PRESS` and `EXAM_RELEASE`.

## Joystick

| Signature | Effect and ownership |
|---|---|
| `exam_status_t exam_joystick_start(exam_joystick_callback_t callback)` | Starts change callbacks and claims the normal 10 ms RIT service. Returns `EXAM_BUSY` in exact/direct RIT mode. |
| `uint32_t exam_joystick_read(void)` | Returns the current direction mask. Test it with `&`. |
| `uint32_t exam_joystick_first(void)` | Returns the first nonzero movement remembered since reset. |
| `void exam_joystick_reset_first(void)` | Clears first-movement memory for a new round. |

Direction masks are `EXAM_JOY_UP`, `EXAM_JOY_DOWN`, `EXAM_JOY_LEFT`,
`EXAM_JOY_RIGHT` and `EXAM_JOY_SELECT`.

## Timers 0 through 3

| Signature | Effect and ownership |
|---|---|
| `exam_status_t exam_timer_every_ms(int timer, int milliseconds, exam_timer_callback_t callback)` | Configures MR0 as a periodic interrupt and starts the timer. It needs the template handler for that timer. |
| `exam_status_t exam_timer_every_hz(int timer, int hertz, exam_timer_callback_t callback)` | Same, with one callback per requested cycle. |
| `exam_status_t exam_timer_clock_divider(uint8_t timer, uint8_t divider)` | Selects PCLK divider 1, 2, 4 or 8 while the timer is stopped. |
| `exam_status_t exam_timer_prescaler(uint8_t timer, uint32_t prescaler)` | Sets PR; the timer-counter divisor is `PR+1`. |
| `exam_status_t exam_timer_match(uint8_t timer, uint8_t match, uint32_t ticks, uint32_t actions)` | Programs MR0..MR3 and its MCR interrupt/reset/stop actions. |
| `exam_status_t exam_timer_start(uint8_t timer)` | Starts counting. |
| `exam_status_t exam_timer_stop(uint8_t timer)` | Stops counting without erasing TC. |
| `exam_status_t exam_timer_reset(uint8_t timer)` | Pulses reset and leaves the timer stopped. |
| `uint32_t exam_timer_count(uint8_t timer)` | Reads TC; useful for a free-running timer. |
| `uint8_t exam_timer_match_happened(uint32_t flags, uint8_t match)` | Tests callback flags for MR0..MR3. |
| `uint8_t exam_timer_capture_happened(uint32_t flags, uint8_t capture)` | Tests callback flags for CR0 or CR1. |

Actions may be ORed from `EXAM_TIMER_INTERRUPT`, `EXAM_TIMER_RESET` and
`EXAM_TIMER_STOP`. Owning `TIMER0_IRQHandler`, for example, disables callback
helpers only for Timer 0; Timers 1..3 remain independent.

## RIT and SysTick

| Signature | Effect and ownership |
|---|---|
| `exam_status_t exam_rit_start(void)` | Starts the normal 10 ms RIT scheduler. Returns `EXAM_BUSY` when the exact RIT handler or direct RIT mode is selected. |
| `void exam_rit_stop(void)` | Stops the scheduler counter. |
| `uint32_t exam_rit_ticks(void)` | Returns elapsed 10 ms scheduler ticks. |
| `exam_status_t exam_systick_every_ms(int milliseconds)` | Configures periodic SysTick interrupts. |
| `uint32_t exam_systick_ticks(void)` | Returns ticks counted by the built-in SysTick handler. Do not use it while owning the exact SysTick vector. |

## ADC and potentiometer

| Signature | Effect and ownership |
|---|---|
| `exam_status_t exam_pot_start(void)` | Lazily initializes ADC channel 5 and requests the first conversion. Fit JP12. |
| `exam_status_t exam_pot_read(int *value)` | Returns a fresh 0..4095 value and requests the next conversion; otherwise returns `EXAM_NOT_READY`. |
| `exam_status_t exam_adc_read(uint8_t channel, uint16_t *value)` | Reads the cached result for channel 0..7. |

These functions depend on the built-in `ADC_IRQHandler`. When the answer owns
the exact ADC vector they return `EXAM_BUSY`; read `LPC_ADC->ADGDR` once in the
handler and decode bits 15:4 yourself.

## DAC / analog output

| Signature | Effect and conditions |
|---|---|
| `exam_status_t exam_dac_write(int value)` | Lazily initializes AOUT and writes 0..1023. Fit JP2. |
| `exam_status_t exam_dac_percent(int percent)` | Writes an easier 0..100 percent value. |
| `void exam_dac_silence(void)` | Writes zero to the DAC. |

## Interrupt-to-foreground communication

| Signature | Effect and conditions |
|---|---|
| `void exam_events_set(uint32_t bits)` | Atomically sets event bits; safe from an interrupt callback. |
| `uint32_t exam_events_take(uint32_t mask)` | Atomically returns and clears selected bits in the foreground loop. |
| `uint32_t exam_critical_enter(void)` | Saves PRIMASK and disables interrupts for a short critical section. |
| `void exam_critical_exit(uint32_t saved_primask)` | Restores the exact saved PRIMASK value. |

Give every event a different bit. Keep critical sections short and never wait
inside them.

## Familiar course functions

`exam_compat.h` also provides `LED_init`, `LED_On`, `LED_Off`, `LED_Out`,
`BUTTON_init`, `init_timer`, `enable_timer`, `disable_timer`, `reset_timer`,
`init_RIT`, `enable_RIT`, `disable_RIT`, `reset_RIT`, `ADC_init`, and
`ADC_start_conversion`.

`LED_On(0)` uses GPIO bit numbering, while `exam_led_on(4)` uses the printed
board number. Pick one numbering system and keep it consistent.

Copyable complete patterns are in `PERIPHERAL_RECIPES.md`. Configuration and
resource-conflict behavior is checked by the strict compiler configurations;
physical electrical behavior still requires the LandTiger board.
