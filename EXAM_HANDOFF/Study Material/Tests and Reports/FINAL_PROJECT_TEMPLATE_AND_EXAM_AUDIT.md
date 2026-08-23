# Final project coverage audit

## Submission boundary

The submitted project is `EXAM_HANDOFF/ARM_Exam_Project`.

- Markdown files in submitted project: **0**
- LCD, GLCD, touch-panel and font sources: **excluded**
- CAN sources: **excluded**
- MIDI/music sources: **excluded**
- Reports, study material and historical answers: retained under `Study Material`

## Scope derived from the 23 indexed exams

| Capability | Occurs in history | Submission implementation |
|---|---:|---|
| GPIO LEDs | yes | `exam_api.c`, `exam_board.c`, compatibility API |
| INT0, KEY1, KEY2 | yes | raw input, IRQ ownership and confirmed debounce |
| Joystick | yes | polling/event API and first-movement capture |
| Timers 0-3 | yes | periodic, free-running, match, reset, start/stop, counter read |
| RIT | yes | scheduler and raw modes |
| SysTick | yes | periodic and direct low-level support |
| ADC/potentiometer | yes | polling and conversion support |
| DAC/speaker waveform output | yes | 10-bit output, percentage output and silence |
| SVC/exception frame | yes | MSP/PSP frame selection and dispatch ownership |
| AAPCS/assembly integration | yes | startup, assembly answer unit and C-callable boundary |
| CAN | no | intentionally excluded |
| MIDI/music library | no | intentionally excluded |
| LCD/GLCD/touch/fonts | no | intentionally excluded by scope |
| PCON/sleep exercise | no | intentionally excluded |

## Keil verification

The final submission project was rebuilt with Arm Compiler 6.22.

`0 Error(s), 0 Warning(s)`

The current build log is `ARM_EXAM_CLEAN_TEMPLATE_BUILD.log` in this directory. This proves compilation,
assembly and linking for the LPC1768 target. It does not claim physical-board execution.

## Documentation-link verification

The repeatable checker in `Tools/test-markdown-links.ps1`
scans every Markdown document, resolves each relative local target from the
document containing it, and checks Markdown anchor fragments. The current run
checked 252 Markdown documents and 597 local links with **0 failures**.

## Historical-solution completeness audit

All 23 historical exam directories exist and each contains C, header and assembly answer
files. File presence alone is not accepted as completion.

Six Q2 C files and seven Q1 assembly files inherited generic template content. They are
therefore classified as incomplete until replaced and tested:

1. 2023-02-24: Q1 assembly is generic; Q2 SVC answer is exam-specific.
2. 2023-05-17: Q1 assembly and Q2 C/flags integration are generic.
3. 2023-09-18: Q1 assembly and Q2 button application are generic.
4. 2024-02-12: Q1 maze assembly and Q2 maze generator are generic.
5. 2024-02-28: Q1 shortest-path assembly and Q2 LED playback are generic.
6. 2024-07-09: Q1 DFS assembly and Q2 random-neighbor/SysTick integration are generic.
7. 2024-09-16: Q1 Kruskal assembly and Q2 two-button application are generic.

The remaining 16 exam folders contain exam-specific Q1 and Q2 source. Their existing
verification labels must still be read literally: a build or C reference test is not the same
as executing the linked ARM routine in the simulator.
