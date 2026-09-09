# 2025-01-29 A2: affine transformation and blinking LEDs

Source: ../../02_ORIGINAL_MATERIALS/Exams/ARM questions/20250129_A.pdf

The two application source files are designed for the existing Official Combined Exam API template. They are not a standalone firmware project: the template supplies startup, CMSIS headers, exam_api.c and peripheral libraries.

## Use in a copy of the starting project

1. Replace the copied project's Source/sample.c with the supplied sample.c.
2. Add bitwiseAffineTransformation.s to the Keil target using the template's ARMASM assembly configuration.
3. Exclude Source/button_EXINT/IRQ_button.c, Source/RIT/IRQ_RIT.c, and Source/timer/IRQ_timer.c from this target's build. The new sample.c owns EINT0, EINT1, RIT and TIMER0. Keep their lib_*.c files and exam_api.c included. Unused vector handlers remain supplied by startup's weak defaults.
4. Keep the existing startup, system, linker and include-path configuration. Do not add a second main function or second definition of bitwiseAffineTransformation.

## Explicit behavior choices

- INT0 captures TIMER1 at its initial interrupt and displays the byte XOR after debounce confirmation. It stops previous blinking.
- KEY1 transforms the stored displayed value, including during the blink's dark phase, and restarts with a complete 250 ms visible phase.
- An initial KEY1 press transforms the initial value zero.
- If both button events are confirmed on the same RIT tick, INT0 is processed first, then KEY1.
- RIT supplies a 10 ms debounce tick with three required pressed samples. TIMER0 alone controls the 250 ms blink phases.
- All four used interrupts share priority 2, preventing mutual preemption while shared display state is updated.

## Method

For each of eight rows, AND the row byte with b, XOR its eight bits to obtain parity, and append that parity to the result. The first row becomes output bit 7. XOR the assembled result with c. The assembly uses R0-R2 for arguments and R0 for the return value; R4-R7 are saved and restored.

The question 1 example uses F8 7C 3E 1F 8F C7 E3 F1. With b=AA and c=63 its output is C9. Question 2 instead uses 8F C7 E3 F1 F8 7C 3E 1F. The sample counter 42AA gives b=42 XOR AA=E8; Question 2's transformation then returns 56.

TIMER1 uses MR0=FFFF, PR=0, and reset-on-match without interrupt. TIMER0 uses interrupt-plus-reset on MR0 with a 250 ms interval. Its full visible/dark cycle is 500 ms. The API computes the match from the actual peripheral clock; at 25 MHz, MR0 is 6,250,000 with PR=0.

## Verification

Run verify.py with Python and the existing workspace LLVM/Unicorn verification dependencies. It assembles the delivered instruction sequence through the existing ARMASM-to-GNU directive adapter, runs it on an emulated Cortex-M3, checks preserved registers and the stack, and checks application events using mocked peripheral functions. This does not verify native Keil ARMASM assembly, real timer timing, or a physical board.
