# API and assembly pattern coverage

This report answers two different questions: whether the final project has a callable C API for hardware/state work, and whether non-API assembly/algorithm requirements have concrete source material that can be adapted during an exam.

`FULL` means an appropriate implementation or canonical source shape is present. It does not mean every new exam is solved without adaptation. `PARTIAL` means useful implementations exist, but the standalone generic source library is missing a complete family-level template.

## Executive result

- Board APIs: full coverage for GPIO/buttons, joystick, timers 0-3, RIT, SysTick, ADC, DAC, debounce, event flags and critical sections.
- ABI/CPU requirements: covered by assembly templates and ownership switches, not by inappropriate C wrappers.
- Generic algorithm support: full for recurrence, fixed point, arrays, matrices, nested loops and early exit; partial for sorting, frequency counting and the broad graph-search family.
- No history-driven need exists for CAN, MIDI/music, LCD/GLCD, touch-panel or PCON APIs.

## Coverage matrix

| Pattern | Layer | Coverage | Concrete support | API or mechanism | Adaptation boundary |
|---|---|---|---|---|---|
| `PAT-ALG-SORTING-001` / `alg:sorting` | ASSEMBLY / C | **PARTIAL** | `Historical 2023-02-07 insertion-sort answer; nested-loop and array templates` | No device API. Sorting is an algorithm routine called from C or assembly. | A complete historical insertion sort exists, but the standalone template library lacks a dedicated generic sort file; the older Kaprekar answer is incomplete. |
| `PAT-ALG-RECURRENCE-001` / `alg:recurrence` | ASSEMBLY / C | **FULL** | `02_algorithms/recurrence_into_array.s` | No device API; callable assembly routine plus C oracle/policy function. | Localize seeds, recurrence formula, length and stop rule. |
| `PAT-ALG-GRAPH-SEARCH-001` / `alg:graph-search` | ASSEMBLY / C | **PARTIAL** | `02_algorithms/matrix_row_major_byte.s; 02_algorithms/nested_search_with_break.s` | No generic device API. Historical maze/DFS/Kruskal answers provide variants. | Addressing/loop pieces are canonical, but no single graph routine covers wavefront, DFS and Kruskal; several older historical answers remain incomplete. |
| `PAT-ALG-FREQUENCY-COUNT-001` / `alg:frequency-count` | ASSEMBLY / C | **PARTIAL** | `Historical BullsAndCows and Mastermind answer sources` | No device API. Use bounded histogram or matched-element tracking. | Exam-specific complete examples exist, but the standalone template library lacks a dedicated frequency-count source. |
| `PAT-ALG-FIXED-POINT-001` / `alg:fixed-point` | ASSEMBLY / C | **FULL** | `02_algorithms/fixed_point_recurrence.s` | No board API; fixed-point scale is part of the routine contract. | Use signed wide multiply and the exact Q-format shift/rounding stated by the paper. |
| `PAT-FLOW-NESTED-LOOP-001` / `flow:nested-loop` | ASSEMBLY / C | **FULL** | `02_algorithms/nested_search_with_break.s` | Language/control-flow pattern; no device API. | Preserve outer state and reset the inner index each row. |
| `PAT-FLOW-EARLY-BREAK-001` / `flow:early-break` | ASSEMBLY / C | **FULL** | `02_algorithms/nested_search_with_break.s` | No device API. | Every early exit must restore the same stack and preserved registers. |
| `PAT-MEM-BYTE-ARRAY-001` / `mem:byte-array` | ASSEMBLY / C | **FULL** | `02_algorithms/matrix_row_major_byte.s; 02_algorithms/digit_extract_and_rebuild.s` | Normal pointer API; use LDRB/LDRSB and STRB. | Use LDRSB only for signed bytes. |
| `PAT-MEM-WORD-ARRAY-001` / `mem:word-array` | ASSEMBLY / C | **FULL** | `02_algorithms/array_scan_word.s` | Normal pointer API; use LDR/STR with index LSL #2 in assembly. | Resolve signedness separately from element width. |
| `PAT-MEM-MATRIX-ROW-MAJOR-001` / `mem:matrix-row-major` | ASSEMBLY / C | **FULL** | `02_algorithms/matrix_row_major_byte.s` | Normal C indexing or assembly base + row*columns + column. | Change element scale for words; use columns, not rows, as stride. |
| `PAT-AAPCS-FOUR-ARGS-001` / `abi:four-register-args` | ASSEMBLY | **FULL** | `01_aapcs/leaf_function.s; 01_aapcs/nonleaf_function.s` | No C API; R0-R3 carry the first four arguments. | Copy caller-saved arguments before BL if they are needed afterward. |
| `PAT-AAPCS-STACKED-ARGS-001` / `abi:stacked-args` | ASSEMBLY | **FULL** | `01_aapcs/five_to_seven_arguments.s` | No C API; the compiler places argument 5+ on the caller stack. | Capture original SP before PUSH or include the exact push size in offsets. |
| `PAT-AAPCS-NONLEAF-001` / `abi:nonleaf` | ASSEMBLY | **FULL** | `01_aapcs/nonleaf_function.s` | No C API; PUSH/POP, LR and preserved-register rules are the implementation. | Use whenever the routine executes BL. |
| `PAT-CPU-FLAGS-001` / `cpu:flags` | ASSEMBLY / CPU | **FULL** | `04_rare_dangerous/apsr_flags.s` | No C API; ADDS/SUBS/CMP or explicit APSR access implements the contract. | Do not destroy required flags after producing them. |
| `PAT-CPU-SVC-001` / `cpu:svc` | ASSEMBLY / CPU | **FULL** | `04_rare_dangerous/svc_handler.s` | Default svc_dispatch plus EXAM_OWN_SVC_HANDLER for an exact assembly owner. | Decode immediate at stacked PC-2 and ensure only one SVC_Handler is linked. |
| `PAT-CPU-EXCEPTION-FRAME-001` / `cpu:exception-frame` | ASSEMBLY / CPU | **FULL** | `04_rare_dangerous/svc_handler.s` | Default handler support and EXAM_OWN_SVC_HANDLER switch. | Use LR bit 2 to select MSP/PSP; stacked PC is at frame +24. |
| `PAT-TIMER-OWNERSHIP-001` / `board:timer` | C / BOARD | **FULL** | `03_board/periodic_timer.c; 03_board/free_running_timer.c; 03_board/multi_timer_state.c` | exam_timer_clock_divider, exam_timer_prescaler, exam_timer_match, start/stop/reset/count | Assign one purpose and one vector owner per timer. |
| `PAT-GPIO-EVENT-001` / `board:gpio` | C / BOARD | **FULL** | `03_board/button_debounce_event.c` | exam_led_*, exam_buttons_start, exam_button_irq_start, exam_button_pressed | Use the callback API normally; claim exact handler ownership only when required. |
| `PAT-GPIO-JOYSTICK-001` / `board:joystick` | C / BOARD | **FULL** | `03_board/joystick_state_machine.c` | exam_joystick_start, exam_joystick_read, exam_joystick_first, exam_joystick_reset_first | Directions are bit masks; test with bitwise AND. |
| `PAT-ADC-SAMPLE-001` / `board:adc` | C / BOARD | **FULL** | `03_board/adc_to_leds.c` | exam_pot_start, exam_pot_read, exam_adc_read | Raw result is 0..4095; validate freshness/status before use. |
| `PAT-DAC-STREAM-001` / `board:dac` | C / BOARD | **FULL** | `03_board/dac_table_stream.c` | exam_dac_write, exam_dac_percent, exam_dac_silence | Samples are 0..1023; timer cadence and table wrap remain exam policy. |
| `PAT-STATE-EVENT-LOOP-001` / `state:event-loop` | C / STATE | **FULL** | `03_board/multi_timer_state.c` | exam_events_set, exam_events_take | Callbacks capture; exam_user_loop performs long work. |
| `PAT-STATE-DEBOUNCE-001` / `state:debounce` | C / BOARD | **FULL** | `03_board/button_debounce_event.c` | exam_buttons_start, exam_buttons_confirmation_ms | Default confirmation is 50 ms; press and release are distinct events. |
| `PAT-TIMER-PERIODIC-001` / `timing:periodic` | C / BOARD | **FULL** | `03_board/periodic_timer.c` | exam_timer_every_ms, exam_timer_every_hz, exam_timer_match | Match actions expose interrupt, reset and stop choices. |
| `PAT-TIMER-FREE-RUNNING-001` / `timing:free-running` | C / BOARD | **FULL** | `03_board/free_running_timer.c` | exam_timer_prescaler, exam_timer_reset, exam_timer_start, exam_timer_count | Do not accidentally configure reset-on-match when a continuously increasing seed is required. |
| `PAT-AAPCS-STACK-SAFETY-001` / `risk:stack-alignment` | ASSEMBLY | **FULL** | `01_aapcs/nonleaf_function.s; 01_aapcs/five_to_seven_arguments.s` | No C API; enforced by the assembly prologue/epilogue. | Keep SP 8-byte aligned at public calls and restore it on every exit. |
| `PAT-STATE-IRQ-HANDOFF-001` / `risk:irq-shared-state` | C / INTERRUPTS | **FULL** | `03_board/button_debounce_event.c; 03_board/joystick_state_machine.c` | exam_events_set, exam_events_take, exam_critical_enter, exam_critical_exit | Shared callback/foreground objects remain volatile; copy multi-field state atomically. |
| `PAT-TIMER-VECTOR-OWNERSHIP-001` / `risk:vector-ownership` | CONFIG / INTERRUPTS | **FULL** | `03_board/multi_timer_state.c; 04_rare_dangerous/systick_raw.s` | EXAM_OWN_TIMER0..3_HANDLER, EXAM_OWN_RIT_HANDLER, EXAM_OWN_SYSTICK_HANDLER and related switches | This is configuration and linker ownership, not a runtime API call. |

## Discovery across the indexed questions

### alg:sorting — 3 questions

- Pattern: [PAT-ALG-SORTING-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-SORTING-001.md)
- Layer: ASSEMBLY / C; coverage: **PARTIAL**
- Exams: E2023-02-07, E2023-02-24
- Questions: E2023-02-07-Q1, E2023-02-07-Q2, E2023-02-24-Q1
- Use: No device API. Sorting is an algorithm routine called from C or assembly.
- Important adaptation: A complete historical insertion sort exists, but the standalone template library lacks a dedicated generic sort file; the older Kaprekar answer is incomplete.

### alg:recurrence — 18 questions

- Pattern: [PAT-ALG-RECURRENCE-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-RECURRENCE-001.md)
- Layer: ASSEMBLY / C; coverage: **FULL**
- Exams: E2023-02-24, E2023-07-04, E2023-09-18, E2024-02-28, E2024-07-09, E2025-02-12-A1, E2025-02-12-A2, E2025-07-01-A1, E2025-07-01-A1-Q3, E2025-07-01-A2, E2025-07-01-A2-Q3, E2026-02-03-A1, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2
- Questions: E2023-02-24-Q1, E2023-02-24-Q2, E2023-07-04-Q1, E2023-07-04-Q2, E2023-09-18-Q2, E2024-02-28-Q2, E2024-07-09-Q2, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1, E2025-07-01-A1-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q2, E2025-07-01-A2-Q3, E2026-02-03-A1-Q1, E2026-02-03-A3-Q1, E2026-02-03-A3-Q2, E2026-02-18-A1-Q1, E2026-02-18-A2-Q1
- Use: No device API; callable assembly routine plus C oracle/policy function.
- Important adaptation: Localize seeds, recurrence formula, length and stop rule.

### alg:graph-search — 7 questions

- Pattern: [PAT-ALG-GRAPH-SEARCH-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-GRAPH-SEARCH-001.md)
- Layer: ASSEMBLY / C; coverage: **PARTIAL**
- Exams: E2024-02-12, E2024-02-28, E2024-07-09, E2024-09-16
- Questions: E2024-02-12-Q1, E2024-02-12-Q2, E2024-02-28-Q1, E2024-02-28-Q2, E2024-07-09-Q1, E2024-07-09-Q2, E2024-09-16-Q1
- Use: No generic device API. Historical maze/DFS/Kruskal answers provide variants.
- Important adaptation: Addressing/loop pieces are canonical, but no single graph routine covers wavefront, DFS and Kruskal; several older historical answers remain incomplete.

### alg:frequency-count — 6 questions

- Pattern: [PAT-ALG-FREQUENCY-COUNT-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-FREQUENCY-COUNT-001.md)
- Layer: ASSEMBLY / C; coverage: **PARTIAL**
- Exams: E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2026-02-18-A1-Q2, E2026-02-18-A2-Q2, E2026-06-25-B1-Q1, E2026-06-25-B1-Q2, E2026-06-25-B2-Q1, E2026-06-25-B2-Q2
- Use: No device API. Use bounded histogram or matched-element tracking.
- Important adaptation: Exam-specific complete examples exist, but the standalone template library lacks a dedicated frequency-count source.

### alg:fixed-point — 4 questions

- Pattern: [PAT-ALG-FIXED-POINT-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/algorithms/PAT-ALG-FIXED-POINT-001.md)
- Layer: ASSEMBLY / C; coverage: **FULL**
- Exams: E2025-01-29-A1, E2025-02-12-A1, E2025-02-12-A2
- Questions: E2025-01-29-A1-Q1, E2025-02-12-A1-Q1, E2025-02-12-A1-Q2, E2025-02-12-A2-Q1
- Use: No board API; fixed-point scale is part of the routine contract.
- Important adaptation: Use signed wide multiply and the exact Q-format shift/rounding stated by the paper.

### flow:nested-loop — 20 questions

- Pattern: [PAT-FLOW-NESTED-LOOP-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/control-flow/PAT-FLOW-NESTED-LOOP-001.md)
- Layer: ASSEMBLY / C; coverage: **FULL**
- Exams: E2023-02-07, E2023-02-24, E2023-05-17, E2023-07-04, E2023-09-18, E2024-02-12, E2024-02-28, E2024-07-09, E2024-09-16, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2025-07-01-A2, E2026-02-03-A3, E2026-06-25-B2
- Questions: E2023-02-07-Q1, E2023-02-07-Q2, E2023-02-24-Q1, E2023-02-24-Q2, E2023-05-17-Q1, E2023-07-04-Q1, E2023-09-18-Q1, E2023-09-18-Q2, E2024-02-12-Q1, E2024-02-12-Q2, E2024-02-28-Q1, E2024-07-09-Q1, E2024-09-16-Q1, E2025-01-29-A1-Q1, E2025-01-29-A2-Q1, E2025-01-29-A2-Q2, E2025-01-29-A3-Q1, E2025-07-01-A2-Q2, E2026-02-03-A3-Q1, E2026-06-25-B2-Q1
- Use: Language/control-flow pattern; no device API.
- Important adaptation: Preserve outer state and reset the inner index each row.

### flow:early-break — 5 questions

- Pattern: [PAT-FLOW-EARLY-BREAK-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/control-flow/PAT-FLOW-EARLY-BREAK-001.md)
- Layer: ASSEMBLY / C; coverage: **FULL**
- Exams: E2023-02-07, E2024-02-12, E2025-01-29-A2, E2026-02-03-A2, E2026-06-25-B2
- Questions: E2023-02-07-Q1, E2024-02-12-Q1, E2025-01-29-A2-Q1, E2026-02-03-A2-Q1, E2026-06-25-B2-Q1
- Use: No device API.
- Important adaptation: Every early exit must restore the same stack and preserved registers.

### mem:byte-array — 11 questions

- Pattern: [PAT-MEM-BYTE-ARRAY-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-BYTE-ARRAY-001.md)
- Layer: ASSEMBLY / C; coverage: **FULL**
- Exams: E2023-02-07, E2023-02-24, E2024-02-12, E2024-02-28, E2024-07-09, E2024-09-16, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2026-02-03-A1, E2026-02-03-A2
- Questions: E2023-02-07-Q1, E2023-02-24-Q2, E2024-02-12-Q1, E2024-02-28-Q1, E2024-07-09-Q1, E2024-09-16-Q1, E2025-01-29-A1-Q1, E2025-01-29-A2-Q1, E2025-01-29-A3-Q1, E2026-02-03-A1-Q1, E2026-02-03-A2-Q1
- Use: Normal pointer API; use LDRB/LDRSB and STRB.
- Important adaptation: Use LDRSB only for signed bytes.

### mem:word-array — 13 questions

- Pattern: [PAT-MEM-WORD-ARRAY-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-WORD-ARRAY-001.md)
- Layer: ASSEMBLY / C; coverage: **FULL**
- Exams: E2023-07-04, E2025-02-12-A1, E2025-02-12-A2, E2025-07-01-A1, E2025-07-01-A2, E2026-02-03-A1, E2026-02-03-A2, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-07-04-Q2, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1, E2025-07-01-A1-Q2, E2025-07-01-A2-Q2, E2026-02-03-A1-Q1, E2026-02-03-A2-Q1, E2026-02-03-A3-Q1, E2026-02-03-A3-Q2, E2026-02-18-A1-Q1, E2026-02-18-A2-Q1, E2026-06-25-B1-Q1, E2026-06-25-B2-Q1
- Use: Normal pointer API; use LDR/STR with index LSL #2 in assembly.
- Important adaptation: Resolve signedness separately from element width.

### mem:matrix-row-major — 21 questions

- Pattern: [PAT-MEM-MATRIX-ROW-MAJOR-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/memory/PAT-MEM-MATRIX-ROW-MAJOR-001.md)
- Layer: ASSEMBLY / C; coverage: **FULL**
- Exams: E2023-02-24, E2023-05-17, E2023-09-18, E2024-02-12, E2024-02-28, E2024-07-09, E2024-09-16, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2025-02-12-A1, E2026-02-18-A2, E2026-06-25-B1
- Questions: E2023-02-24-Q1, E2023-02-24-Q2, E2023-05-17-Q1, E2023-05-17-Q2, E2023-09-18-Q2, E2024-02-12-Q1, E2024-02-12-Q2, E2024-02-28-Q1, E2024-07-09-Q1, E2024-09-16-Q1, E2024-09-16-Q2, E2025-01-29-A1-Q1, E2025-01-29-A2-Q1, E2025-01-29-A2-Q2, E2025-01-29-A3-Q1, E2025-02-12-A1-Q1, E2025-02-12-A1-Q2, E2026-02-18-A2-Q1, E2026-02-18-A2-Q2, E2026-06-25-B1-Q1, E2026-06-25-B1-Q2
- Use: Normal C indexing or assembly base + row*columns + column.
- Important adaptation: Change element scale for words; use columns, not rows, as stride.

### abi:four-register-args — 4 questions

- Pattern: [PAT-AAPCS-FOUR-ARGS-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-FOUR-ARGS-001.md)
- Layer: ASSEMBLY; coverage: **FULL**
- Exams: E2024-07-09, E2024-09-16, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2024-07-09-Q1, E2024-09-16-Q1, E2026-06-25-B1-Q1, E2026-06-25-B2-Q1
- Use: No C API; R0-R3 carry the first four arguments.
- Important adaptation: Copy caller-saved arguments before BL if they are needed afterward.

### abi:stacked-args — 5 questions

- Pattern: [PAT-AAPCS-STACKED-ARGS-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-STACKED-ARGS-001.md)
- Layer: ASSEMBLY; coverage: **FULL**
- Exams: E2024-09-16, E2025-07-01-A1, E2025-07-01-A2
- Questions: E2024-09-16-Q1, E2025-07-01-A1-Q1, E2025-07-01-A1-Q2, E2025-07-01-A2-Q1, E2025-07-01-A2-Q2
- Use: No C API; the compiler places argument 5+ on the caller stack.
- Important adaptation: Capture original SP before PUSH or include the exact push size in offsets.

### abi:nonleaf — 32 questions

- Pattern: [PAT-AAPCS-NONLEAF-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-NONLEAF-001.md)
- Layer: ASSEMBLY; coverage: **FULL**
- Exams: E2023-02-07, E2023-02-24, E2023-05-17, E2023-07-04, E2023-09-18, E2024-02-12, E2024-02-28, E2024-07-09, E2024-09-16, E2025-01-29-A1, E2025-01-29-A3, E2025-02-12-A1, E2025-02-12-A2, E2025-07-01-A1, E2025-07-01-A2, E2026-02-03-A1, E2026-02-03-A2, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-02-07-Q1, E2023-02-07-Q2, E2023-02-24-Q1, E2023-02-24-Q2, E2023-05-17-Q2, E2023-07-04-Q1, E2023-07-04-Q2, E2023-09-18-Q1, E2023-09-18-Q2, E2024-02-12-Q1, E2024-02-12-Q2, E2024-02-28-Q1, E2024-07-09-Q1, E2024-07-09-Q2, E2024-09-16-Q1, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2025-07-01-A1-Q2, E2025-07-01-A2-Q2, E2026-02-03-A1-Q1, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q1, E2026-02-18-A1-Q1, E2026-02-18-A1-Q2, E2026-02-18-A2-Q1, E2026-02-18-A2-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- Use: No C API; PUSH/POP, LR and preserved-register rules are the implementation.
- Important adaptation: Use whenever the routine executes BL.

### cpu:flags — 13 questions

- Pattern: [PAT-CPU-FLAGS-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/exceptions/PAT-CPU-FLAGS-001.md)
- Layer: ASSEMBLY / CPU; coverage: **FULL**
- Exams: E2023-05-17, E2023-09-18, E2024-02-12, E2024-09-16, E2025-01-29-A2, E2025-02-12-A1, E2025-07-01-A1-Q3, E2026-02-03-A1, E2026-02-03-A3, E2026-02-18-A2
- Questions: E2023-05-17-Q1, E2023-05-17-Q2, E2023-09-18-Q1, E2023-09-18-Q2, E2024-02-12-Q2, E2024-09-16-Q1, E2024-09-16-Q2, E2025-01-29-A2-Q2, E2025-02-12-A1-Q1, E2025-07-01-A1-Q3, E2026-02-03-A1-Q1, E2026-02-03-A3-Q2, E2026-02-18-A2-Q2
- Use: No C API; ADDS/SUBS/CMP or explicit APSR access implements the contract.
- Important adaptation: Do not destroy required flags after producing them.

### cpu:svc — 2 questions

- Pattern: [PAT-CPU-SVC-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/exceptions/PAT-CPU-SVC-001.md)
- Layer: ASSEMBLY / CPU; coverage: **FULL**
- Exams: E2023-02-07, E2023-02-24
- Questions: E2023-02-07-Q1, E2023-02-24-Q2
- Use: Default svc_dispatch plus EXAM_OWN_SVC_HANDLER for an exact assembly owner.
- Important adaptation: Decode immediate at stacked PC-2 and ensure only one SVC_Handler is linked.

### cpu:exception-frame — 1 questions

- Pattern: [PAT-CPU-EXCEPTION-FRAME-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/exceptions/PAT-CPU-EXCEPTION-FRAME-001.md)
- Layer: ASSEMBLY / CPU; coverage: **FULL**
- Exams: E2023-02-24
- Questions: E2023-02-24-Q2
- Use: Default handler support and EXAM_OWN_SVC_HANDLER switch.
- Important adaptation: Use LR bit 2 to select MSP/PSP; stacked PC is at frame +24.

### board:timer — 17 questions

- Pattern: [PAT-TIMER-OWNERSHIP-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/timers/PAT-TIMER-OWNERSHIP-001.md)
- Layer: C / BOARD; coverage: **FULL**
- Exams: E2023-02-07, E2023-07-04, E2024-02-12, E2024-02-28, E2024-07-09, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2025-02-12-A1, E2025-02-12-A2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-02-07-Q2, E2023-07-04-Q2, E2024-02-12-Q2, E2024-02-28-Q2, E2024-07-09-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- Use: exam_timer_clock_divider, exam_timer_prescaler, exam_timer_match, start/stop/reset/count
- Important adaptation: Assign one purpose and one vector owner per timer.

### board:gpio — 19 questions

- Pattern: [PAT-GPIO-EVENT-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/gpio-input/PAT-GPIO-EVENT-001.md)
- Layer: C / BOARD; coverage: **FULL**
- Exams: E2023-02-07, E2023-07-04, E2023-09-18, E2024-02-12, E2024-02-28, E2024-09-16, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2025-02-12-A1, E2025-02-12-A2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1, E2026-02-03-A2, E2026-02-03-A3, E2026-02-18-A1, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-02-07-Q2, E2023-07-04-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2024-02-28-Q2, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- Use: exam_led_*, exam_buttons_start, exam_button_irq_start, exam_button_pressed
- Important adaptation: Use the callback API normally; claim exact handler ownership only when required.

### board:joystick — 4 questions

- Pattern: [PAT-GPIO-JOYSTICK-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/gpio-input/PAT-GPIO-JOYSTICK-001.md)
- Layer: C / BOARD; coverage: **FULL**
- Exams: E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- Use: exam_joystick_start, exam_joystick_read, exam_joystick_first, exam_joystick_reset_first
- Important adaptation: Directions are bit masks; test with bitwise AND.

### board:adc — 10 questions

- Pattern: [PAT-ADC-SAMPLE-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/adc-dac/PAT-ADC-SAMPLE-001.md)
- Layer: C / BOARD; coverage: **FULL**
- Exams: E2023-05-17, E2025-02-12-A1, E2025-02-12-A2, E2026-02-03-A1, E2026-02-03-A2, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1
- Questions: E2023-05-17-Q1, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2, E2026-06-25-B1-Q1, E2026-06-25-B1-Q2
- Use: exam_pot_start, exam_pot_read, exam_adc_read
- Important adaptation: Raw result is 0..4095; validate freshness/status before use.

### board:dac — 10 questions

- Pattern: [PAT-DAC-STREAM-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/adc-dac/PAT-DAC-STREAM-001.md)
- Layer: C / BOARD; coverage: **FULL**
- Exams: E2025-01-29-A3, E2025-02-12-A1, E2025-02-12-A2, E2026-02-03-A1, E2026-02-03-A2, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2
- Questions: E2025-01-29-A3-Q1, E2025-01-29-A3-Q2, E2025-02-12-A1-Q1, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2
- Use: exam_dac_write, exam_dac_percent, exam_dac_silence
- Important adaptation: Samples are 0..1023; timer cadence and table wrap remain exam policy.

### state:event-loop — 14 questions

- Pattern: [PAT-STATE-EVENT-LOOP-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/state-machines/PAT-STATE-EVENT-LOOP-001.md)
- Layer: C / STATE; coverage: **FULL**
- Exams: E2023-07-04, E2023-09-18, E2024-02-12, E2024-02-28, E2024-09-16, E2025-01-29-A3, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-07-04-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2024-02-28-Q2, E2024-09-16-Q2, E2025-01-29-A3-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1-Q2, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- Use: exam_events_set, exam_events_take
- Important adaptation: Callbacks capture; exam_user_loop performs long work.

### state:debounce — 10 questions

- Pattern: [PAT-STATE-DEBOUNCE-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/state-machines/PAT-STATE-DEBOUNCE-001.md)
- Layer: C / BOARD; coverage: **FULL**
- Exams: E2023-02-07, E2023-09-18, E2024-02-12, E2024-09-16, E2025-01-29-A3, E2025-02-12-A1, E2026-02-03-A1, E2026-02-03-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-02-07-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2024-09-16-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- Use: exam_buttons_start, exam_buttons_confirmation_ms
- Important adaptation: Default confirmation is 50 ms; press and release are distinct events.

### timing:periodic — 15 questions

- Pattern: [PAT-TIMER-PERIODIC-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/timers/PAT-TIMER-PERIODIC-001.md)
- Layer: C / BOARD; coverage: **FULL**
- Exams: E2023-07-04, E2024-02-28, E2024-07-09, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2025-02-12-A1, E2025-02-12-A2, E2025-07-01-A1-Q3, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-07-04-Q2, E2024-02-28-Q2, E2024-07-09-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2025-07-01-A1-Q3, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q1, E2026-06-25-B2-Q2
- Use: exam_timer_every_ms, exam_timer_every_hz, exam_timer_match
- Important adaptation: Match actions expose interrupt, reset and stop choices.

### timing:free-running — 9 questions

- Pattern: [PAT-TIMER-FREE-RUNNING-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/timers/PAT-TIMER-FREE-RUNNING-001.md)
- Layer: C / BOARD; coverage: **FULL**
- Exams: E2023-02-07, E2024-02-12, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-02-07-Q2, E2024-02-12-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2026-02-18-A1-Q1, E2026-02-18-A2-Q1, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- Use: exam_timer_prescaler, exam_timer_reset, exam_timer_start, exam_timer_count
- Important adaptation: Do not accidentally configure reset-on-match when a continuously increasing seed is required.

### risk:stack-alignment — 28 questions

- Pattern: [PAT-AAPCS-STACK-SAFETY-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/aapcs/PAT-AAPCS-STACK-SAFETY-001.md)
- Layer: ASSEMBLY; coverage: **FULL**
- Exams: E2023-02-07, E2023-02-24, E2023-05-17, E2023-07-04, E2023-09-18, E2024-02-12, E2024-02-28, E2024-07-09, E2024-09-16, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2025-02-12-A1, E2025-02-12-A2, E2025-07-01-A1, E2025-07-01-A2, E2026-02-03-A1, E2026-02-03-A2, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-02-07-Q1, E2023-02-24-Q1, E2023-02-24-Q2, E2023-05-17-Q1, E2023-05-17-Q2, E2023-07-04-Q1, E2023-09-18-Q1, E2024-02-12-Q1, E2024-02-28-Q1, E2024-07-09-Q1, E2024-07-09-Q2, E2024-09-16-Q1, E2025-01-29-A1-Q1, E2025-01-29-A2-Q1, E2025-01-29-A3-Q1, E2025-02-12-A1-Q1, E2025-02-12-A2-Q1, E2025-07-01-A1-Q1, E2025-07-01-A1-Q2, E2025-07-01-A2-Q1, E2025-07-01-A2-Q2, E2026-02-03-A1-Q1, E2026-02-03-A2-Q1, E2026-02-03-A3-Q1, E2026-02-18-A1-Q1, E2026-02-18-A2-Q1, E2026-06-25-B1-Q1, E2026-06-25-B2-Q1
- Use: No C API; enforced by the assembly prologue/epilogue.
- Important adaptation: Keep SP 8-byte aligned at public calls and restore it on every exit.

### risk:irq-shared-state — 20 questions

- Pattern: [PAT-STATE-IRQ-HANDOFF-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/state-machines/PAT-STATE-IRQ-HANDOFF-001.md)
- Layer: C / INTERRUPTS; coverage: **FULL**
- Exams: E2023-02-07, E2023-07-04, E2023-09-18, E2024-02-12, E2024-02-28, E2024-09-16, E2025-01-29-A1, E2025-01-29-A2, E2025-01-29-A3, E2025-02-12-A1, E2025-02-12-A2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1, E2026-02-03-A2, E2026-02-03-A3, E2026-02-18-A1, E2026-02-18-A2, E2026-06-25-B1, E2026-06-25-B2
- Questions: E2023-02-07-Q2, E2023-07-04-Q2, E2023-09-18-Q2, E2024-02-12-Q2, E2024-02-28-Q2, E2024-09-16-Q2, E2025-01-29-A1-Q2, E2025-01-29-A2-Q2, E2025-01-29-A3-Q2, E2025-02-12-A1-Q2, E2025-02-12-A2-Q2, E2025-07-01-A1-Q3, E2025-07-01-A2-Q3, E2026-02-03-A1-Q2, E2026-02-03-A2-Q2, E2026-02-03-A3-Q2, E2026-02-18-A1-Q2, E2026-02-18-A2-Q2, E2026-06-25-B1-Q2, E2026-06-25-B2-Q2
- Use: exam_events_set, exam_events_take, exam_critical_enter, exam_critical_exit
- Important adaptation: Shared callback/foreground objects remain volatile; copy multi-field state atomically.

### risk:vector-ownership — 2 questions

- Pattern: [PAT-TIMER-VECTOR-OWNERSHIP-001](../Exam%20Atlas%20and%20Code%20Patterns/ARM_EXAM_ATLAS/patterns/timers/PAT-TIMER-VECTOR-OWNERSHIP-001.md)
- Layer: CONFIG / INTERRUPTS; coverage: **FULL**
- Exams: E2023-02-07, E2026-02-18-A1
- Questions: E2023-02-07-Q2, E2026-02-18-A1-Q2
- Use: EXAM_OWN_TIMER0..3_HANDLER, EXAM_OWN_RIT_HANDLER, EXAM_OWN_SYSTICK_HANDLER and related switches
- Important adaptation: This is configuration and linker ownership, not a runtime API call.

## What API coverage does not mean

An API can initialize a timer, capture a button event, read ADC, write DAC or move an event safely to foreground. It cannot decide the new exam recurrence formula, matrix dimensions, comparison signedness, graph encoding, sorting order, stopping rule, SVC service semantics or returned flags. Those are answer logic. The package supplies source shapes and historical examples so that answer logic can be adapted without redesigning the platform.

## Current gaps to close

1. Add and assemble a standalone generic insertion-sort source covering signed/unsigned and ascending/descending policy points.
2. Add and assemble a standalone bounded frequency-count source, with an alternative matched-element form for small alphabets/digits.
3. Split graph support into standalone wavefront, explicit-stack DFS and component-relabel/Kruskal templates instead of treating one broad prose pattern as executable coverage.
4. Replace the seven generic historical assembly answers and six generic historical C answers identified by the completeness audit before calling all 23 exams solved.
