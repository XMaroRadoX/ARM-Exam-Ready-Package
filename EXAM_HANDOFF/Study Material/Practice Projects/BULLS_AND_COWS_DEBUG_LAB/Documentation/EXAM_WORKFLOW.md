# Exam workflow

## 1. Translate the question before coding

Make a small table on paper:

| Requirement | Where it belongs |
|---|---|
| One-time peripheral setup | `exam_user_init()` |
| Repeated polling or long algorithm | `exam_user_loop()` |
| Short periodic or input reaction | callback or exact handler |
| Required assembly algorithm | `exam_asm.s` |
| Required `Reset_Handler` work | strong handler in `exam_asm.s` |

Record exact timer numbers and periods. If three timers are requested, treat
them as three independent resources; do not merge their periods unless the
question permits software scheduling from one timer.

## 2. Connect C and assembly

In the C answer file:

```c
extern uint32_t MyRoutine(uint32_t input);
```

In the assembly answer file:

```asm
                EXPORT  MyRoutine

MyRoutine       PROC
                ; R0 contains input. Return a 32-bit result in R0.
                BX      LR
                ENDP
```

The first four arguments use `R0-R3`; later arguments are on the caller's
stack. Preserve any changed `R4-R11`. Save `LR` when the routine uses `BL`.

## 3. Choose the least complicated peripheral form that still answers the paper

- Use `exam_*` calls when the peripheral supports the algorithm and its raw
  register setup is not graded.
- Use the familiar course functions when the wording follows a laboratory
  template exactly.
- Use LPC1768 registers and the exact vector name when the register work or
  interrupt handler is part of the answer.

These choices use the same target and may be mixed across different
peripherals. Do not mix a callback helper and exact ownership for the same
interrupt vector.

## 4. Build in small steps

1. Add the C prototype and empty assembly routine; rebuild.
2. Implement and test the assembly result; rebuild.
3. Add one peripheral setup; rebuild.
4. Add one callback or exact handler; rebuild.
5. Add foreground state logic; rebuild.

Fix the first compiler error first. Later errors are often consequences of
the first missing brace, wrong prototype or misspelled label.

## 5. Reset and startup questions

`Source/startup_LPC17xx.s` remains in the internal project group. Its
`Reset_Handler` is weak. A strong handler written in `exam_asm.s` replaces it
without changing the startup file. Perform only reset-safe raw assembly work,
then branch to `__main`; do not return with `BX LR`.

## 6. Debugging order

1. Check that the selected timer/peripheral is powered.
2. Check pin function and direction.
3. Check PCLK and prescaler.
4. Check the match/reload value.
5. Check peripheral interrupt enable and NVIC enable.
6. Check that the handler runs and clears the pending flag.
7. Check shared state and foreground consumption.

When hardware is unavailable, compilation proves syntax and linking only.
Keep board verification listed separately.
