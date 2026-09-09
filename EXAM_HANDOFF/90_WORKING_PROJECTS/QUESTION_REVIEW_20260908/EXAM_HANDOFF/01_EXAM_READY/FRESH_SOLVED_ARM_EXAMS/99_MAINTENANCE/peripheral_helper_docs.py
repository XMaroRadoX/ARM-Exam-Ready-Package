"""Additive peripheral contracts shared by the API reference and pattern pages."""

TIMER_BEHAVIOUR = [
    ("General timer config_ticks/ms/hz", "TC=PC=0; PR=0; stopped", "Owns MR0, preserves MR1..3 and capture/output setup; clears IR and NVIC pending. Interrupt modes enable NVIC and assign priority equal to timer number."),
    ("General timer start", "Count from current TC/PC", "Retains configuration and pending flags; does not reset."),
    ("General timer stop", "Pause TC/PC", "Retains configuration and pending flags; does not disable NVIC."),
    ("General timer reset", "TC=PC=0; stopped", "Retains configuration; does not acknowledge IR or disable NVIC."),
    ("General timer ack", "No counter change", "Read IR once, clear those hardware flags, return saved bits 0..5. Does not explicitly clear NVIC pending."),
    ("RIT config", "Counter=0; stopped", "Select core clock, clear mask and hardware/controller pending, enable interrupt."),
    ("RIT reset", "Counter=0; retains running state", "Does not acknowledge the interrupt or change the interval."),
    ("SysTick config", "Clear current count; starts immediately", "Set reload and enable core-clock counting and its interrupt."),
]

ADVANCED_EXAMPLE = '''#include "exam_api.h"
volatile uint32_t matches[4];
static void require(exam_status_t s) { if (s != EXAM_OK) for (;;) {} }
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0, 1000u, EXAM_TIMER_PERIODIC));
  require(exam_timer_set_clock_divider(EXAM_TIMER0, 4u));
  require(exam_timer_set_prescaler(EXAM_TIMER0, 24u));
  require(exam_timer_config_match(EXAM_TIMER0, 1u, 250u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 2u, 500u, EXAM_MATCH_INTERRUPT));
  require(exam_timer_config_match(EXAM_TIMER0, 3u, 750u, EXAM_MATCH_INTERRUPT));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
/* Replace TIMER0_IRQHandler in Source/timer/IRQ_timer.c; keep one definition. */
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  uint8_t i;
  for (i = 0u; i < 4u; ++i)
    if (exam_timer_match_happened(flags, i)) ++matches[i];
}'''

RELEASE_EXAMPLE = '''#include "exam_api.h"
volatile uint32_t held, pressed, released;
int main(void) {
  uint32_t previous, current;
  exam_init();
  exam_joystick_init();
  previous = exam_joystick_read();
  for (;;) {
    current = exam_joystick_read();
    pressed = exam_joystick_pressed_edges(previous, current);
    released = exam_joystick_released_edges(previous, current);
    held = current;
    if (pressed & EXAM_JOY_SELECT) exam_led_write(1u);
    if (released & EXAM_JOY_SELECT) exam_led_clear();
    previous = current;
  }
}'''

def extend(api, values, scenarios, constants, gaps, d, p, value):
    from pattern_board_projects import COMMON, CAPTURE
    constants.extend(("EXAM_MATCH_"+name, text) for name, text in (
        ("INTERRUPT", "Bit 0: request an interrupt on the selected match."),
        ("RESET", "Bit 1: reset TC on the selected match."),
        ("STOP", "Bit 2: stop TC on the selected match. Combine with |; zero disables all three actions.")))
    common = "Call exam_init once, then a successful exam_timer_config_ticks/ms/hz for this timer. It must remain powered and stopped, with neither TCR enable nor reset set."
    ret = "EXAM_OK on success; EXAM_BAD_ARGUMENT for an invalid timer/index/action/divider; EXAM_NOT_READY if uninitialized, unpowered, running or held in reset. Invalid calls leave peripheral configuration unchanged."
    info = {
      "exam_timer_config_match": (
        "Configure one match channel without disturbing the others or starting the timer.",
        {"timer":p("in","EXAM_TIMER0..EXAM_TIMER3"), "match":p("in","0..3 selects MR0..MR3"), "ticks":p("in","1..UINT32_MAX counter ticks; zero returns EXAM_OUT_OF_RANGE"), "actions":p("in","0..7: any OR combination of EXAM_MATCH_INTERRUPT, EXAM_MATCH_RESET, EXAM_MATCH_STOP")},
        "Writes only the selected MR and its three MCR bits; acknowledges only its old IR flag. Enables NVIC if INTERRUPT is selected, preserving priority and pending state for other sources. Preserves TC, PC, PR, CCR, EMR and other matches.",
        "Do not assume this helper clears another channel's reset/stop action. A reset on an earlier match can prevent later matches."),
      "exam_timer_set_prescaler": (
        "Set the prescaler of an initialized stopped timer.",
        {"timer":p("in","EXAM_TIMER0..EXAM_TIMER3"), "prescaler":p("in","0..UINT32_MAX; TC advances once per PR+1 peripheral clocks")},
        "Writes PR and clears PC; preserves TC, matches, flags, NVIC and clock selection.",
        "Apply after standard configuration, which always sets PR=0. PR=24 means 25 peripheral clocks per counter tick."),
      "exam_timer_set_clock_divider": (
        "Select the peripheral clock divider of one stopped timer.",
        {"timer":p("in","EXAM_TIMER0..EXAM_TIMER3"), "divider":p("in","1, 2, 4 or 8; all other values rejected")},
        "Changes only this timer's two PCLKSEL bits; preserves counters, match/capture configuration, other clocks and interrupt state.",
        "Changing PCLK after millisecond/hertz configuration changes the resulting period. Recompute or use explicit ticks. Counter frequency is core_clock/divider/(PR+1)."),
    }
    for name, (summary, params, side, mistake) in info.items():
        api[name] = d(summary, params=params, returns=ret + (" Zero ticks: EXAM_OUT_OF_RANGE." if name.endswith("match") else ""), preconditions=common, side_effects=side,
          context="Foreground stopped-timer setup. A short critical section restores the original interrupt mask.", example=ADVANCED_EXAMPLE,
          mistake=mistake, exam_note="Keep exact paper tick values. This example uses teaching values; at a 100 MHz core, PR=24 and divider=4 yield a 1 MHz counter.", related=tuple(n for n in info if n != name))
        values[name] = [value("See parameter ranges", mistake, "Current implementation contract")]
    for kind, limit, offset in (("match",3,0),("capture",1,4)):
        name=f"exam_timer_{kind}_happened"
        api[name]=d(f"Test {kind} status in an already saved interrupt snapshot.",
          params={"flags":p("in","Saved result from one exam_timer_ack(timer) call"),kind:p("in",f"0..{limit}; invalid indexes return zero")},
          returns=f"1 when bit {offset}+index is set; otherwise 0.", preconditions="No hardware setup is needed to test a value.",
          side_effects="None: no register reads, no acknowledgement, no NVIC changes.",context="IRQ or foreground, pure function.",
          example=(ADVANCED_EXAMPLE if kind=="match" else COMMON+CAPTURE),
          mistake="Acknowledging a second time loses the first snapshot. Testing a capture flag does not configure a capture pin or CCR.",
          exam_note="Simultaneous sources may set several bits; use independent tests.",related=("exam_timer_ack",))
        values[name]=[value(f"index 0..{limit}",f"Tests snapshot bit {offset}+index", "LPC1768 timer IR mapping")]
    api["exam_joystick_released_edges"]=d("Find five-bit joystick controls released since the previous sample.",
      params={"previous":p("in","Earlier active-high pressed mask"),"current":p("in","Current active-high pressed mask")},
      returns="previous & ~current & 0x1F; high bits are ignored.",preconditions="None for mask comparison; initialize joystick before raw hardware reads.",
      side_effects="None; no hardware access or hidden state.",context="Pure function; caller chooses sampling and repeat policy.",example=RELEASE_EXAMPLE,
      mistake="The argument order is (previous, current), matching pressed_edges. The retired (current, changed) convention is incompatible.",
      exam_note="Initialize previous from the current read to avoid synthesizing startup edges. Raw edge detection is not debounce.",related=("exam_joystick_pressed_edges","exam_joystick_read"))
    values["exam_joystick_released_edges"]=[value("0x01..0x10; combined masks", "SELECT/DOWN/LEFT/RIGHT/UP; no hidden repeat", "Current joystick bit mapping")]
    from pattern_board_projects import COMMON, CAPTURE
    scenarios.extend([
      dict(id="capture-pin",title="Capture an edge using CAP0.0",basis="Teaching example with explicit pin and capture configuration.",exams=[],functions=("exam_timer_capture_happened",),code=COMMON+CAPTURE),
      dict(id="advanced-timer-matches",title="One timer with four independent match notifications",basis="Teaching example; inspect matches[0..3] after each cycle.",exams=[],functions=tuple(info)+("exam_timer_match_happened",),code=ADVANCED_EXAMPLE),
      dict(id="joystick-release",title="Press lights LD11; hold retains it; release clears it",basis="Teaching example; raw comparisons without debounce or repeat.",exams=[],functions=("exam_joystick_pressed_edges","exam_joystick_released_edges"),code=RELEASE_EXAMPLE),
    ])
    for i, gap in enumerate(gaps):
        gap=gap.replace("exam_joystick_first, exam_joystick_released_edges,", "exam_joystick_first,")
        gap=gap.replace("exam_timer_capture_happened, ", "").replace("exam_timer_match_happened, ", "")
        gaps[i]=gap
    gaps.append("Restored capabilities: individual matches, prescaler and divider controls under the new config_match/set_prescaler/set_clock_divider contracts; pure match/capture predicates; joystick released_edges(previous,current). Callback schedulers remain absent. ADC/DAC existing low-level flow already covers reading/writing; percentage scaling belongs in examples.")
