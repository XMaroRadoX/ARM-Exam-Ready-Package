# How to use the project in the exam

## Before the paper arrives

Copy the entire `ARM_Exam_Project` directory into the location required by the
exam system. Keep the original USB copy untouched so it remains a recovery
copy. Open `ARM_Exam_Template.uvprojx`, select the single target `ARM Exam`, and
build once before changing code.

The directory to submit is the copied `ARM_Exam_Project` directory—not `Study
Material`, `ARM`, `Architectures` or `Exams`.

## The three files that matter first

1. `Answer/exam_asm.s` — write or paste the Q1 assembly routine.
2. `Answer/exam_user.c` — write the Q2 application and call Q1.
3. `Answer/exam_user.h` — put shared prototypes, event bits and small types here.

`Source/platform/exam_config.h` is the fourth file only when you need to own an
interrupt handler, change debounce policy or change an optional platform mode.

Do not create another C `main`. The existing one initializes the platform and
calls `exam_user_init()` once, then `exam_user_loop()` forever.

## What is ready before your answer runs

The startup path is `Reset_Handler` → C runtime → `main()` → `exam_init()` →
`exam_user_init()`. By the time `exam_user_init()` starts, the template has
already established the following state:

| Resource | State on entry to `exam_user_init()` | Additional answer setup |
|---|---|---|
| C runtime | stack and initialized C data are ready | none |
| core/system clock | configured; `SystemFrequency` is current | none unless the paper explicitly changes the clock |
| LEDs 4–11 | GPIO function selected, outputs enabled, all off | call the desired `exam_led_*` function |
| fault support | configured from `exam_config.h` | none for ordinary questions |
| timers 0–3 | not running and not claimed | start/configure only the timer named by the paper |
| RIT | not running | `exam_buttons_start`, `exam_joystick_start`, or `exam_rit_start` starts scheduler mode |
| external buttons | not configured | `exam_buttons_start(callback)` for confirmed events, or `exam_button_irq_start` for a direct IRQ exercise |
| joystick | not configured | `exam_joystick_start(callback)` for serviced input; direct polling also has low-level helpers |
| SysTick | not running | `exam_systick_every_ms(period)` when the paper calls for SysTick |
| ADC/potentiometer | powered down and no conversion pending | `exam_pot_start()` initializes channel 5 and starts the first conversion |
| DAC/speaker | not configured | `exam_dac_write(value)` initializes the DAC automatically on its first call |
| Ethernet, CAN, MIDI and LCD | not included in the submission project | historical papers did not justify carrying these into the exam template |

This opt-in state is deliberate. Starting every peripheral automatically would
consume timers and interrupt vectors before the question assigns them.

### Minimal initialization shapes

Only the calls relevant to the paper belong in `exam_user_init()`:

```c
/* No board peripheral in the question. */
void exam_user_init(void)
{
}
```

```c
/* LEDs only: the LEDs already have their GPIO setup. */
void exam_user_init(void)
{
  (void)exam_led_write(0u);
}
```

```c
/* One periodic timer. The helper configures MR0, registers the callback,
 * clears stale state and starts the selected timer. */
static void timer_event(uint8_t timer, uint32_t flags)
{
  if (timer == 0u && exam_timer_match_happened(flags, 0u)) {
    exam_events_set(1u);
  }
}

void exam_user_init(void)
{
  (void)exam_timer_every_ms(0, 1000, timer_event);
}
```

```c
/* Debounced external buttons. The call also starts the 10 ms RIT service. */
static void button_event(exam_button_t button, exam_button_event_t event)
{
  if (button == EXAM_BUTTON_INT0 && event == EXAM_PRESS) {
    exam_events_set(1u);
  }
}

void exam_user_init(void)
{
  (void)exam_buttons_start(button_event);
}
```

```c
/* Potentiometer. The first conversion begins during initialization. */
void exam_user_init(void)
{
  (void)exam_pot_start();
}
```

Return values are useful debugger evidence. `EXAM_OK` means the peripheral was
accepted; `EXAM_BUSY` usually means an interrupt vector or timer already has a
different owner; `EXAM_RANGE` indicates an invalid timer, period, rate, channel
or sample value.

## Translate Q1 into a contract

Before writing instructions, note:

- exact C-style prototype and return type;
- byte, halfword or word elements;
- signed or unsigned comparisons;
- R0–R3 arguments and any fifth argument at the caller's stack;
- output memory and bounds;
- whether flags are part of the return contract;
- whether the routine calls another routine and therefore must preserve LR;
- callee-saved registers R4–R11;
- eight-byte stack alignment at every public call boundary.

Change the export and label in `exam_asm.s` to the required name. Put an exact
prototype in `exam_user.h` or near the top of `exam_user.c`:

```c
extern uint32_t requiredRoutine(const uint32_t *input, uint32_t length);
```

For a leaf routine, `BX LR` returns. For a non-leaf routine, save LR before the
first `BL`. Push an even number of registers, or compensate explicitly, so SP
remains eight-byte aligned when another public routine is called.

## Decide whether Q1 is a routine or startup code

Most papers require a callable assembly routine. In that case, leave
`Source/startup_LPC17xx.s` alone.

If the paper explicitly requires a loop in `Reset_Handler`, export a strong
`Reset_Handler` from the answer assembly. The platform startup handler is weak.
If C must run afterwards, branch to `__main` after the required startup work.
Preserve stack alignment while placing a fifth argument on the stack.

## Translate Q2 into initialization, events and state

Place one-time setup in `exam_user_init()`:

- configure clocks/prescalers/matches;
- start ADC, buttons or joystick;
- clear arrays and state;
- register callbacks;
- start only the timers the paper says should already run.

Place foreground state-machine work in `exam_user_loop()`. Interrupt callbacks
should normally record minimal state and set an event bit. Direct handler bodies
are appropriate only when the paper explicitly grades register-level interrupt
work or the timing is genuinely bounded.

## Choose one owner for each interrupt

Callback API path:

```c
static void timer_event(uint8_t timer, uint32_t flags)
{
  if (timer == 1u && exam_timer_match_happened(flags, 0u)) {
    /* bounded event work */
  }
}

void exam_user_init(void)
{
  (void)exam_timer_every_ms(1, 500, timer_event);
}
```

Direct-vector path:

```c
/* In exam_config.h */
#define EXAM_OWN_TIMER1_HANDLER 1

/* In exam_user.c */
void TIMER1_IRQHandler(void)
{
  uint32_t pending = LPC_TIM1->IR & 0x3Fu;
  LPC_TIM1->IR = pending;
  if (pending & 1u) {
    /* bounded work */
  }
}
```

Never keep both owners. A duplicate-handler link error is a configuration error,
not an assembly-algorithm error.

## Common API choices

| Paper wording | Starting API |
|---|---|
| show an 8-bit value on LEDs | `exam_led_write(value)` |
| LED number 4–11 | `exam_led_on`, `exam_led_off`, `exam_led_toggle` |
| debounced INT0/KEY1/KEY2 | `exam_buttons_start(callback)` |
| raw external interrupt | `exam_button_irq_start(button)` plus vector ownership if writing the handler |
| joystick direction/first move | `exam_joystick_start`, `exam_joystick_read`, `exam_joystick_first` |
| periodic timer | `exam_timer_every_ms` or `exam_timer_every_hz` |
| free-running timer | prescaler, reset, start, then `exam_timer_count` |
| exact match actions | `exam_timer_match` with interrupt/reset/stop bits |
| ADC potentiometer | `exam_pot_start`, then `exam_pot_read` |
| DAC value | `exam_dac_write`; input range is 0–1023 |
| transfer IRQ work to foreground | `exam_events_set` and `exam_events_take` |
| direct peripheral requirement | typed low-level API or `LPC_*` definitions from `LPC17xx.h` |

## Build and inspect before debugging behavior

Build after each small milestone. Resolve errors in this order:

1. duplicate symbol — two vector owners or two `Reset_Handler` definitions;
2. undefined symbol — export/prototype spelling mismatch or missing source file;
3. assembly syntax — wrong instruction form or immediate range;
4. link/RAM overflow — object size or section placement;
5. warnings — signedness, implicit declarations and narrowing conversions;
6. only then inspect state-machine or peripheral behavior.

In the debugger, stop at C `main`, then at `exam_user_init`, then at the assembly
routine. Watch R0–R3, SP, LR and the output array. Step over a `BL` only after
checking that LR and callee-saved registers will be restored.

## Simulator versus board

The same target can be selected for Keil's Cortex-M3 simulator or a hardware
debug adapter. Algorithm routines are appropriate for simulator stepping.
Generic Cortex-M3 simulation does not prove LandTiger buttons, ADC, DAC, timer
pin behavior or electrical debounce. For board execution, verify jumpers and
the required pins, then test the shortest observable sequence first.

## Final five-minute check

- The copied project is inside the exact exam submission directory.
- The build reports zero errors; inspect warnings rather than ignoring them.
- There is one C `main` and one owner for every interrupt vector.
- Every assembly export exactly matches its C prototype.
- Stack alignment and R4–R11 preservation are deliberate.
- Arrays are large enough and loops stop before the first invalid element.
- Timer flags are cleared with write-one-to-clear semantics.
- Active-low buttons are interpreted correctly.
- ADC values use the requested eight or twelve bits.
- DAC values stay within 0–1023.
- The final visible state matches the paper after the last event.
- Save the project in the required exam location and reopen the saved copy once.

Before trusting an old answer, consult the
[exam-by-exam audit](../Tests%20and%20Reports/Repository%20Audit/EXAM_READINESS_AUDIT.md).
