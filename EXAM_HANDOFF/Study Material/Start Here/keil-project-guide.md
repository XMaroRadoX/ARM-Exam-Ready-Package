# Keil one-project usage

Open only `ARM_Exam_Project/ARM_Exam_Template.uvprojx`.

The Project pane must show one target, `ARM Exam`, and one expanded group,
`EDIT HERE - C AND ASM FIRST`. Its first entries are:

1. `exam_user.c` — C answer and callbacks.
2. `exam_asm.s` — assembly answer.
3. `exam_user.h` — declarations shared by the two answer units.

The remaining entries in the same group are linked platform/startup support and
normally remain unchanged.

## Simulator

The saved default is the Keil Cortex-M3 simulator. Build the `ARM Exam` target,
then use Debug > Start/Stop Debug Session. The linked image is the same LPC1768
image produced by the build. Register-level peripherals may require simulator
models or scripted stimuli; a successful build alone is not evidence that a
peripheral scenario executed.

## LPC1768 board

The same target retains the LPC1768 device, memory map, flash algorithm and
ULINK configuration. To use a board, open Options for Target > Debug, select the
available ULINK/CMSIS-DAP hardware adapter instead of Use Simulator, configure
its settings, rebuild and download. This remains theoretical until the actual
board, jumpers and probe are tested.

## If the files are hidden

Open the Project window and expand `ARM Exam`, then expand
`EDIT HERE - C AND ASM FIRST`. The supplied `.uvoptx` already records both as
expanded. If Keil overwrites the personal view state, expansion affects only
the display; it does not remove the files from the project.
