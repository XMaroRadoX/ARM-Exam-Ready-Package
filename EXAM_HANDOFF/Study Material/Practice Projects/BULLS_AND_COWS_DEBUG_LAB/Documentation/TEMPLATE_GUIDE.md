# Ultimate CA Exam Template v2

## One project, one target, one solution

Open `ARM_Exam_Template.uvprojx` and build the single `ARM Exam` target. The target builds C and assembly together.

You normally edit only:

- `Source/exam/exam_user.c` for C setup, foreground work, callbacks, and exact interrupt handlers.
- `Source/exam/exam_asm.s` for ARM assembly subroutines.

The remaining files provide startup, checked helpers, familiar course names, and fault capture. Leave them unchanged during a normal exam.

`Source/startup_LPC17xx.s` is still present under the internal group. It holds
the vector table, weak default handlers and the 4 KB stack. A normal answer
does not edit it.

## First five minutes

1. Underline whether each required function is C or assembly.
2. List inputs, outputs, peripherals, timing units, and signedness.
3. Write the assembly prototype in C and the matching `EXPORT` in assembly.
4. Build the untouched project once.
5. Add one requirement at a time and rebuild after each small step.

## Three ways to write code in the same target

Use `exam_*` functions when the peripheral is only a tool in the problem. Use familiar course names from `exam_compat.h` when you want the same calls used in class. Use LPC1768 registers directly when the register setup itself is graded.

There is no target change between these choices. They may be mixed in one answer.

## Exact interrupt ownership

A linked program may contain only one function with a vector name. The template owns common vectors by default and calls your callback.

If the statement explicitly requires `TIMER0_IRQHandler`, for example:

1. Set `EXAM_OWN_TIMER0_HANDLER` to 1 in `exam_config.h`.
2. Write `TIMER0_IRQHandler` in `exam_user.c`.
3. Read the pending flags once.
4. Write the pending bits back to clear W1C flags.
5. Perform only the short required action and return.

Every vector has its own switch, so a direct Timer 0 handler does not disturb buttons or other timers.

Callback helpers for the owned vector return `EXAM_BUSY` instead of silently
waiting for an internal handler that is no longer linked. This conflict is
local: owning Timer 0 does not stop callback helpers on Timers 1 through 3.

## Callback rule

A callback runs inside an interrupt. Read or save the required value, set an event bit, and return. Sorting, formatting, long loops, and waits belong in `exam_user_loop()` unless the statement explicitly requires them inside the handler.

## SVC work in the same target

The default C handler decodes the immediate at stacked PC minus 2 and calls `svc_dispatch`. Override `svc_dispatch` for normal C service handling. If the question requires an exact assembly `SVC_Handler`, set `EXAM_OWN_SVC_HANDLER` to 1 and add that handler to `exam_asm.s`.

## Physical-board checklist

- Confirm the debugger and board power are connected.
- Fit JP12 before reading the potentiometer.
- Fit JP2 before checking speaker or analog output.
- Remember that INT0, KEY1, KEY2, and joystick inputs are active-low.
- Automatic tests do not prove jumper placement or analog signal quality; verify those on the board.

## Common failures

- Duplicate handler: the matching ownership switch is still 0.
- Timer runs at the wrong rate: PCLK divider or PR+1 was omitted.
- Interrupt repeats forever: a pending W1C flag was not written back.
- Main misses a value: interrupt-shared data was not `volatile` or protected.
- Assembly returns incorrectly: LR was not saved before a nested `BL`.
- Fifth argument is wrong: it was loaded after changing SP without saving the original SP.
