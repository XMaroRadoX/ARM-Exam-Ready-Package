# Question 3: complete commented rhythm game

## Put each complete file in the working template

| Download | Destination |
|---|---|
| main.c | Source/sample.c |
| assembly.s | Source/ASM_funct.s |
| IRQ_timer.c | Source/timer/IRQ_timer.c |
| IRQ_RIT.c | Source/RIT/IRQ_RIT.c |

The complete C answer includes both used handlers alongside the game logic. The supplied IRQ files remove those duplicate definitions while preserving the unused Timer1-3 handlers. This is the same solution as the split-file lesson, collected into one readable C answer. Do not append it to the existing handlers.

Keep the original startup file. The supplied assembly has no custom Reset_Handler: normal startup initializes C state and enters main. Q1's immediate array-generation loop is a separate test, not part of this timed game.

## Why use RIT?

Timer0 controls WHEN a new LED appears: once every 3000 ms. The joystick must be checked DURING that interval. Checking only inside Timer0 would miss a player who pressed and released between its interrupts.

RIT means Repetitive Interrupt Timer. It checks for a new joystick press every 10 ms, approximately 300 checks per round. This is an implementation choice, not an extra requirement in the paper. It allows main to wait for interrupts instead of spinning.

| Time | Action |
|---|---|
| 3.000 s | Timer0 shows LED9; RIGHT is expected. |
| 3.010 s onward | RIT checks for a new direction every 10 ms. |
| Example: 3.450 s | RIT detects the first response, updates one counter, and clears the LED. |
| Until 6.000 s | Further responses are ignored. |
| 6.000 s | Timer0 starts the next round. |

"Immediately" means on the next sample, normally within about 10 ms; this is polling, not a zero-latency hardware input interrupt. Edge detection handles held inputs; it is not a separate mechanical-debounce guarantee.

## One response per round

waiting_for_move is 1 when a round opens. The first directional press sets it to 0, increments num_correct or num_wrong, and switches off the LED. Only the next Timer0 round can set it back to 1.

old_joystick records each sample even when responses are disabled. The edge helper detects released-to-pressed transitions, so a held direction cannot repeatedly score or automatically answer the next round.

Equal Timer0 and RIT priorities prevent one handler interrupting the other's shared-state update. volatile requests actual accesses; it does not provide that protection by itself.

## Direction and score rules

Remainders 0/1/2/3 select LED11/10/9/8 and UP/LEFT/RIGHT/DOWN.

Expected directions: RIGHT, RIGHT, DOWN, DOWN, UP, DOWN, RIGHT, RIGHT, RIGHT, LEFT.

The paper does not assign a penalty for no movement; a missed round leaves both counters unchanged. Centre/select is ignored. Simultaneous new direction presses count as wrong rather than choosing an arbitrary direction.

## The tenth round still gets three seconds

Timer0 shows the first LED at 3 seconds and the tenth at 30 seconds. It scores the game at 33 seconds, after the last response window. There are 11 Timer0 interrupts but only 10 LCG calls. The scoring branch stops both timers before displaying the result.

num_correct > num_wrong lights LED4. Otherwise, including a tie, LED5 lights. No later input should clear the result LED.
