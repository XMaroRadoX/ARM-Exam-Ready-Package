# Template cleanup and improvements

## Current submission layout

The USB handoff now has two plainly named directories:

```text
EXAM_HANDOFF/
├── ARM_Exam_Project/     Keil project copied and submitted
└── Study Material/       private guides, solutions, tests and reports
```

The submission project contains only the Keil project and its required source
support:

```text
ARM_Exam_Project/
├── Answer/
│   ├── exam_user.c
│   ├── exam_user.h
│   └── exam_asm.s
├── Source/
├── DebugConfig/
├── Build/                empty until Keil builds
├── Listings/             empty until Keil builds
├── ARM_Exam_Template.uvprojx
├── ARM_Exam_Template.uvoptx
└── EventRecorderStub.scvd
```

`EventRecorderStub.scvd` and the remaining `DebugConfig` file are Keil support
files also present in the professor's projects. They are not answer material,
but they are related to the simulator/debug configuration and therefore remain.

## Cleanup completed

- Replaced numbered staging names with `ARM_Exam_Project`, `Answer` and
  `Study Material`.
- Renamed the visible Keil group to `Answer Files`.
- Reduced `exam_user.c` to the three entry points used by the platform.
- Reduced `exam_user.h` to its required includes and public prototypes.
- Reduced `exam_asm.s` to a valid, AAPCS-compatible Thumb leaf-function shell.
- Removed tutorial recipes and command-like commentary from submitted answer
  files. Detailed guidance remains in `Study Material`.
- Reworded platform comments as API contracts, ranges, ownership rules and
  hardware explanations.
- Removed the stale duplicate `CA_Exam_LPC1768.dbgconf`.
- Removed generated objects, listings, maps, logs and user-specific Keil files
  from the submission directory after validation.
- Rebuilt the renamed project with Arm Compiler 6.22: 0 errors and 0 warnings.

The retained build evidence is
[`ARM_EXAM_CLEAN_TEMPLATE_BUILD.log`](../Tests%20and%20Reports/ARM_EXAM_CLEAN_TEMPLATE_BUILD.log).
It is deliberately outside the submitted project.

## Improvements worth making

### 1. Automated simulator execution — highest priority

The current clean build proves that the C and assembly sources compile,
assemble and link. It does not by itself prove that every API or future answer
has executed in the Keil simulator. A separate test configuration should call
the real linked assembly symbol, preserve sentinel values in R4-R11, check the
stack pointer before and after the call, and store an unmistakable pass/fail
word in RAM.

### 2. Small exam-specific test harness

A private harness can be copied into `Answer` while developing, then removed
before submission if the paper does not request it. It should test nominal,
boundary and invalid cases and compare results with a short independent C
reference. The Bulls and Cows learning project is the current worked example.

### 3. Physical-board smoke test

The project uses the LPC1768 device, startup file and interrupt table, so it is
structured for the board. A real LandTiger run is still needed to verify pin
wiring, active-low switches, debounce behavior, ADC values, DAC output and
timer clock assumptions. Until then the correct label is
`PHYSICAL_BOARD_NOT_TESTED`.

### 4. Optional API surface reduction per paper

The submission deliberately keeps the full historical API coverage in one
project. This makes the project larger than a single-question solution but
avoids missing a required timer, GPIO, joystick, ADC, DAC, RIT, SysTick, SVC or
fault primitive. After the paper is known, unused platform modules could be
excluded from the Keil build; doing that in advance is not recommended because
it trades a small size reduction for coverage risk.

### 5. Fresh clean-copy check before the exam

Create a temporary copy, open only `ARM_Exam_Template.uvprojx`, confirm that the
`Answer Files` group is expanded, build once, and verify zero errors and zero
warnings. Delete the generated `Build` and `Listings` contents from the USB
master only after the evidence log has been copied into `Study Material`.

## Changes not recommended

- Do not merge all platform code into `exam_user.c`; it would hide the answer
  among driver code and make submission review harder.
- Do not place the atlas, solved exams, reports or Markdown guides inside
  `ARM_Exam_Project`.
- Do not remove the startup, CMSIS device definitions or system-clock source;
  both simulator and hardware builds depend on them.
- Do not add CAN, MIDI, LCD or touch-panel code without a paper that needs it.
  The indexed 23-exam history does not justify that extra surface.

