"""Board lessons extend the canonical peripheral chapters without new API names."""
from course_c import lesson
BOARD = [
lesson("board-start", "1. Project ownership and a safe baseline",
"""A peripheral is hardware performing input, output, or timing independently of normal instructions. A driver is code configuring and operating it. Your answer should initialize only the devices required by the question, and each interrupt vector must have one owner.

Copy the whole starting project. Build before changing logic. Source/sample.c owns foreground behavior; existing driver IRQ files own their handlers. Source/ASM_funct.s is the listed assembly file. Decide whether the question permits the Combined API, demands professor functions, or explicitly tests registers.

Build a responsibility table before adding features. Configuration, IRQ work, foreground processing, and output are separate responsibilities. Keeping those boundaries visible makes faults much easier to localize.""",
"/* Planning example, not extra handler definitions: */\n/* Timer0: 500 ms scheduling -> timer/IRQ_timer.c */\n/* RIT: 10 ms input sampling -> RIT/IRQ_RIT.c */\n/* main: state changes and assembly calls -> sample.c */",
"Unchanged copy builds → add LED output → build → add one time source → build → add one event consumer.",
"List the owner, trigger, shared data, and acknowledgement for Timer0 and RIT.",
["Read the existing handler files.", "Configuration is not the same as starting a timer."],
"Timer0 has one TIMER0_IRQHandler which snapshots/clears flags with exam_timer_ack. RIT has one RIT_IRQHandler which calls exam_rit_ack. Both configure before explicit start. Shared software events have named bits and one consumer.",
"Adding a second handler creates duplicate symbols. Starting everything at once hides which device caused failure.",
"Build the unchanged copied project and identify each file you will edit.", "Core|Build|IRQ", 1),

lesson("board-leds", "2. LEDs: physical labels versus logical bits",
"""The single-LED API uses the printed board labels 4 through 11: exam_led_on(11) turns on LD11. Whole-display writes use a byte mask: bit 0 controls LD11 and bit 7 controls LD4. A bit value of one means on.

A whole-byte write replaces the display pattern. Individual on/off/toggle helpers select one LED by its printed board label. one_hot clears the others and lights one LED. Separate a mathematical result from its encoded display: first inspect the result, then test the bit layout independently.

When a question mentions 'most significant digit', draw the physical LED order. Paper wording about number representation can invert the mapping you first expect.""",
"exam_led_write(0x81u);\n/* Physical LED4 and LED11 on; other six off. */\n(void)exam_led_one_hot(9u);\n/* Only physical LED9 on. */",
"0x81 sets bits 7 and 0 → LED4 and LED11. one_hot(9) selects LD9 and replaces that display with bit 2 only.",
"Display binary 10 on the least significant four LEDs while clearing the others.",
["Decimal 10 is binary 1010.", "Logical bits 0..3 correspond to LED11..LED8."],
"exam_led_write(0x0Au) turns on LED10 and LED8. Inspect these physical outputs separately before integrating the algorithm.",
"Old API indexes must be migrated to board labels using 11 - old_index. Labels outside 4..11 are rejected without changing the LEDs. Toggling when a full write was intended retains stale bits.",
"Predict the exact physical LEDs for masks 0x01,0x80,0x55.", "LED|Bits", 2),

lesson("board-buttons", "3. Buttons and raw external interrupts",
"""A raw button signal is an electrical level; an edge is a transition. Mechanical buttons can bounce, creating several transitions for one physical press. The external-interrupt hardware signals activity, but does not by itself implement a reliable one-press event.

The API normalizes pressed state, so exam_button_is_pressed returns a Boolean pressed meaning. The current EINT handlers initially acknowledge raw interrupts. For a debounced question, replace that raw acknowledgement with exam_debounce_begin in the one existing handler, then supply a periodic debounce tick.

Use raw inputs only when the exercise genuinely asks for raw behavior or your own explicit debounce scheme. Do not count IRQ entries as human presses.""",
"/* In the existing EINT0_IRQHandler, choose ONE flow: */\nexam_button_ack(EXAM_BUTTON_INT0); /* raw */\n/* OR replace that call with exam_debounce_begin(EXAM_BUTTON_INT0); */",
"A press bounces low/high/low → hardware can report several edges → a raw counter may increment repeatedly.",
"Why is inserting a delay loop inside EINT0_IRQHandler a poor debounce method?",
["It blocks the handler while other timing continues.", "CPU-cycle delays depend on clock and optimization."],
"Busy waiting lengthens interrupt latency and has an uncertain duration. Use a periodic stable-input check and publish one confirmed event, with release/re-arm behavior, instead.",
"Acknowledge and debounce-begin are alternative flows here, not two calls to paste together. Forgetting re-arm makes only the first press work.",
"Separate level, edge, raw interrupt, and confirmed press.", "Buttons|EINT|Debounce", 3),

lesson("board-irq", "4. Interrupt ownership, flags, and bounded work",
"""An IRQ vector connects a hardware interrupt to a function name. The startup file and target membership decide which implementation owns it. A handler should identify and acknowledge the actual source, capture minimal state, and return.

A timer can have multiple pending match/capture flags. exam_timer_ack returns a snapshot and clears them. Read it once, then test every enabled source in that snapshot with independent if statements. Calling ack separately for each test loses later information because the first call already cleared it.

Keep long array processing in foreground. A small fixed-time output update can stay in a timing-critical handler when the requirement needs it; the relevant distinction is bounded work and timing, not an absolute ban on every instruction beyond setting a flag.""",
"uint32_t pending = exam_timer_ack(EXAM_TIMER0);\nif (pending & 1u) exam_events_set(1u);\nif (pending & 2u) exam_events_set(2u);",
"MR0 and MR1 both pending → snapshot=3 → both independent conditions run → both event bits become pending.",
"What changes if the second condition is else if? What if ack is called again?",
["Simultaneous sources are not mutually exclusive.", "The snapshot survives hardware clearing."],
"else if processes only the first source when both are set. Calling ack again sees cleared flags. Use one snapshot and independent tests for all enabled sources.",
"An uncleared level can cause immediate repeated IRQ entry. A wrong handler name leaves the default handler active.",
"Demonstrate simultaneous-source handling and one owner per vector.", "IRQ|Timer|Acknowledgement", 4),

lesson("board-timers", "5. Timer0-Timer3: units, modes, and starting",
"""A timer counts peripheral-clock ticks. A match compares that count with a programmed value and may cause an interrupt, reset, or stop. Periodic mode repeats; one-shot stops after its event. The current helpers configure MR0 with PR=0 and use the selected timer's actual clock.

Milliseconds, hertz, and ticks are different inputs. The API converts milliseconds/hertz; do not apply a second conversion yourself. Configuration stops/resets but does not start Timer0-Timer3. Check the returned status, then call start explicitly.

A modulo counter without IRQ is not a full-range free-running counter. The compatibility FREE_RUNNING name aliases modulo behavior. For exact register questions, derive prescaler/match behavior from the supplied manual and required clock, not from a memorized constant.""",
"if (exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC)==EXAM_OK) {\n    exam_timer_start(EXAM_TIMER0);\n}",
"Configure 500 ms → timer remains stopped → start → match → handler acknowledges → periodic counter resets and continues.",
"Describe the changes needed for a single event after two seconds.",
["Change both the duration and mode.", "Still start explicitly and acknowledge the IRQ."],
"Use 2000u milliseconds and EXAM_TIMER_ONE_SHOT. Start once; after its match process the event without assuming another will occur. Restart deliberately when another one-shot is required.",
"Passing 500 ticks while meaning milliseconds produces the wrong rate. Ignoring a configuration error can leave the device stopped.",
"Explain period, frequency, ticks, mode, and start/stop lifecycle.", "Timer|Periodic|One-shot", 5),

lesson("board-debounce", "6. Debouncing: sample, confirm, emit, re-arm",
"""Debouncing asks whether a pressed level is stable long enough to count as one press. It needs a real periodic sample source. Configuration tells the state machine how often ticks happen; it does not create that source.

A maintained teaching recipe is 10 ms sampling with 50 ms confirmation, not a universal paper constant. Configure matching values, call debounce_begin from the existing button handler, call debounce_tick once per real sample interval, and consume confirmed events in foreground.

Repeated ticks while held must not create unlimited press events. Release and re-arm are part of the workflow. Test short bounces, a stable press, a long hold, release, and a second press on the actual board.""",
"/* Setup: check statuses, then start the selected tick source. */\n(void)exam_debounce_config(10u,50u);\n/* Existing EINT handler: */\n(void)exam_debounce_begin(EXAM_BUTTON_INT0);\n/* Existing 10 ms time-source handler: */\nexam_debounce_tick();\n/* Foreground: */\nuint32_t pressed = exam_button_events_take();",
"Raw edge starts confirmation → periodic stable samples accumulate → one event published → foreground takes it → release allows a later new press.",
"RIT actually runs every 20 ms but debounce_config says 10 ms. Why is this wrong?",
["The state machine counts calls using the configured interval.", "Software timing assumptions must match the real source."],
"Elapsed-time interpretation is wrong: confirmation may take approximately twice the intended wall time. Set both to the same real interval and retest press/hold/release behavior.",
"Calling debounce_tick in a fast main loop provides no defined interval. Stopping the tick source breaks re-arming.",
"Show two distinct presses producing two events, with no repeat from a hold.", "Buttons|Debounce|RIT|SysTick", 6),

lesson("board-systick", "7. SysTick and the CPU clock",
"""SysTick is the Cortex-M core's 24-bit system timer. Its width limits the interval representable at a given core clock. The API validates tick/millisecond configuration and starts SysTick immediately when successful, unlike Timer and RIT configuration.

There is no peripheral acknowledgement helper for SysTick in this API. Put a short periodic action in the single SysTick_Handler. If debounce uses it, stopping SysTick also stops debounce progress.

For periods beyond its range, use a slower hardware time source or count short ticks in software. State the divider and protect state shared with foreground. A divider adds a scheduling layer, not a different hardware clock.""",
"if (exam_systick_config_ms(10u) != EXAM_OK) {\n    /* handle invalid/range/clock configuration */\n}\n/* Existing SysTick_Handler: exam_debounce_tick(); */",
"Successful 10 ms configuration starts immediately → handler repeats each tick → five nominal intervals span 50 ms.",
"Can you paste a Timer0 acknowledgement into SysTick_Handler? What must a failed configuration do?",
["These are different interrupt sources.", "The application must not pretend the time base exists after failure."],
"No. SysTick has its own hardware semantics and no exam_systick_ack function. Handle failure visibly or stop the dependent workflow rather than running with an absent time source.",
"Assuming config leaves SysTick stopped creates startup races. Configuring a duration too large for 24 bits must not be ignored.",
"Distinguish SysTick start semantics and interval limits from Timer0.", "SysTick|Timing", 7),

lesson("board-rit", "8. RIT: a shared input sampling clock",
"""The Repetitive Interrupt Timer provides an independent periodic source suited to bounded sampling work. Configure it, check success, and start explicitly. Its handler must acknowledge RIT.

One 10 ms tick can drive debounce and joystick sampling if both share that interval. Give RIT one handler and one owner; do not configure it again from another component with a competing period.

If foreground sampling is notified by a bit, multiple delayed ticks may coalesce. For debounce tick accounting, execute the required small tick operation at the actual periodic source or use a mechanism that preserves elapsed ticks. Do not replay arbitrary delayed samples as if they measured past input levels.""",
"if (exam_rit_config_ms(10u)==EXAM_OK) exam_rit_start();\n/* Existing RIT_IRQHandler: */\nexam_rit_ack();\nexam_debounce_tick();",
"RIT matches → acknowledge → one bounded debounce tick → return. Other foreground work continues between interrupts.",
"Two features configure RIT to 10 ms and 100 ms respectively. Design one ownership plan.",
["Configuration is shared hardware state, not per-feature state.", "A slower task can count ten 10 ms ticks."],
"Keep one RIT owner at 10 ms. Drive the fast feature every tick and the slower one every tenth tick, if its timing tolerates that policy. Use another timer when timing/resource requirements conflict.",
"Reconfiguring RIT silently resets it. Forgetting ack can trap execution in repeated IRQs.",
"Explain configuration, start, acknowledge, and dependency effects of stop.", "RIT|Polling|Debounce", 8),

lesson("board-joystick", "9. Joystick levels, edges, and repeat policy",
"""The joystick exposes select/down/left/right/up. The API normalizes active-low inputs into pressed bits. A level stays true while held; a pressed edge is true only for a transition from unpressed to pressed.

Store the previous sample. Compute edges from previous/current, process them, then update previous. Reinitializing previous to zero every loop makes a held direction look like a new press. Decide how simultaneous directions are handled and whether repeat while held is allowed by the paper.

Edge detection is not automatically debounce. Mechanical noise may need a stable-sample filter. Keep state changes and display updates explicit so select cannot also edit a digit after changing modes.""",
"uint32_t current = exam_joystick_read();\nuint32_t edges = exam_joystick_pressed_edges(previous,current);\nprevious = current;\nif (edges & EXAM_JOY_LEFT) { /* one left-press action */ }",
"Samples 0,left,left,0,left → edges 0,left,0,0,left. Five samples contain two distinct presses.",
"How would a game that repeats a held direction after a delay differ?",
["Keep level information as well as edges.", "Use a timer/counter for delay and repeat spacing."],
"On the initial edge act once and start a hold timer. While the level stays pressed, act after the specified initial delay and then at the specified repeat interval. On release clear the timer. Do not invent repeat behavior if the paper requires one action per press.",
"Using current instead of edges repeats every sample. Clearing previous too early loses transition information.",
"Trace press, hold, release, and simultaneous inputs against a written policy.", "Joystick|State|Polling", 9),

lesson("board-adc", "10. ADC: start, capture, take a fresh result",
"""The ADC converts an analog voltage into an integer. The maintained API uses channel 5 for the potentiometer and yields a 12-bit result, 0..4095. Start requests one conversion; the value is not instantly ready.

The single ADC_IRQHandler calls exam_adc_irq_capture. Foreground calls exam_adc_take with a valid output pointer and checks whether a fresh value was obtained. Reading an old variable after take returns false is not a fresh measurement.

Scale using a sufficiently wide intermediate and the destination range. Showing the high eight bits produces a quick LED representation; a DAC needs a 10-bit range. Define endpoint mapping and rounding before coding.""",
"exam_adc_start();\n/* Existing ADC_IRQHandler: exam_adc_irq_capture(); */\nuint16_t sample;\nif (exam_adc_take(&sample)) {\n    exam_adc_show_high8(sample);\n}",
"Start → conversion progresses → IRQ captures DONE result → take returns true once → a second take without a new conversion returns false.",
"Map 0..4095 into 0..1023 with endpoints preserved. Calculate results at 0 and 4095.",
["Multiply before dividing using uint32_t.", "Check both endpoints and an interior point."],
"dac=((uint32_t)sample*1023u)/4095u gives 0 and 1023 at the endpoints. Interior values are truncated in this policy. A >>2 mapping is a different simple quantization policy; choose according to the requirement.",
"Calling start continuously can disrupt the intended one-conversion flow. Ignoring take's Boolean reads stale/uninitialized values.",
"Explain why a successful start is not a completed sample.", "ADC|Conversion|Scaling", 10),

lesson("board-dac", "11. DAC: samples, tables, and speaker timing",
"""The DAC converts a numeric sample into an analog output on P0.26. The current API accepts integers 0..1023. A waveform table is a sequence of samples; a periodic source selects the next entry. Table length and sample rate jointly determine the repeated waveform frequency: frequency=sample_rate/table_length.

Keep every sample in range and wrap the index only after the last valid entry. A centered waveform uses a midpoint such as 512; silencing the supplied output workflow uses an explicit zero write. Stopping the timer alone can leave the last sample at the DAC.

Playback timing matters. If every sample must be emitted, do not transfer sample ticks through a coalescing event bit and assume none were lost. A bounded single-sample update in the periodic IRQ is often the appropriate timing path.""",
"static const uint16_t wave[4] = {512u,768u,512u,256u};\n/* One bounded step at each playback tick: */\n(void)exam_dac_write(wave[index]);\nindex = (index + 1u) % 4u;",
"At 4000 samples/s, this four-sample table repeats at 1000 Hz. Indexes cycle 0,1,2,3,0.",
"Double the table length without changing sample rate. What happens to waveform frequency? How do you stop cleanly?",
["One cycle now requires twice as many ticks.", "Output level and time-source state are separate."],
"The frequency halves. Stop the playback timer and write exam_dac_write(0). Reset index if the restart contract requires beginning at sample zero.",
"Writing 4095 to a 10-bit DAC fails validation. A missed sample changes timing even if all values are mathematically correct.",
"Derive sample rate, table length, frequency, and stop behavior.", "DAC|Speaker|Timer", 11),

lesson("board-events", "12. Atomic handoff and simultaneous events",
"""Choose a representation matching the information you need. A Boolean/bit records presence. A counter preserves multiplicity but not individual payloads. A queue preserves ordered payloads at a capacity cost. There is no universally correct replacement among them.

exam_events_take(mask) atomically takes only requested event bits. Process independent bits using independent if statements. For shared multi-step state, enter a brief critical section and restore the exact returned interrupt mask with exam_critical_exit.

Define simultaneous-event priority in the state machine: for example reset before increment, or first finish a pending calculation. 'Whatever branch happens to come first' is not a specification.""",
"uint32_t saved = exam_critical_enter();\n/* copy/clear a small shared counter here */\nexam_critical_exit(saved);\nuint32_t e = exam_events_take(3u);\nif (e & 1u) { /* event A */ }\nif (e & 2u) { /* event B */ }",
"A and B both pending → take(3) returns 3 and clears them → both independent actions can run under the chosen priority.",
"Why must exit restore saved rather than blindly enable interrupts?",
["The caller may already have disabled interrupts.", "A helper must preserve its caller's state."],
"Blindly enabling interrupts breaks an outer critical section. Restoring saved PRIMASK preserves the prior state, including already-disabled interrupts. Keep the protected work short and nonblocking.",
"else-if loses independent events. Volatile counters can still lose updates without protection.",
"Choose flag/counter/queue and specify simultaneous-event order.", "Events|Atomic|IRQ", 12),

lesson("board-combine", "13. Combine peripherals without competing owners",
"""Integration connects known-good pieces through explicit interfaces. List each hardware resource, its clock/period, handler, producer data, and consumer. Two unrelated modules cannot independently own Timer0 or RIT configuration.

Bring devices up separately, then connect one event path at a time. C owns board behavior; a pure assembly function consumes values and returns computation unless the question explicitly requires something else. Document values that persist across rounds and values reset per round.

Timing dependencies matter: stopping the playback timer should not stop a different tick still needed for debounce. Initialization order should establish shared state before enabling interrupt producers. Keep the final start operation visibly last for Timer and RIT.""",
"/* Example ownership map: */\n/* RIT 10 ms: debounce and joystick sampling */\n/* Timer0: one bounded DAC sample per match */\n/* ADC IRQ: capture only */\n/* main: scale fresh ADC result and update game state */",
"LED alone passes → input events pass → algorithm passes with fixed inputs → replace fixed input with captured input → add periodic output.",
"Which resource stops when playback is paused? Which must remain alive for a button to resume it?",
["Playback and input sampling have different lifetimes.", "Resume cannot depend on a tick you stopped."],
"Stop the playback timer only. Leave the input/debounce time source active so a confirmed resume event remains possible. Restart with an explicitly chosen index/state policy.",
"Stopping a shared timer can make resume impossible. Reinitializing the whole API during a round erases shared state.",
"Produce an ownership table with no competing timer or vector owners.", "Timer|ADC|DAC|Buttons|Integration", 13),

lesson("board-power", "14. Waiting, power, and pending-work races",
"""Waiting is not the same as delaying. __WFI asks the processor to wait for an interrupt, while a busy loop keeps executing. It can reduce idle work but does not guarantee that your software event queue is empty or that a future interrupt will arrive.

An event can occur after foreground checks 'empty' but before WFI. If the handler publishes an event and returns before WFI executes, foreground may sleep with work pending until another interrupt. Choose a documented atomic wait scheme or keep bounded polling where appropriate; do not add sleep casually to a one-shot event loop.

The supplied power-control lecture covers sleep modes beyond the basic wait instruction. Treat deeper power transitions as supporting material requiring clock/wakeup review. They can affect the peripherals the exam expects to continue running.""",
"for (;;) {\n    uint32_t e = exam_events_take(1u);\n    if (e & 1u) { /* bounded work */ }\n    /* No sleep in this deliberately simple polling illustration. */\n}",
"Empty take → IRQ publishes event → next polling iteration sees it. Adding WFI between those steps needs a separate race analysis.",
"A one-shot timer has already fired and no other interrupts remain. Explain why careless WFI can appear to freeze pending work.",
["There may be no later interrupt to wake the CPU.", "The software bit can be set even though the hardware IRQ is already handled."],
"If the event arrived just before WFI, the CPU can wait while a software event remains pending. Keep polling for the basic implementation or use a validated atomic sleep protocol that preserves prior interrupt state.",
"A delay loop is not a hardware timer. Deep sleep can stop clocks required for ongoing sampling.",
"Explain a check-then-sleep race with an event timeline.", "Power|Core|Events", 1, "Supporting knowledge"),

lesson("board-interface", "15. API, professor functions, or direct registers",
"""The most convenient interface is not always the required one. Read the paper first: a named professor function or required handler must keep its specified interface. A direct-register question may be testing power control, pin selection, prescalers, or interrupt flags that a helper hides.

When the Combined API is allowed, use its current header and examples. When direct access is required, consult the actual register manual and original lab example. Do not configure the same peripheral through both paths: a later helper may reset fields you set directly.

Keep migrations explicit. Historical callback names and answer-file layouts are not declarations in the current project. Reference code teaches a technique; the current build defines what can be called.""",
"/* Decision order: */\n/* 1. Required by paper? Keep the exact interface. */\n/* 2. Combined API allowed and capability supported? Use it. */\n/* 3. Otherwise consult original driver/register source. */",
"Question names an MR1 action → current helper covers MR0 configuration → preserve required MR1 setup/handling explicitly rather than pretending an MR0-only recipe satisfies it.",
"The question asks to configure a timer prescaler, but a helper forces PR=0. What should you do?",
["The requested register behavior is part of the task.", "Avoid reconfiguring through a helper afterwards."],
"Use the required professor/register path and derive the requested prescaler/match values. Keep one owner and inspect the manual. Do not call a helper that overwrites PR after your setup.",
"A convenient helper can erase required settings. Historical API names may compile nowhere in the current project.",
"State why your chosen interface satisfies the exact question.", "API|Registers|Professor interface", 14),

lesson("board-lcd", "16. LCD and touch panel extension",
"""The supplied LCD/touch lecture separates display output from touch input. The ILI9325 display controller and ADS7843 touch controller are distinct devices. A pixel coordinate is not a raw touch measurement; touch coordinates need calibration, axis/orientation handling, and bounds checking.

Begin with the original lecture and matching driver, not invented exam_api functions: the maintained API has no LCD/touch wrappers. Bring up a fixed rectangle first, then a text/coordinate display, then calibrated input. The display's 240-by-320 coordinate range must be interpreted in the configured orientation.

For an on-screen button, define a rectangle and a press/release state machine. Clamp or reject out-of-range readings before indexing a framebuffer or interpreting a hit. This is an extension, not a prerequisite for reviewed LED-only exam questions.""",
"/* Pure coordinate test; not a display driver. */\nstatic int inside(int x,int y) {\n    return x>=20 && x<80 && y>=30 && y<60;\n}",
"Point (20,30) is inside; (79,59) is inside; (80,59) is outside. Half-open rectangles avoid counting shared edges twice.",
"A calibration maps raw X values 200..3800 to display X 0..239. Compute the endpoint mapping using a wide intermediate and state an out-of-range policy.",
["Subtract the calibration minimum before scaling.", "Reject or clamp before unsigned subtraction."],
"Clamp raw to [200,3800], then x=((uint32_t)(raw-200)*239u)/3600u. Endpoints map to 0 and 239. Validate calibration span is nonzero. Y and orientation need their own measured mapping.",
"Raw ADC-like touch values are not pixels. A missing driver cannot be fixed by inventing API names.",
"Explain display versus touch responsibilities and test rectangle boundaries.", "LCD|Touch|Coordinates", None, "Extension"),
]
