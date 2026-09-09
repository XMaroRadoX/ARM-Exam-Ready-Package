# Solution Pattern and peripheral-helper upgrade

## Delivered

- All 78 coding-pattern pages and seven workflow pages now use explicit implementation mappings and complete projects. `PATTERN_COVERAGE.json` records the exact files, functions, resources, expected result, tests and source hashes for every page.
- There are 146 runnable pattern projects: 122 C/assembly algorithm variants and 24 board/integration projects. Each page links its baseline and variants directly, shows every replacement source file, names IRQ ownership, and includes expected values. Project READMEs contain exact replacement filenames.
- The supplied template, each generated project, the generated API reference and every API page expose the same 58-function interface. Fixed counts were removed from active checks.
- The seven active board recipes now contain complete code and direct links to their matching projects.

Representative complete projects include:

- buttons with RIT and Timer0; a SysTick sampling variant; raw Timer1 capture;
- ADC preview, an explicitly captured button sample, and a timed display sequence;
- Bulls-and-Cows, Mastermind, release-edge actions, and the rhythm-game ownership rules;
- DAC table streaming, button-triggered playback, a separate duration timer, and the paper's three-timer note sequence;
- periodic, one-shot, pause/resume, exact-tick, multi-match, prescaler/divider, and real CAP0.0 timer examples;
- complete SVC wrapper/dispatcher, register/stack arguments, non-leaf calls, shared objects, signed/unsigned byte and word algorithms, and tested algorithm drivers.

## API additions

| Addition | Current contract |
|---|---|
| `exam_timer_config_match` | Configures one MR0-MR3 channel and its interrupt/reset/stop actions while stopped; preserves the other channels and counters. |
| `exam_timer_set_prescaler` | Sets PR while stopped, clears PC, and preserves TC and match settings. |
| `exam_timer_set_clock_divider` | Sets the selected timer divider to 1, 2, 4, or 8 while stopped, preserving other PCLK selections and timer state. |
| `exam_timer_match_happened` | Tests MR0-MR3 in one saved acknowledgement mask without reading or clearing hardware. |
| `exam_timer_capture_happened` | Tests CR0-CR1 in the saved mask without reading or clearing hardware. |
| `exam_joystick_released_edges` | Returns five-bit release edges using `(previous, current)` and no internal state. |

`EXAM_MATCH_INTERRUPT`, `EXAM_MATCH_RESET`, and `EXAM_MATCH_STOP` may be combined or omitted. Advanced timer calls reject invalid inputs before mutation and require a powered, initialized, stopped timer. A handler acknowledges once and tests its saved flags. Basic tick/ms/hz setup still sets PR to zero, so an advanced prescaler follows basic configuration.

No restart helper, automatic joystick repeat/filter, callback scheduler, generic event counter/queue, microsecond API, DAC playback service, or renamed raw peripheral alias was added. Existing signatures, timer modes, debounce behaviour and LED numbering remain unchanged.

RIT configuration now disables the source and counter, establishes its clock, clears RIMASK, installs the interval, resets the counter, clears the hardware/controller pending state, then enables its IRQ while leaving it stopped.

## Pattern corrections

The audit corrected misleading or incomplete teaching mappings, including sorting versus maximum finding, reachable-node count versus shortest distance, the indirect recurrence versus Fibonacci, maximum traversal versus summation, byte versus word row-major offsets, the Q15 recurrence trace, APSR flag meaning, signed/unsigned comparisons, and the February 2023 raw-interrupt timer description. Exam-derived games and timer examples use explicit named sources instead of an automatically selected “first related exam.”

## Verification completed

- Unchanged template native baseline: Keil MDK-ARM Lite 5.41 / Arm Compiler 6.22, LPC1700 device pack 2.7.1: 0 errors, 0 warnings.
- Native projects: 149/149 `SW_Debug` targets linked successfully. This includes all 146 delivered pattern projects and all three existing course projects. Four C99-compatibility warnings remain in pre-existing DFS/recurrence fixtures; there were no native errors.
- Algorithms: 61 maintained C/reference plus actual Thumb suites passed, with 470 assertions and existing SP/R4-R11 checks.
- Production peripheral code: 70,340 modeled checks passed, including all match channels/actions, all dividers, invalid/no-partial-change cases, stale RIT state, W1C acknowledgement, NVIC pending/set/clear state, masked-interrupt restoration, ADC capture, event-bit merging, button bounce/hold/reconfiguration, DAC, and joystick release combinations.
- Complete flows: all 24 board projects passed explicit scenario execution, including ADC freshness, ordered inputs, game persistence, rhythm first-movement-only behaviour, DAC wrap/stop, and three-timer ownership.
- Coverage agreement: 85/85 pages, 146/146 projects, 1,083 displayed/downloadable replacement files and 58/58 API declarations/docs/pages passed 25,093 agreement checks.
- Compatibility: all 48 question folders passed the current-interface check; course C/Thumb checks and the workstation's 38,086 structural checks passed.
- Portal: 465 student pages passed link, copy-control, contrast, long-listing and generated-page checks. Pattern variant navigation and desktop/narrow layouts passed browser inspection.
- Search: 23 reviewed exams and 48 questions remain mapped. Exact-function/date/relevance tests passed against the combined corpus, including `digitSum`, `Q1 Timer0`, Hofstadter, `exam_timer_config_ms`, `fifth argument`, `LDRSB`, and variant-specific records.
- The integrated ASM Reference remains available and its own validation/browser checks pass.

## Limits

Electrical button bounce, real elapsed time, analog signal quality, speaker output, automatic NVIC arbitration, PLL startup, SVC hardware entry/return, and physical output were not tested on an LPC1768 board. Hardware-independent logic, native compilation/linking, register semantics and explicit handler flows were tested separately as described above.

## Maintenance and integration

`PATTERN_MAINTENANCE.md` documents the isolated rebuild, native build gate, O0 simulation-image rationale, report interpretation and integration rules. The final package was rebuilt from the latest combined sources after the ASM-reference and search upgrades were integrated. Source conflicts were merged file by file. Other worktrees were not modified. Integration uses a last-moment live hash check, exact-file backups and post-copy hash verification; it never replaces the shared tree with an older snapshot.
