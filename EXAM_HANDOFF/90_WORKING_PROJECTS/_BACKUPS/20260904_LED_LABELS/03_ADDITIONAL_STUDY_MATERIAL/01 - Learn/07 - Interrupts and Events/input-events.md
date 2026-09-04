# Inputs, handlers and foreground events

The Official Combined Exam API does not register application callbacks. Use the
exact interrupt handler required by the startup file or exam. A handler should
acknowledge the source, publish the minimum information, and return quickly.

```c
#include "LPC17xx.h"
#include "exam_api.h"

enum { EVENT_BUTTON = 1u << 0 };

void EINT0_IRQHandler(void)
{
  exam_button_ack(EXAM_BUTTON_INT0);
  exam_events_set(EVENT_BUTTON);
}

int main(void)
{
  exam_init();
  exam_buttons_init();

  for (;;) {
    if ((exam_events_take(EVENT_BUTTON) & EVENT_BUTTON) != 0u) {
      (void)exam_led_toggle(0u);
    }
    __WFI();
  }
}
```

For a debounced press, call `exam_debounce_begin()` from the matching EINT
handler and `exam_debounce_tick()` from one periodic time source. Consume the
confirmed `EXAM_BUTTON_EVENT_*` bits with `exam_button_events_take()`.

Joystick input is polled with `exam_joystick_read()`; calculate new presses with
`exam_joystick_pressed_edges(previous, current)`. Use
`exam_critical_enter()` and `exam_critical_exit()` only around a compound shared
snapshot. `volatile` provides visibility but does not make read-modify-write
atomic.
