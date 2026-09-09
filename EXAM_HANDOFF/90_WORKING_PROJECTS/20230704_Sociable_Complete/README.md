# ARM exam of 4 July 2023 - complete solution

Start with **Detailed_Solution.pdf** for the full explanation. The same explanation is available as editable text in **Detailed_Solution.md**.

## Complete projects

- **Q1_Assembly/sample.uvprojx**: Question 1, with the assembly routine and a small C driver that checks the four examples in the paper.
- **Q2_Timer_LEDs/sample.uvprojx**: Question 2, including Question 1's assembly, the seven-element array, Timer 1, and LED output.

Both projects are independent copies of the package's **Official Combined Exam API** starting template. Extract the entire ZIP before opening a project. Select **SW_Debug** for the simulator or **LandTiger_LPC1768 (release)** for the board. Build before starting a debug session. The LPC1700 device pack and Arm Compiler must be installed in Keil.

## Files to study

1. `Q1_Assembly/Source/ASM_funct.s`: the complete assembly answer to Question 1.
2. `Q1_Assembly/Source/sample.c`: calls the assembly on the four paper examples.
3. `Q2_Timer_LEDs/Source/sample.c`: initializes the board and starts a two-second periodic Timer 1.
4. `Q2_Timer_LEDs/Source/timer/IRQ_timer.c`: the complete array-processing interrupt handler.
5. `Q2_Timer_LEDs/Source/ASM_funct.s`: the same assembly answer, included in the extended project.

If copying into your own copy of this same template, replace these files at their existing paths. Do not add a second `TIMER1_IRQHandler` in `sample.c`. The supplied projects are already wired correctly; no manual project edits are needed.

## Expected results

Question 1: after `tests_done` becomes 1, `results` must be `{1, 2, 5, 0}` and `tests_passed` must be 4.

Question 2: the result sequence is `{1, 2, 0, 5, 4, 2, 4}`, repeating every seven interrupts. LEDs: **LD4, LD5, all off, LD8, LD7, LD5, LD7**. The first result appears after the first two-second timer interval plus the computation time. `last_input`, `last_result`, and `interrupt_count` are available in the debugger.

## Validation

See `validation/results.json` for the current execution results, `validation/build_results.json` for native builds, and the four `.log` files for compiler/linker output. `validation/verify.py` is the repeatable check script. It accepts `--compiler-bin`, `--device-include`, and `--test-deps` for another installation. It requires Python, pyelftools, Unicorn, and the native Arm compiler. Run build and execution phases separately with `--build-only` and `--test-only` if needed.

Validation distinguishes native compile/link from emulated execution. The emulator executes the delivered native instructions; the interrupt tests mock the peripheral API calls. Physical hardware, real exception entry, and measured two-second wall-clock timing are not tested.
