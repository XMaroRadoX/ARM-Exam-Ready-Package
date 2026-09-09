# 29 January 2025, C2 - Bit matrix transpose and XOR identity

Source: ../../02_ORIGINAL_MATERIALS/Exams/ARM questions/20250129_B.pdf

## Files

- `transpose.s`: complete ARMASM routine plus the Question 1 input and result storage.
- `Q1_main.c`: standalone C caller for inspecting the example result.
- `Q2_main.c`: complete button/timer application using the same assembly routine.
- `check.py`: native compile/link checks and explicitly labelled algorithm-model checks.

## Use with the current template

Use a copy of `../../01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/sample.uvprojx`.

For Question 1:
1. Replace the contents of the copy's `Source/sample.c` with `Q1_main.c`.
2. Add `transpose.s` to the project as an assembly source.
3. Build and watch `matrix_T` after the call. Expected: `8F C7 E3 F1 F8 7C 3E 1F`.

For Question 2:
1. Replace the contents of the copy's `Source/sample.c` with `Q2_main.c`.
2. Add `transpose.s` to the project as an assembly source.
3. Exclude the copy's `Source/button_EXINT/IRQ_button.c` and `Source/systick/IRQ_systick.c` from the build: Q2_main.c supplies those four handlers.
4. Keep the library implementation files, startup, and other default handlers.
5. Include exactly one main function. Q1_main.c and Q2_main.c are alternatives.

No existing template or solved answer was modified.

## Solution rules

- One byte represents one matrix row; column zero is byte bit seven (mask 0x80).
- Transpose moves A[i][j] to AT[j][i].
- The routine clears all destination bytes before setting any bits.
- Input and output must be separate, non-overlapping eight-byte buffers.
- R0 and R1 pass the addresses; no scalar is returned. R4-R8 and LR are saved in a 24-byte stack frame; R8 is included to keep the frame a multiple of eight.
- TIMER2 matches at 0xFFFF, resets, and produces no timer interrupt. The configured value is literal, not 0x10000.
- A byte stores the low eight bits of a timer reading; for example 0xABCD becomes 0xCD.
- The initial KEY1/KEY2 interrupt captures the reading. A 10 ms SysTick service confirms a held press using the template debounce helper configured for three samples. The captured reading is then accepted in main.
- KEY1 and KEY2 have independent counters, each limited to eight accepted presses.
- INT0 before both arrays are full is ignored; this is an explicit choice for an unspecified case.
- Exactly three transpose calls calculate transpose(A XOR B), transpose(A), and transpose(B).
- Compare all eight rows of the two sides. Clear the LEDs and light physical LD4 for equality, LD5 for inequality.
- The identity holds for all bit matrices with a correct transpose. LD5 diagnoses a mismatch; passing the identity alone does not prove that transpose is implemented correctly.
- C static arrays without explicit initializers are zero-initialized by the C runtime. The solution does not rely on that initial content; all inputs must be filled first and all transpose outputs are cleared by the routine.

## Verification scope

Run `check.py` with Python on this machine to compile and link both alternatives with the installed native Arm compiler and current template. Build products stay under `build/`.

The Python algorithm model checks the paper example, all 64 single-bit positions, and 1000 deterministic random input pairs, including double-transpose and XOR identities. These checks do not execute the assembled machine code and do not test physical button bounce, board timing, or LEDs.
