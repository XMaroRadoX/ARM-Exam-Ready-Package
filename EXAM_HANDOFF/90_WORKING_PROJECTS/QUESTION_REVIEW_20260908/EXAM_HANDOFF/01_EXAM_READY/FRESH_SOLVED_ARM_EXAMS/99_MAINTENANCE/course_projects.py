"""Complete small project sources; generator copies the protected template first."""
from course_c import lesson
INCLUDES = '#include "exam_api.h"\n'
FAIL = 'static void stop_on_error(void) { exam_led_write(0xFFu); for (;;) {} }\n'
BUTTON_MAIN = INCLUDES+FAIL+"""
int main(void)
{
    uint8_t count=0u;
    exam_init();
    exam_buttons_init();
    if (exam_debounce_config(10u,50u)!=EXAM_OK) stop_on_error();
    if (exam_rit_config_ms(10u)!=EXAM_OK) stop_on_error();
    exam_rit_start();
    for (;;) {
        uint32_t pressed=exam_button_events_take();
        if (pressed & EXAM_BUTTON_EVENT_INT0) {
            count=(uint8_t)(count+1u);
            exam_led_write(count);
        }
    }
}
"""
BUTTON_IRQ = INCLUDES+"""
void EINT0_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_INT0); }
void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1); }
void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2); }
"""
RIT_IRQ = INCLUDES+"""
void RIT_IRQHandler(void) { exam_rit_ack(); exam_debounce_tick(); }
"""
TIMER_IRQ = INCLUDES+"""
void TIMER0_IRQHandler(void) {
    uint32_t flags=exam_timer_ack(EXAM_TIMER0);
    if (flags & 1u) exam_events_set(1u);
}
void TIMER1_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER1); }
void TIMER2_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER2); }
void TIMER3_IRQHandler(void) { (void)exam_timer_ack(EXAM_TIMER3); }
"""
TIMED_MAIN = INCLUDES+FAIL+"""
extern uint32_t sum_words(const uint32_t *values,uint32_t count);
static const uint32_t values[4]={1u,2u,3u,4u};
int main(void)
{
    exam_init();
    if (exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC)!=EXAM_OK)
        stop_on_error();
    exam_timer_start(EXAM_TIMER0);
    for (;;) {
        if (exam_events_take(1u) & 1u) {
            uint32_t result=sum_words(values,4u);
            exam_led_write((uint8_t)result);
        }
    }
}
"""
SUM_ASM = """        AREA |.text.course_sum|, CODE, READONLY
        THUMB
        PRESERVE8
        EXPORT sum_words
sum_words PROC
        MOV R2, #0
        MOV R3, #0
next    CMP R2, R1
        BHS done
        LDR R12, [R0, R2, LSL #2]
        ADD R3, R3, R12
        ADD R2, R2, #1
        B next
done    MOV R0, R3
        BX LR
        ENDP
        END
"""
ANALOG_MAIN = INCLUDES+FAIL+"""
int main(void)
{
    uint8_t in_flight=0u;
    exam_init();
    exam_adc_init();
    exam_dac_init();
    if (exam_timer_config_ms(EXAM_TIMER0,50u,EXAM_TIMER_PERIODIC)!=EXAM_OK)
        stop_on_error();
    exam_timer_start(EXAM_TIMER0);
    for (;;) {
        uint16_t sample;
        if (exam_adc_take(&sample)) {
            in_flight=0u;
            uint32_t scaled=((uint32_t)sample*1023u)/4095u;
            if (exam_dac_write((int32_t)scaled)!=EXAM_OK) stop_on_error();
            exam_adc_show_high8(sample);
        }
        if ((exam_events_take(1u)&1u) && !in_flight) {
            in_flight=1u;
            exam_adc_start();
        }
    }
}
"""
PROJECTS = {
 "project-buttons":{"Source/sample.c":BUTTON_MAIN,"Source/button_EXINT/IRQ_button.c":BUTTON_IRQ,"Source/RIT/IRQ_RIT.c":RIT_IRQ},
 "project-timed":{"Source/sample.c":TIMED_MAIN,"Source/timer/IRQ_timer.c":TIMER_IRQ,"Source/ASM_funct.s":SUM_ASM},
 "project-analog":{"Source/sample.c":ANALOG_MAIN,"Source/timer/IRQ_timer.c":TIMER_IRQ},
}
CAPSTONES = [
lesson("project-buttons","1. Guided project: debounced button and LED counter",
"""Build a counter that increments once per confirmed INT0 press. This is a teaching project, not a claim that a paper specifies these constants. The state is one uint8_t counter with intentional modulo-256 wrap. LEDs show its binary value.

Milestone 1: copy/build the template and display 0x01. Milestone 2: configure RIT for 10 ms and prove its IRQ executes. Milestone 3: replace INT0's raw acknowledgement with debounce_begin and call debounce_tick from RIT. Milestone 4: consume a confirmed press in foreground and update the display.

Before opening the solution, write an ownership table. The generated complete project changes only the listed answer/IRQ files in a template copy. Its polling foreground deliberately avoids a check-then-sleep race.""",
"/* Required behavior: */\n/* reset ->0; press ->1; hold ->1; release; press ->2 */",
"Initial count0 → first confirmed press count1 → prolonged hold unchanged → release/repress count2.",
"Implement the four milestones before revealing the complete project. Add a KEY1 reset as an extension without counting it as INT0.",
["KEY1 needs its own debounce_begin flow and event bit.", "If reset and increment arrive together, choose and document priority."],
"Use the complete project below for comparison. For reset priority, handle KEY1 first and skip increment in that iteration, or explicitly apply reset then increment if the task requires that order. Do not clear the whole API state to reset one counter.",
"Raw IRQ entries overcount bouncing. Editing sample.c to add a duplicate EINT handler breaks the link.",
"Pass press, hold, release, second press, and wraparound on the board.", "Buttons|LED|Debounce|RIT"),

lesson("project-timed","2. Guided project: timer calls a real ARM computation",
"""Every 500 ms, request a foreground sum of four unsigned words and display the result. The contract returns the sum modulo 2^32 and does not modify input. This small fixed workload treats timer events as a pending request; it does not promise to count every timer tick under arbitrary foreground delay.

Milestone 1: write the C prototype and a temporary stub returning 10. Milestone 2: verify that the real Timer0 handler publishes an event and main displays that value. Milestone 3: replace the stub with the bounded ARM word scan. Milestone 4: inspect R0, input memory, SP, and callee-saved registers.

Change the input vector to distinguish a real computation from a surviving stub. A repeated displayed 10 for every input is evidence to investigate, not success.""",
"/* Known cases: [] ->0; [7] ->7; [1,2,3,4] ->10 */",
"Timer0 match → one event bit → main calls sum_words → R0=10 → LED mask0x0A.",
"Implement sum_words and test [2,4,6] before opening the full source. Why would a queue be needed in a different timing contract?",
["A leaf scan can use only caller-clobbered registers.", "A bit can coalesce multiple delayed ticks."],
"The complete project contains a real loop, not the temporary stub. [2,4,6] returns12. If each tick has a distinct payload or must be counted, replace the notification design with bounded counter/queue semantics rather than assuming event flags count.",
"Link success with a stub proves only connectivity. Wrong stride and unbalanced registers can survive a simple result test.",
"Pass independent ARM cases, then integration, with no temporary stub remaining.", "Timer|Assembly|ABI|LED"),

lesson("project-analog","3. Guided project: timed ADC to DAC workflow",
"""Sample the potentiometer on a 50 ms scheduling request, show its high eight bits on LEDs, and map the fresh 12-bit sample to the 10-bit DAC range. This is an analog-following project, not an audio waveform generator.

Milestone 1: confirm ADC initialization and one conversion/capture/take. Milestone 2: test the integer scaling function with 0 and 4095 without hardware. Milestone 3: initialize DAC and write bounded test levels. Milestone 4: connect Timer0 scheduling to a single in-flight conversion and use only fresh samples.

in_flight prevents starting another conversion while one is pending. Timer requests while busy are deliberately coalesced/dropped; every-sample acquisition would require a different contract. A failure to receive ADC completion is a troubleshooting checkpoint, not a reason to continuously restart it.""",
"/* endpoint mapping */\nuint32_t scaled=((uint32_t)sample*1023u)/4095u;",
"Timer request → start ADC → ADC IRQ captures → main takes sample4095 → DAC1023, LEDs0xFF.",
"Test the output endpoints and explain why writing the raw ADC sample directly to DAC is wrong.",
["Source is 12-bit; destination is 10-bit.", "Take must report a fresh result before processing."],
"Raw ADC can reach4095, but DAC accepts at most1023. Widen before multiplying, divide by4095, and check the write status. Test zero, maximum, and midpoint. Physical output needs board measurement; a software build alone cannot validate it.",
"Starting conversions repeatedly hides a missing ADC handler. Treating the same stale value as fresh violates the flow.",
"Demonstrate one in-flight conversion, fresh consumption, range-safe output, and stable repeated operation.", "ADC|DAC|Timer|LED"),

lesson("practice-exam","4. Independent practice: remove the scaffolding",
"""Choose a reviewed paper whose required peripherals you can already operate. First read only its statement and record the prototype, constraints, interface rules, and submission requirements. Use In the Exam to record your own duration and checklist; no historical duration is imposed.

Attempt both questions before opening the maintained solution. Start with a buildable baseline, then a correct small algorithm case and a basic board action. Save working milestones in your own copy. When stuck, record the symptom and the smallest failing case rather than browsing entire unrelated solutions.

After time ends, preserve your attempt unchanged. Compare the contract, algorithm, ABI, peripheral ownership, and boundary behavior against the reviewed answer. Keep a separate correction copy and an error log. Repeat with a new paper only after you can explain each correction.""",
"/* Personal error log fields: */\n/* requirement | first wrong observation | cause | fix | regression test */",
"Attempt → frozen timed version → compare → one identified cause → correction → rerun distinguishing test.",
"Solve one assembly and one board question without viewing their solutions. Then explain three differences in your correction copy.",
["Use the question's exact types and timing.", "The error log should include causes, not only changed lines."],
"Success means a reproducible attempt and an explained correction, not matching a code listing character for character. Use all reviewed questions in the coverage map to choose the next skill gap. Keep official self-correction format rules separate from a personal practice log.",
"Reading the solution before attempting hides gaps. Editing the only exam-version copy destroys your record of what was submitted.",
"Complete both questions under a self-chosen time limit and explain every remaining failure.", "Exam|Practice|Debug|Assembly|C"),
]
