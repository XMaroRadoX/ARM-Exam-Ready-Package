param([string]$Root = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$atlas = Join-Path $Root 'Exam Atlas and Code Patterns\ARM_EXAM_ATLAS'
$links = Import-Csv (Join-Path $atlas 'indexes\exam_pattern_links.csv')
$patterns = Import-Csv (Join-Path $atlas 'indexes\patterns.csv')
$output = Join-Path $Root 'Start Here\api-and-pattern-coverage.md'

$coverage = @{
'PAT-AAPCS-NONLEAF-001'=@('ASSEMBLY','FULL','01_aapcs/nonleaf_function.s','No C API; PUSH/POP, LR and preserved-register rules are the implementation.','Use whenever the routine executes BL.');
'PAT-AAPCS-STACK-SAFETY-001'=@('ASSEMBLY','FULL','01_aapcs/nonleaf_function.s; 01_aapcs/five_to_seven_arguments.s','No C API; enforced by the assembly prologue/epilogue.','Keep SP 8-byte aligned at public calls and restore it on every exit.');
'PAT-MEM-MATRIX-ROW-MAJOR-001'=@('ASSEMBLY / C','FULL','02_algorithms/matrix_row_major_byte.s','Normal C indexing or assembly base + row*columns + column.','Change element scale for words; use columns, not rows, as stride.');
'PAT-FLOW-NESTED-LOOP-001'=@('ASSEMBLY / C','FULL','02_algorithms/nested_search_with_break.s','Language/control-flow pattern; no device API.','Preserve outer state and reset the inner index each row.');
'PAT-STATE-IRQ-HANDOFF-001'=@('C / INTERRUPTS','FULL','03_board/button_debounce_event.c; 03_board/joystick_state_machine.c','exam_events_set, exam_events_take, exam_critical_enter, exam_critical_exit','Shared callback/foreground objects remain volatile; copy multi-field state atomically.');
'PAT-GPIO-EVENT-001'=@('C / BOARD','FULL','03_board/button_debounce_event.c','exam_led_*, exam_buttons_start, exam_button_irq_start, exam_button_pressed','Use the callback API normally; claim exact handler ownership only when required.');
'PAT-ALG-RECURRENCE-001'=@('ASSEMBLY / C','FULL','02_algorithms/recurrence_into_array.s','No device API; callable assembly routine plus C oracle/policy function.','Localize seeds, recurrence formula, length and stop rule.');
'PAT-TIMER-OWNERSHIP-001'=@('C / BOARD','FULL','03_board/periodic_timer.c; 03_board/free_running_timer.c; 03_board/multi_timer_state.c','exam_timer_clock_divider, exam_timer_prescaler, exam_timer_match, start/stop/reset/count','Assign one purpose and one vector owner per timer.');
'PAT-TIMER-PERIODIC-001'=@('C / BOARD','FULL','03_board/periodic_timer.c','exam_timer_every_ms, exam_timer_every_hz, exam_timer_match','Match actions expose interrupt, reset and stop choices.');
'PAT-STATE-EVENT-LOOP-001'=@('C / STATE','FULL','03_board/multi_timer_state.c','exam_events_set, exam_events_take','Callbacks capture; exam_user_loop performs long work.');
'PAT-CPU-FLAGS-001'=@('ASSEMBLY / CPU','FULL','04_rare_dangerous/apsr_flags.s','No C API; ADDS/SUBS/CMP or explicit APSR access implements the contract.','Do not destroy required flags after producing them.');
'PAT-MEM-WORD-ARRAY-001'=@('ASSEMBLY / C','FULL','02_algorithms/array_scan_word.s','Normal pointer API; use LDR/STR with index LSL #2 in assembly.','Resolve signedness separately from element width.');
'PAT-MEM-BYTE-ARRAY-001'=@('ASSEMBLY / C','FULL','02_algorithms/matrix_row_major_byte.s; 02_algorithms/digit_extract_and_rebuild.s','Normal pointer API; use LDRB/LDRSB and STRB.','Use LDRSB only for signed bytes.');
'PAT-STATE-DEBOUNCE-001'=@('C / BOARD','FULL','03_board/button_debounce_event.c','exam_buttons_start, exam_buttons_confirmation_ms','Default confirmation is 50 ms; press and release are distinct events.');
'PAT-ADC-SAMPLE-001'=@('C / BOARD','FULL','03_board/adc_to_leds.c','exam_pot_start, exam_pot_read, exam_adc_read','Raw result is 0..4095; validate freshness/status before use.');
'PAT-DAC-STREAM-001'=@('C / BOARD','FULL','03_board/dac_table_stream.c','exam_dac_write, exam_dac_percent, exam_dac_silence','Samples are 0..1023; timer cadence and table wrap remain exam policy.');
'PAT-TIMER-FREE-RUNNING-001'=@('C / BOARD','FULL','03_board/free_running_timer.c','exam_timer_prescaler, exam_timer_reset, exam_timer_start, exam_timer_count','Do not accidentally configure reset-on-match when a continuously increasing seed is required.');
'PAT-ALG-GRAPH-SEARCH-001'=@('ASSEMBLY / C','PARTIAL','02_algorithms/matrix_row_major_byte.s; 02_algorithms/nested_search_with_break.s','No generic device API. Historical maze/DFS/Kruskal answers provide variants.','Addressing/loop pieces are canonical, but no single graph routine covers wavefront, DFS and Kruskal; several older historical answers remain incomplete.');
'PAT-ALG-FREQUENCY-COUNT-001'=@('ASSEMBLY / C','PARTIAL','Historical BullsAndCows and Mastermind answer sources','No device API. Use bounded histogram or matched-element tracking.','Exam-specific complete examples exist, but the standalone template library lacks a dedicated frequency-count source.');
'PAT-FLOW-EARLY-BREAK-001'=@('ASSEMBLY / C','FULL','02_algorithms/nested_search_with_break.s','No device API.','Every early exit must restore the same stack and preserved registers.');
'PAT-AAPCS-STACKED-ARGS-001'=@('ASSEMBLY','FULL','01_aapcs/five_to_seven_arguments.s','No C API; the compiler places argument 5+ on the caller stack.','Capture original SP before PUSH or include the exact push size in offsets.');
'PAT-AAPCS-FOUR-ARGS-001'=@('ASSEMBLY','FULL','01_aapcs/leaf_function.s; 01_aapcs/nonleaf_function.s','No C API; R0-R3 carry the first four arguments.','Copy caller-saved arguments before BL if they are needed afterward.');
'PAT-ALG-FIXED-POINT-001'=@('ASSEMBLY / C','FULL','02_algorithms/fixed_point_recurrence.s','No board API; fixed-point scale is part of the routine contract.','Use signed wide multiply and the exact Q-format shift/rounding stated by the paper.');
'PAT-GPIO-JOYSTICK-001'=@('C / BOARD','FULL','03_board/joystick_state_machine.c','exam_joystick_start, exam_joystick_read, exam_joystick_first, exam_joystick_reset_first','Directions are bit masks; test with bitwise AND.');
'PAT-ALG-SORTING-001'=@('ASSEMBLY / C','PARTIAL','Historical 2023-02-07 insertion-sort answer; nested-loop and array templates','No device API. Sorting is an algorithm routine called from C or assembly.','A complete historical insertion sort exists, but the standalone template library lacks a dedicated generic sort file; the older Kaprekar answer is incomplete.');
'PAT-CPU-SVC-001'=@('ASSEMBLY / CPU','FULL','04_rare_dangerous/svc_handler.s','Default svc_dispatch plus EXAM_OWN_SVC_HANDLER for an exact assembly owner.','Decode immediate at stacked PC-2 and ensure only one SVC_Handler is linked.');
'PAT-TIMER-VECTOR-OWNERSHIP-001'=@('CONFIG / INTERRUPTS','FULL','03_board/multi_timer_state.c; 04_rare_dangerous/systick_raw.s','EXAM_OWN_TIMER0..3_HANDLER, EXAM_OWN_RIT_HANDLER, EXAM_OWN_SYSTICK_HANDLER and related switches','This is configuration and linker ownership, not a runtime API call.');
'PAT-CPU-EXCEPTION-FRAME-001'=@('ASSEMBLY / CPU','FULL','04_rare_dangerous/svc_handler.s','Default handler support and EXAM_OWN_SVC_HANDLER switch.','Use LR bit 2 to select MSP/PSP; stacked PC is at frame +24.');
}

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add('# API and assembly pattern coverage')
$lines.Add('')
$lines.Add('This report answers two different questions: whether the final project has a callable C API for hardware/state work, and whether non-API assembly/algorithm requirements have concrete source material that can be adapted during an exam.')
$lines.Add('')
$lines.Add('`FULL` means an appropriate implementation or canonical source shape is present. It does not mean every new exam is solved without adaptation. `PARTIAL` means useful implementations exist, but the standalone generic source library is missing a complete family-level template.')
$lines.Add('')
$lines.Add('## Executive result')
$lines.Add('')
$lines.Add('- Board APIs: full coverage for GPIO/buttons, joystick, timers 0-3, RIT, SysTick, ADC, DAC, debounce, event flags and critical sections.')
$lines.Add('- ABI/CPU requirements: covered by assembly templates and ownership switches, not by inappropriate C wrappers.')
$lines.Add('- Generic algorithm support: full for recurrence, fixed point, arrays, matrices, nested loops and early exit; partial for sorting, frequency counting and the broad graph-search family.')
$lines.Add('- No history-driven need exists for CAN, MIDI/music, LCD/GLCD, touch-panel or PCON APIs.')
$lines.Add('')
$lines.Add('## Coverage matrix')
$lines.Add('')
$lines.Add('| Pattern | Layer | Coverage | Concrete support | API or mechanism | Adaptation boundary |')
$lines.Add('|---|---|---|---|---|---|')
foreach ($pattern in $patterns) {
    $c = $coverage[$pattern.pattern_id]
    if ($null -eq $c) { throw "No coverage entry for $($pattern.pattern_id)" }
    $lines.Add(('| `{0}` / `{1}` | {2} | **{3}** | `{4}` | {5} | {6} |' -f
        $pattern.pattern_id, $pattern.primary_tag, $c[0], $c[1], $c[2], $c[3], $c[4]))
}

$lines.Add('')
$lines.Add('## Discovery across the indexed questions')
$lines.Add('')
foreach ($pattern in $patterns) {
    $questionIds = @($links | Where-Object pattern_id -eq $pattern.pattern_id | Select-Object -ExpandProperty question_id -Unique | Sort-Object)
    $examIds = @($questionIds | ForEach-Object { $_ -replace '-Q[12]$', '' } | Select-Object -Unique)
    $c = $coverage[$pattern.pattern_id]
    $patternPath = Get-ChildItem (Join-Path $atlas 'patterns') -Recurse -File -Filter "$($pattern.pattern_id).md" | Select-Object -First 1
    $relativePattern = if ($patternPath) { '../Exam Atlas and Code Patterns/ARM_EXAM_ATLAS/' + $patternPath.FullName.Substring($atlas.Length + 1).Replace('\','/') } else { '' }
    $lines.Add("### $($pattern.primary_tag) — $($questionIds.Count) questions")
    $lines.Add('')
    $lines.Add("- Pattern: [$($pattern.pattern_id)]($relativePattern)")
    $lines.Add("- Layer: $($c[0]); coverage: **$($c[1])**")
    $lines.Add("- Exams: $($examIds -join ', ')")
    $lines.Add("- Questions: $($questionIds -join ', ')")
    $lines.Add("- Use: $($c[3])")
    $lines.Add("- Important adaptation: $($c[4])")
    $lines.Add('')
}

$lines.Add('## What API coverage does not mean')
$lines.Add('')
$lines.Add('An API can initialize a timer, capture a button event, read ADC, write DAC or move an event safely to foreground. It cannot decide the new exam recurrence formula, matrix dimensions, comparison signedness, graph encoding, sorting order, stopping rule, SVC service semantics or returned flags. Those are answer logic. The package supplies source shapes and historical examples so that answer logic can be adapted without redesigning the platform.')
$lines.Add('')
$lines.Add('## Current gaps to close')
$lines.Add('')
$lines.Add('1. Add and assemble a standalone generic insertion-sort source covering signed/unsigned and ascending/descending policy points.')
$lines.Add('2. Add and assemble a standalone bounded frequency-count source, with an alternative matched-element form for small alphabets/digits.')
$lines.Add('3. Split graph support into standalone wavefront, explicit-stack DFS and component-relabel/Kruskal templates instead of treating one broad prose pattern as executable coverage.')
$lines.Add('4. Replace the seven generic historical assembly answers and six generic historical C answers identified by the completeness audit before calling all 23 exams solved.')

[System.IO.File]::WriteAllLines($output, $lines, [System.Text.UTF8Encoding]::new($false))
Write-Output "Wrote $output"
