# Peripheral recipes: put the functions in this order

The drivers are already part of the project. Do not copy driver files and do not write `main()` again. For a normal solution, edit only `exam_user.c` and `exam_asm.s`.

The internal main already does this:

```c
exam_init();
exam_user_init();

for (;;) {
    exam_user_loop();
    exam_idle();
}
```

`exam_init()` configures only the system clock, LEDs and fault support. Buttons,
RIT, joystick, timers, ADC and DAC remain untouched until your answer calls
their setup function.

The foreground loop does not sleep by default, so polling continues even when
no interrupt is enabled. Use `CA_IDLE_USE_WFI 1` only when the question
explicitly needs sleep and an enabled interrupt can wake the processor.

## The order inside `exam_user.c`

1. Assembly prototypes and callback prototypes.
2. Global or static variables shared with callbacks.
3. Peripheral setup calls in `exam_user_init()`.
4. Longer repeated work in `exam_user_loop()`.
5. Short callback bodies below the loop.

Use `volatile` when a callback writes a value that the loop reads. Initialize each peripheral once. Add only the peripherals named by the question.

## LEDs only

No setup call is required. Use printed LED numbers 4 through 11:

```c
exam_led_on(4);
exam_led_off(4);
exam_led_toggle(4);
exam_led_write(0xA5);       /* show an eight-bit result */
exam_leds_off();
```

## Poll one external button

Use this when the question does not request interrupts or confirmation:

```c
void exam_user_loop(void)
{
    if (exam_button_pressed(EXAM_BUTTON_INT0)) {
        exam_led_on(4);
    } else {
        exam_led_off(4);
    }
}
```

INT0, KEY1 and KEY2 are active-low. The helper returns 1 while the button is held.

## Confirmed button press using interrupts

First, place the setup call in `exam_user_init()`:

```c
void exam_user_init(void)
{
    exam_buttons_start(exam_button_event);
}
```

Then put the required action in the callback that already exists in `exam_user.c`:

```c
void exam_button_event(exam_button_t button, exam_button_event_t event)
{
    if ((button == EXAM_BUTTON_INT0) && (event == EXAM_PRESS)) {
        exam_led_toggle(4);
    }
}
```

Confirmation is already 50 ms. Do not add a delay loop.
`exam_buttons_start()` starts the required 10 ms RIT service automatically.
It returns `EXAM_BUSY` if the answer owns `RIT_IRQHandler` or selects direct
RIT mode. In that case use the exact button-handler recipe instead.

## Joystick

Setup:

```c
void exam_user_init(void)
{
    exam_joystick_start(exam_joystick_event);
    exam_joystick_reset_first();
}
```

Polling all current directions:

```c
uint32_t directions = exam_joystick_read();

if (directions & EXAM_JOY_UP)     { /* up */ }
if (directions & EXAM_JOY_DOWN)   { /* down */ }
if (directions & EXAM_JOY_LEFT)   { /* left */ }
if (directions & EXAM_JOY_RIGHT)  { /* right */ }
if (directions & EXAM_JOY_SELECT) { /* centre */ }
```

For “only the first movement counts”:

```c
exam_joystick_reset_first();       /* when a new round begins */
uint32_t first = exam_joystick_first();
```

Joystick callbacks also use the normal 10 ms RIT service. Do not combine this
helper with an exact or direct RIT answer.

## Periodic timer in milliseconds

Setup:

```c
void exam_user_init(void)
{
    exam_timer_every_ms(0, 1000, exam_timer_event);
}
```

Short action in the existing callback:

```c
void exam_timer_event(uint8_t timer, uint32_t flags)
{
    if ((timer == 0) && exam_timer_match_happened(flags, 0)) {
        exam_led_toggle(4);
    }
}
```

The library clears the timer W1C flags before calling the callback.

## Timer asks the loop to run a longer function

At the top of the file:

```c
extern uint32_t MyAssembly(uint32_t value);
static volatile uint32_t input_value;
```

Setup:

```c
void exam_user_init(void)
{
    exam_timer_every_ms(0, 500, exam_timer_event);
}
```

## Multiple independent timers

The four hardware timers are independent. Start each one once and use the
`timer` argument to identify which timer interrupted. One callback can handle
all of them:

```c
static volatile uint32_t timer0_events;
static volatile uint32_t timer1_events;
static volatile uint32_t timer2_events;

void exam_user_init(void)
{
    exam_timer_every_ms(0, 100,  exam_timer_event);
    exam_timer_every_ms(1, 250,  exam_timer_event);
    exam_timer_every_ms(2, 1000, exam_timer_event);
}

void exam_timer_event(uint8_t timer, uint32_t flags)
{
    if (!exam_timer_match_happened(flags, 0)) return;

    if (timer == 0) ++timer0_events;
    if (timer == 1) ++timer1_events;
    if (timer == 2) ++timer2_events;
}
```

Timer 3 remains free. Different callbacks may also be used, but the shared
callback is usually shorter and prevents copied code. If the exam requires an
exact handler for one timer, take ownership of only that timer; callback
helpers for the other three continue to work.

Callback:

```c
void exam_timer_event(uint8_t timer, uint32_t flags)
{
    if ((timer == 0) && exam_timer_match_happened(flags, 0)) {
        exam_events_set(EXAM_EVENT_TIMER);
    }
}
```

Foreground work:

```c
void exam_user_loop(void)
{
    if (exam_events_take(EXAM_EVENT_TIMER)) {
        uint32_t answer = MyAssembly(input_value);
        exam_led_write((uint8_t)answer);
    }
}
```

## Free-running timer

Setup:

```c
void exam_user_init(void)
{
    exam_timer_clock_divider(1, 4);  /* 100 MHz / 4 = 25 MHz */
    exam_timer_prescaler(1, 0);      /* divide by PR+1 = 1 */
    exam_timer_reset(1);
    exam_timer_start(1);
}
```

Read it later:

```c
uint32_t elapsed_ticks = exam_timer_count(1);
```

Do not configure an interrupting match when the question asks for a free-running counter.

## Exact timer match value

Use this when the paper gives timer ticks or grades MR/MCR meaning:

```c
void exam_user_init(void)
{
    exam_timer_clock_divider(0, 4);
    exam_timer_prescaler(0, 0);
    exam_timer_match(
        0, 0, 25000000,
        EXAM_TIMER_INTERRUPT | EXAM_TIMER_RESET
    );
    timer_set_callback(0, exam_timer_event);
    exam_timer_start(0);
}
```

The last call uses the precise library function because callback ownership is part of the configuration.

## SysTick

Setup:

```c
static uint32_t previous_tick;

void exam_user_init(void)
{
    exam_systick_every_ms(10);
    previous_tick = exam_systick_ticks();
}
```

Foreground check:

```c
void exam_user_loop(void)
{
    uint32_t now = exam_systick_ticks();

    if (now != previous_tick) {
        previous_tick = now;
        /* one new system-timer event */
    }
}
```

## Ten-millisecond RIT hook

Start the 10 ms scheduler once, then put only a tiny bounded action in the
existing hook:

```c
void exam_user_init(void)
{
    exam_rit_start();
}
```

```c
void exam_user_10ms_hook(void)
{
    /* short 10 ms action */
}
```

Use event bits when the action is long.

## Potentiometer to LEDs

Fit JP12. Start the first conversion once:

```c
void exam_user_init(void)
{
    exam_pot_start();
}
```

Read fresh cached results in the loop:

```c
void exam_user_loop(void)
{
    int value;

    if (exam_pot_read(&value) == EXAM_OK) {
        exam_led_write((uint8_t)(value >> 4));
    }
}
```

The result is 0 through 4095. A successful read automatically requests the next conversion.

These cached helpers require the built-in `ADC_IRQHandler`. If the question
requires your own exact ADC handler, do not call them. Read `LPC_ADC->ADGDR`
once in your handler, extract bits 15:4, and store the result in a `volatile`
variable shared with the foreground loop.

## One analog output value

Fit JP2. Values are 0 through 1023:

```c
exam_dac_write(512);
exam_dac_percent(50);
exam_dac_silence();
```

## Timer-driven waveform

At the top of the file:

```c
static const uint16_t samples[] = { 512, 900, 512, 124 };
static volatile uint32_t sample_index;

static void wave_timer(uint8_t timer, uint32_t flags);
```

Setup for 440 waves per second with four samples per wave:

```c
void exam_user_init(void)
{
    sample_index = 0;
    exam_timer_every_hz(0, 440 * 4, wave_timer);
}
```

Short sample update:

```c
static void wave_timer(uint8_t timer, uint32_t flags)
{
    if ((timer == 0) && exam_timer_match_happened(flags, 0)) {
        exam_dac_write(samples[sample_index]);
        sample_index = (sample_index + 1) % 4;
    }
}
```

Do not put a delay inside the callback.

## Direct power-control question

The project already includes `LPC17xx.h`, so direct registers are available in the same answer file:

```c
LPC_SC->PCONP |= 1u << 1;       /* power Timer 0 */
LPC_SC->PCONP &= ~(1u << 1);    /* remove Timer 0 power */
```

Only change the bit named by the question. Preserve unrelated power bits.

## Exact interrupt handler question

If the paper requires the literal function name `TIMER0_IRQHandler`:

1. Set `EXAM_OWN_TIMER0_HANDLER` to 1 in `exam_config.h`.
2. Add the handler to `exam_user.c`.
3. Read pending flags once and write them back to clear them.

```c
void TIMER0_IRQHandler(void)
{
    uint32_t pending = LPC_TIM0->IR;
    LPC_TIM0->IR = pending;

    if (pending & 1u) {
        /* short MR0 action */
    }
}
```

Do not add a second function with the same vector name.

For an exact external-button handler, enable only the requested vector during
setup. This does not start debounce or the RIT scheduler:

```c
void exam_user_init(void)
{
    exam_button_irq_start(EXAM_BUTTON_INT0);
}

void EINT0_IRQHandler(void)
{
    LPC_SC->EXTINT = 1u;
    /* short required action */
}
```

## Reset_Handler question

Past papers have required initialization directly inside `Reset_Handler`.
The startup file already declares its handler as weak, so define the strong
replacement in `exam_asm.s`; do not edit the startup file.

```asm
                EXPORT  Reset_Handler
                IMPORT  __main

Reset_Handler   PROC
                ; Required one-time setup or test loop goes here.

                LDR     R0, =__main
                BX      R0
                ENDP
```

`Reset_Handler` is entered by hardware reset. It does not return with
`BX LR`. In this combined C and assembly project it completes the required
startup work and branches to `__main`. A pure assembly-only test may end in
an infinite stop loop instead.

Do not call `exam_*` C functions or read initialized C globals before
branching to `__main`; the C runtime has not initialized them yet. Use raw
registers, assembly constants and assembly data during the reset-only section.
If reset-created data must survive C runtime initialization, place it in a
`NOINIT, READWRITE` assembly area.

## Familiar course names

The same project also provides `LED_init`, `LED_On`, `LED_Off`, `LED_Out`, `BUTTON_init`, `init_timer`, `enable_timer`, `disable_timer`, `reset_timer`, `init_RIT`, `enable_RIT`, `disable_RIT`, `reset_RIT`, `ADC_init`, and `ADC_start_conversion`.

Important: `LED_On(0)` means GPIO LED bit 0, while `exam_led_on(4)` means the printed board label LED4. Pick one numbering system for the answer.

## Final order check

1. Declare the assembly function, custom callback or required Reset_Handler.
2. Declare shared variables as `static volatile` where required.
3. Initialize each required peripheral once in `exam_user_init()`.
4. Put longer work and polling in `exam_user_loop()`.
5. Keep every callback short and clear exact-handler flags once.
6. Rebuild and require zero errors and zero warnings.
