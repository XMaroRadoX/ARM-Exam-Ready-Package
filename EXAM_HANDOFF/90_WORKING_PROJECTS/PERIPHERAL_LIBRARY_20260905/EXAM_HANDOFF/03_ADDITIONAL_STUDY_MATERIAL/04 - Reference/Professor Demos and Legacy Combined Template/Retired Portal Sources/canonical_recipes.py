"""Canonical, student-facing peripheral recipes for the offline workstation."""

from __future__ import annotations


RECIPE_META = [
    (1, "led-masks-bars-counters-patterns", "LED masks, bars, counters, and patterns", ["LED"], "Main writes one coherent LED mask.", "initialize -> compute bounded mask -> write LEDs", "Extra practice", []),
    (2, "button-debounce-rit", "Button debounce using RIT", ["Buttons", "RIT"], "The Exam API owns button IRQs and the RIT debounce scheduler.", "button IRQ -> RIT confirms state -> callback -> event -> main", "Appeared in past exams", ["2023-02-07-Q2", "2023-09-18-Q2", "2024-09-16-Q2"]),
    (3, "button-debounce-systick", "Button debounce using SysTick", ["Buttons", "SysTick"], "Student code samples buttons from one SysTick timebase; do not also start API button debounce.", "SysTick timestamp -> sample -> stable-state update -> main", "Possible variation", []),
    (4, "button-press-release-hold-repeat", "Button press, release, hold, and repeat", ["Buttons", "SysTick"], "Main polls a timestamped state machine; callbacks remain unused.", "sample -> edge -> hold deadline -> repeat deadline -> event", "Possible variation", []),
    (5, "multi-button-chords-priority", "Multi-button chords and input priority", ["Buttons"], "Main takes one snapshot and applies an explicit priority table.", "button snapshot -> chord test -> priority decision -> LED result", "Possible variation", []),
    (6, "joystick-pressed-released-edges", "Joystick pressed and released edges", ["Joystick"], "The Exam API owns joystick sampling and supplies changed bits.", "joystick sample -> changed mask -> pressed/released masks -> events", "Appeared in past exams", ["2025-01-29_ARM1-Q2", "2025-01-29_ARM2-Q2", "2025-01-29_ARM3-Q2"]),
    (7, "joystick-sequence-recognition", "Joystick sequence recognition", ["Joystick"], "The callback records one pressed direction; main advances the sequence.", "edge -> queued direction -> bounded sequence state -> success", "Possible variation", []),
    (8, "unified-input-dispatcher", "Unified button-and-joystick event dispatcher", ["Buttons", "Joystick", "Events"], "Callbacks publish bits only; main owns all visible work.", "button/joystick callback -> event bits -> main dispatch table", "Possible variation", []),
    (9, "timer-modes", "Periodic, free-running, and one-shot timer modes", ["Timer"], "Timer3 is API-owned for callbacks; Timer0 is student-owned and demonstrated through the native board layer.", "configure mode -> clear/reset -> start -> callback or timestamp", "Appeared in past exams", ["2023-07-04-Q2", "2024-02-28-Q2"]),
    (10, "retriggerable-one-shot", "Retriggerable one-shot timeout", ["Buttons", "Timer", "Events"], "A periodic Timer3 callback maintains the deadline; a button event safely retriggers it.", "button -> set remaining ticks -> timer ticks down -> expiry event", "Possible variation", []),
    (11, "stopwatch-lap", "Stopwatch and lap timing", ["Buttons", "SysTick"], "SysTick is the only timebase; unsigned timestamp subtraction handles wraparound.", "press start -> timestamps advance -> lap snapshot -> display", "Possible variation", []),
    (12, "periodic-task-scheduler", "Periodic task scheduler using one hardware timer", ["Timer", "Events"], "Timer3 publishes a base tick; main runs all tasks.", "Timer3 tick -> event -> software dividers -> tasks", "Possible variation", []),
    (13, "multiple-software-timers", "Multiple software timers on one tick source", ["Timer", "Events"], "One Timer3 callback decrements bounded counters and publishes expirations.", "base tick -> decrement timers -> expiry bits -> main", "Possible variation", []),
    (14, "capture-period-frequency", "Timer capture for period and frequency", ["Timer", "Capture"], "Timer0 is student-owned; the native board capture layer owns CAP0 and its callback.", "rising edge -> capture register -> wrap-safe delta -> frequency", "Appeared in past exams", ["2023-02-07-Q2", "2026-02-18_ARM1-Q2"]),
    (15, "capture-pulse-duty", "Timer capture for pulse width and duty cycle", ["Timer", "Capture"], "Timer0 native capture records alternating edges; main computes high/period ratios.", "rising/falling captures -> deltas -> duty calculation", "Possible variation", []),
    (16, "coordinated-multi-timer-state-machine", "Coordinated multi-timer state machine", ["Timer", "Events"], "Timer callbacks publish independent events; main alone changes the state machine.", "timer events -> main transition -> outputs -> next deadline", "Appeared in past exams", ["2024-07-09-Q2", "2025-02-12_ARM1-Q2"]),
    (17, "adc-capture-led-display", "ADC capture and LED display", ["ADC", "LED"], "Main starts the potentiometer and displays only successful samples.", "ADC conversion -> bounded percent -> LED bar", "Appeared in past exams", ["2026-02-03_ARM1-Q2", "2026-02-03_ARM2-Q2"]),
    (18, "adc-threshold-hysteresis", "ADC threshold with hysteresis", ["ADC", "LED"], "Main owns the state; separate high and low thresholds stop chatter.", "ADC sample -> hysteresis -> LED state", "Possible variation", []),
    (19, "adc-moving-average-median", "ADC moving average and median filtering", ["ADC"], "Main owns fixed-size filter storage; no allocation or blocking IRQ work.", "sample -> ring update -> average/median -> result", "Possible variation", []),
    (20, "adc-periodic-ring-buffer", "Periodic ADC sampling into a ring buffer", ["ADC", "Timer", "Events"], "Timer3 requests work; main performs ADC reads and owns the buffer.", "timer event -> ADC read -> ring push -> consumer", "Possible variation", []),
    (21, "dac-table-timer", "DAC table playback using a timer", ["DAC", "Timer"], "exam_dac_play owns the selected API timer until the finite table finishes.", "table -> timer cadence -> DAC samples -> silence", "Appeared in past exams", ["2024-07-09-Q2", "2025-02-12_ARM1-Q2"]),
    (22, "waveform-lookup-tables", "Square, triangle, sawtooth, and sine lookup tables", ["DAC"], "Main constructs bounded 10-bit tables; playback remains a separate choice.", "waveform rule -> 10-bit samples -> table", "Possible variation", []),
    (23, "dac-once-loop-pause-stop", "DAC playback once, loop, pause, and stop", ["DAC", "Timer", "Events"], "Finite API playback is restarted by main for looping; stop is explicit.", "play -> completion deadline -> restart/pause/stop", "Possible variation", []),
    (24, "adc-dac-passthrough", "ADC-to-DAC passthrough and quantization", ["ADC", "DAC"], "Main reads ADC then writes the scaled 10-bit DAC value.", "12-bit ADC -> quantize/scale -> 10-bit DAC", "Possible variation", []),
    (25, "irq-main-event-flags", "IRQ-to-main event flags", ["Events", "Buttons"], "Callbacks set event bits; main atomically takes them exactly once.", "IRQ callback -> set bits -> main take -> slow work", "Appeared in past exams", ["2023-09-18-Q2", "2024-09-16-Q2"]),
    (26, "critical-shared-state", "Correct critical sections around shared state", ["Events"], "Only the smallest multiword snapshot is protected.", "disable briefly -> copy/update shared words -> restore state", "Appeared in past exams", ["2025-07-01_ARM1-Q2"]),
    (27, "rit-deferred-input", "RIT-deferred input processing", ["Buttons", "RIT", "Events"], "The Exam API's RIT scheduler confirms button state; main handles the event.", "edge -> RIT confirmation -> callback -> main", "Appeared in past exams", ["2025-07-01_ARM1-Q2", "2026-06-25_ARM1-Q2"]),
    (28, "systick-timebase", "SysTick timebase without blocking delays", ["SysTick", "Events"], "SysTick provides timestamps; main compares elapsed unsigned ticks.", "timestamp -> elapsed comparison -> periodic action", "Possible variation", []),
    (29, "button-triggered-capture", "Button-triggered timer capture", ["Buttons", "Timer", "Capture"], "Button events arm a student-owned Timer0 capture window.", "button -> arm capture -> edge timestamp -> main result", "Appeared in past exams", ["2026-02-18_ARM1-Q2", "2026-02-18_ARM2-Q2"]),
    (30, "button-adc-assembly", "Button-controlled ADC processing in assembly", ["Buttons", "ADC", "Assembly"], "C owns hardware and passes a plain sample to an ABI-safe assembly function.", "button -> ADC read -> C call -> assembly transform -> LEDs", "Appeared in past exams", ["2026-02-03_ARM1-Q2", "2026-02-03_ARM2-Q2"]),
    (31, "three-timer-audio", "Three-timer DAC and audio sequencing", ["Timer", "DAC", "Events"], "Student-owned Timer2 supplies samples; Timer0 and Timer1 publish duration and envelope events.", "Timer2 sample -> DAC; Timer0 duration and Timer1 envelope -> events -> main", "Appeared in past exams", ["2024-07-09-Q2", "2025-02-12_ARM2-Q2"]),
    (32, "c-assembly-many-arguments", "C and assembly calls with more than four arguments, arrays, and shared structures", ["Assembly"], "C owns storage; assembly follows AAPCS and reads argument five from the caller stack.", "C prototype -> R0-R3 plus stack -> assembly -> result", "Appeared in past exams", ["2025-01-29_ARM1-Q1", "2026-06-25_ARM2-Q1"]),
]


def _format_c_source(source: str) -> str:
    """Expand the compact recipe definitions into readable, indented C."""
    lines: list[str] = []
    current = ""
    indent = 0
    paren_depth = 0
    index = 0
    state = "code"

    def append(value: str) -> None:
        nonlocal current
        if not current:
            current = "    " * indent
        current += value

    def space() -> None:
        if current and not current.endswith((" ", "\t")):
            append(" ")

    def emit() -> None:
        nonlocal current
        text = current.rstrip()
        if text:
            lines.append(text)
        current = ""

    def split_control_statement(line: str) -> list[str]:
        """Put a compact unbraced control body on its own indented line."""
        leading = line[: len(line) - len(line.lstrip())]
        text = line.strip()
        prefix = ""
        control = text
        if control.startswith("} else "):
            prefix = "} else "
            control = control[len(prefix):]
        elif control.startswith("else "):
            prefix = "else "
            control = control[len(prefix):]

        keyword = next((word for word in ("if", "for", "while") if control.startswith(word + " ")), None)
        if keyword is None:
            return [line]
        opening = control.find("(", len(keyword))
        if opening < 0:
            return [line]
        depth = 0
        closing = -1
        for offset in range(opening, len(control)):
            if control[offset] == "(":
                depth += 1
            elif control[offset] == ")":
                depth -= 1
                if depth == 0:
                    closing = offset
                    break
        if closing < 0:
            return [line]
        body = control[closing + 1:].strip()
        if not body or body.startswith("{") or not body.endswith(";"):
            return [line]
        header = leading + prefix + control[: closing + 1]
        body_lines = split_control_statement(leading + "    " + body)
        return [header, *body_lines]

    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""

        if state == "string":
            append(char)
            if char == "\\" and following:
                append(following)
                index += 2
                continue
            if char == '"':
                state = "code"
            index += 1
            continue

        if state == "character":
            append(char)
            if char == "\\" and following:
                append(following)
                index += 2
                continue
            if char == "'":
                state = "code"
            index += 1
            continue

        if state == "block-comment":
            append(char)
            if char == "*" and following == "/":
                append("/")
                index += 2
                state = "code"
                continue
            index += 1
            continue

        if char == "/" and following == "*":
            space()
            append("/*")
            state = "block-comment"
            index += 2
            continue
        if char == '"':
            append(char)
            state = "string"
        elif char == "'":
            append(char)
            state = "character"
        elif char.isspace():
            space()
        elif char == "(":
            if current.rstrip().endswith(("if", "for", "while", "switch")):
                space()
            append(char)
            paren_depth += 1
        elif char == ")":
            append(char)
            paren_depth = max(0, paren_depth - 1)
        elif char == ",":
            append(char)
            space()
        elif char == ";":
            append(char)
            if paren_depth == 0:
                emit()
        elif char == "{":
            space()
            append("{")
            emit()
            indent += 1
        elif char == "}":
            emit()
            indent = max(0, indent - 1)
            append("}")
        else:
            if current.lstrip().startswith("}") and char.isalpha():
                if source.startswith("else", index) or source.startswith("while", index):
                    space()
                else:
                    emit()
            append(char)
        index += 1

    emit()
    expanded: list[str] = []
    for line in lines:
        if expanded and expanded[-1] == "}" and line and not line[0].isspace():
            expanded.append("")
        expanded.extend(split_control_statement(line))
    return "\n".join(expanded) + "\n"


def _program(number: int) -> str:
    """Return a complete, consistently formatted Answer/main.c recipe."""
    common = '#include "exam_api.h"\n#include <stdint.h>\n#include <stddef.h>\n\n'
    programs = {
        1: '''int main(void){uint8_t n=0u,index;exam_init();if((exam_self_test()&1u)==0u)return 1;exam_leds_clear();if(exam_led_from_board_label(4u,&index)==EXAM_OK)exam_led_on(index);for(;;){uint8_t previous=exam_leds_read();exam_leds_write((uint8_t)(previous^(uint8_t)(++n)));for(volatile uint32_t i=0;i<120000u;++i){} }}''',
        2: '''enum{EV_PRESS=1u};static void button_cb(exam_button_t b,exam_button_event_t e){if(b==EXAM_BUTTON_INT0&&e==EXAM_PRESS)exam_events_set(EV_PRESS);}int main(void){exam_init();exam_buttons_confirmation_ms(30u);if(exam_buttons_start(button_cb)!=EXAM_OK)return 1;if(exam_button_irq_start(EXAM_BUTTON_INT0)!=EXAM_OK)return 2;for(;;){if(exam_events_take(EV_PRESS))exam_led_toggle(0u);exam_idle();}}''',
        3: '''typedef struct{uint8_t stable,candidate,count;}Debounce;static uint8_t update(Debounce*s,uint8_t x){if(x!=s->candidate){s->candidate=x;s->count=1u;}else if(s->count<20u)++s->count;if(s->count==20u&&s->stable!=x){s->stable=x;return 1u;}return 0u;}int main(void){Debounce d={0};uint32_t last;exam_init();if(exam_systick_periodic_ms(1u)!=EXAM_OK)return 1;last=exam_systick_ticks();for(;;){uint32_t now=exam_systick_ticks();if(now!=last){last=now;if(update(&d,exam_button_is_down(EXAM_BUTTON_INT0)))exam_led_set(0u,d.stable!=0u);}}}''',
        4: '''int main(void){uint8_t old=0u;uint32_t down_at=0u,next_repeat=0u;exam_init();exam_systick_periodic_ms(1u);for(;;){uint8_t now=exam_button_is_down(EXAM_BUTTON_INT0);uint32_t t=exam_systick_ticks();if(now&&!old){down_at=t;next_repeat=t+500u;exam_led_toggle(0u);}if(now&&(int32_t)(t-next_repeat)>=0){exam_led_toggle(1u);next_repeat+=150u;}if(!now&&old){uint32_t held=t-down_at;exam_leds_bar(held>2000u?2000u:held,2000u);}old=now;}}''',
        5: '''int main(void){uint32_t previous=0u;exam_init();for(;;){uint32_t b=exam_buttons_down(),changed=b^previous;uint32_t pressed=exam_button_pressed_edges(b,changed),released=exam_button_released_edges(b,changed);uint8_t out=0u;if((b&3u)==3u)out=0x80u;else if(pressed&1u)out=0x01u;else if(pressed&2u)out=0x02u;else if(released)out=0x40u;exam_leds_write(out);previous=b;}}''',
        6: '''enum{EV_PRESS=1u,EV_RELEASE=2u};static void joy_cb(uint32_t now,uint32_t changed){if(exam_joystick_pressed_edges(now,changed))exam_events_set(EV_PRESS);if(exam_joystick_released_edges(now,changed))exam_events_set(EV_RELEASE);}int main(void){exam_init();if(exam_joystick_start(joy_cb)!=EXAM_OK)return 1;for(;;){uint32_t e=exam_events_take(EV_PRESS|EV_RELEASE);if(e&EV_PRESS){exam_leds_write((uint8_t)exam_joystick_down());exam_leds_bar(exam_joystick_first(),EXAM_JOY_UP);}if(e&EV_RELEASE){exam_leds_clear();exam_joystick_reset_first();}exam_idle();}}''',
        7: '''static const uint32_t wanted[]={EXAM_JOY_UP,EXAM_JOY_RIGHT,EXAM_JOY_DOWN,EXAM_JOY_LEFT};static volatile uint32_t pending;static void joy_cb(uint32_t now,uint32_t changed){uint32_t p=exam_joystick_pressed_edges(now,changed);if(p)pending=p&(~p+1u);}int main(void){size_t step=0u;exam_init();exam_joystick_start(joy_cb);for(;;){uint32_t p,s=exam_critical_enter();p=pending;pending=0u;exam_critical_exit(s);if(p){step=(p==wanted[step])?step+1u:0u;if(step==4u){exam_leds_fill();step=0u;}}exam_idle();}}''',
        8: '''enum{EV_BUTTON=1u,EV_JOY=2u};static void bcb(exam_button_t b,exam_button_event_t e){(void)b;if(e==EXAM_PRESS)exam_events_set(EV_BUTTON);}static void jcb(uint32_t n,uint32_t c){if(exam_joystick_pressed_edges(n,c))exam_events_set(EV_JOY);}int main(void){exam_init();exam_buttons_start(bcb);exam_button_irq_start(EXAM_BUTTON_INT0);exam_joystick_start(jcb);for(;;){uint32_t e=exam_events_take(EV_BUTTON|EV_JOY);if(e&EV_BUTTON)exam_led_toggle(0u);if(e&EV_JOY)exam_led_toggle(1u);exam_idle();}}''',
        9: '''static volatile uint32_t ticks;static void tick(exam_timer_t t,uint32_t f){(void)t;if(exam_timer_match_happened(f,0u))++ticks;}int main(void){exam_init();if(exam_timer_periodic_hz(EXAM_TIMER_3,10u,tick)!=EXAM_OK)return 1;for(;;)exam_leds_write((uint8_t)ticks);}''',
        10: '''static volatile uint32_t remaining;static void tick(exam_timer_t t,uint32_t f){(void)t;if(exam_timer_match_happened(f,0u)&&remaining&&--remaining==0u)exam_events_set(1u);}static void button(exam_button_t b,exam_button_event_t e){(void)b;if(e==EXAM_PRESS)remaining=20u;}int main(void){exam_init();exam_timer_periodic_ms(EXAM_TIMER_3,10u,tick);exam_buttons_start(button);exam_button_irq_start(EXAM_BUTTON_INT0);for(;;){if(exam_events_take(1u))exam_led_off(0u);else if(remaining)exam_led_on(0u);exam_idle();}}''',
        11: '''int main(void){uint32_t start=0u,lap=0u;uint8_t running=0u,old=0u;exam_init();if(exam_timer_free_running_start(EXAM_TIMER_3,4u,24999u)!=EXAM_OK)return 1;for(;;){uint8_t b=exam_button_is_down(EXAM_BUTTON_INT0);if(b&&!old){uint32_t now=exam_timer_read(EXAM_TIMER_3);if(!running){start=now;running=1u;}else{lap=now-start;exam_leds_bar(lap%10000u,9999u);}}old=b;}}''',
        12: '''static void tick(exam_timer_t t,uint32_t f){(void)t;if(exam_timer_match_happened(f,0u))exam_events_set(1u);}int main(void){uint32_t n=0u;exam_init();exam_timer_periodic_ms(EXAM_TIMER_3,10u,tick);for(;;){if(exam_events_take(1u)){++n;if(n%10u==0u)exam_led_toggle(0u);if(n%50u==0u)exam_led_toggle(1u);}exam_idle();}}''',
        13: '''typedef struct{uint16_t left,reload;uint32_t event;}SoftTimer;static SoftTimer a[]={ {10u,10u,1u},{25u,25u,2u},{100u,100u,4u} };static void tick(exam_timer_t t,uint32_t f){size_t i;(void)t;if(!exam_timer_match_happened(f,0u))return;for(i=0u;i<3u;++i)if(--a[i].left==0u){a[i].left=a[i].reload;exam_events_set(a[i].event);}}int main(void){exam_init();exam_timer_periodic_ms(EXAM_TIMER_3,10u,tick);for(;;){uint32_t e=exam_events_take(7u);if(e&1u)exam_led_toggle(0u);if(e&2u)exam_led_toggle(1u);if(e&4u)exam_led_toggle(2u);exam_idle();}}''',
        14: '''static volatile uint32_t previous,period;static void captured(uint8_t timer,uint32_t flags){uint32_t now;if(exam_timer_capture_happened(flags,0u)&&timer_read_capture(timer,0u,&now)==BOARD_OK){period=now-previous;previous=now;}}int main(void){exam_init();timer_set_callback(0u,captured);timer_set_prescaler(0u,0u);timer_configure_capture(0u,0u,CAPTURE_RISING,1u);timer_start(0u);for(;;){uint32_t p,s=exam_critical_enter();p=period;exam_critical_exit(s);if(p)exam_leds_bar(timer_counter_clock_hz(0u)/p,10000u);}}''',
        15: '''static volatile uint32_t last_rise,high_ticks,period_ticks;static volatile uint8_t was_high;static void edge(uint8_t t,uint32_t f){uint32_t x;if(timer_capture_occurred(f,0u)&&timer_read_capture(t,0u,&x)==BOARD_OK){if(was_high){high_ticks=x-last_rise;was_high=0u;}else{period_ticks=x-last_rise;last_rise=x;was_high=1u;}}}int main(void){exam_init();timer_set_callback(0u,edge);timer_configure_capture(0u,0u,CAPTURE_BOTH,1u);timer_start(0u);for(;;){uint32_t h=high_ticks,p=period_ticks;if(p)exam_leds_bar(h, p);}}''',
        16: '''enum{EV_FAST=1u,EV_SLOW=2u};static uint8_t div10;static void tick(exam_timer_t t,uint32_t f){(void)t;if(exam_timer_match_happened(f,0u)){exam_events_set(EV_FAST);if(++div10==10u){div10=0u;exam_events_set(EV_SLOW);}}}int main(void){uint8_t state=0u;exam_init();exam_timer_periodic_ms(EXAM_TIMER_3,100u,tick);for(;;){uint32_t e=exam_events_take(3u);if(e&EV_FAST)exam_led_toggle(state);if(e&EV_SLOW)state=(uint8_t)((state+1u)%8u);exam_idle();}}''',
        17: '''int main(void){uint8_t percent;exam_init();if(exam_potentiometer_start()!=EXAM_OK)return 1;for(;;)if(exam_potentiometer_read_percent(&percent)==EXAM_OK)exam_leds_bar(percent,100u);}''',
        18: '''int main(void){uint16_t x;uint8_t on=0u;exam_init();exam_potentiometer_start();for(;;)if(exam_potentiometer_read_raw(&x)==EXAM_OK){if(!on&&x>=2800u)on=1u;else if(on&&x<=2400u)on=0u;exam_led_set(0u,on!=0u);}}''',
        19: '''static uint16_t median5(uint16_t*a){for(size_t i=1u;i<5u;++i){uint16_t v=a[i];size_t j=i;while(j&&a[j-1u]>v){a[j]=a[j-1u];--j;}a[j]=v;}return a[2];}int main(void){uint16_t ring[5]={0},copy[5],x;uint32_t sum=0u;size_t at=0u;exam_init();exam_potentiometer_start();for(;;)if(exam_potentiometer_read_raw(&x)==EXAM_OK){sum-=ring[at];ring[at]=x;sum+=x;at=(at+1u)%5u;for(size_t i=0u;i<5u;++i)copy[i]=ring[i];exam_leds_bar((sum/5u+median5(copy))/2u,4095u);}}''',
        20: '''static uint16_t samples[32];static size_t head,count;static void tick(exam_timer_t t,uint32_t f){(void)t;if(exam_timer_match_happened(f,0u))exam_events_set(1u);}int main(void){uint16_t x;exam_init();exam_potentiometer_start();exam_timer_periodic_ms(EXAM_TIMER_3,10u,tick);for(;;){if(exam_events_take(1u)&&exam_potentiometer_read_raw(&x)==EXAM_OK){samples[head]=x;head=(head+1u)%32u;if(count<32u)++count;exam_leds_bar(count,32u);}exam_idle();}}''',
        21: '''static const uint16_t triangle[]={0u,256u,512u,768u,1023u,768u,512u,256u};int main(void){exam_init();if(exam_dac_play(triangle,8u,8000u,EXAM_TIMER_3)!=EXAM_OK)return 1;for(;;)exam_idle();}''',
        22: '''static void make_tables(uint16_t*square,uint16_t*triangle,uint16_t*saw,size_t n){for(size_t i=0u;i<n;++i){square[i]=(i<n/2u)?0u:1023u;saw[i]=(uint16_t)((1023u*i)/(n-1u));triangle[i]=(i<n/2u)?(uint16_t)((2046u*i)/n):(uint16_t)((2046u*(n-i-1u))/n);}}int main(void){uint16_t sq[32],tri[32],saw[32];exam_init();make_tables(sq,tri,saw,32u);exam_dac_write_percent(50u);return exam_dac_play(tri,32u,8000u,EXAM_TIMER_3)==EXAM_OK?0:1;}''',
        23: '''static const uint16_t wave[]={0u,512u,1023u,512u};int main(void){uint8_t loop=1u;exam_init();for(;;){if(loop){if(exam_dac_play(wave,4u,1000u,EXAM_TIMER_3)==EXAM_BUSY){exam_idle();continue;}for(volatile uint32_t i=0u;i<500000u;++i){} }else exam_dac_stop();}}''',
        24: '''int main(void){uint16_t adc;exam_init();exam_potentiometer_start();for(;;)if(exam_adc_read_raw(5u,&adc)==EXAM_OK)exam_dac_write_raw((uint16_t)(adc>>2));}''',
        25: '''enum{EV_WORK=1u};static void button(exam_button_t b,exam_button_event_t e){(void)b;if(e==EXAM_PRESS)exam_events_set(EV_WORK);}int main(void){exam_init();exam_buttons_start(button);exam_button_irq_start(EXAM_BUTTON_INT0);for(;;){if(exam_events_take(EV_WORK)){exam_led_toggle(0u);/* slow application work belongs here */}exam_idle();}}''',
        26: '''typedef struct{uint32_t count,total;}Shared;static volatile Shared shared;static void tick(exam_timer_t t,uint32_t f){(void)t;if(exam_timer_match_happened(f,0u)){++shared.count;shared.total+=10u;}}int main(void){Shared snap;exam_init();exam_timer_periodic_ms(EXAM_TIMER_3,10u,tick);for(;;){uint32_t s=exam_critical_enter();snap.count=shared.count;snap.total=shared.total;exam_critical_exit(s);exam_leds_bar(snap.count&255u,255u);}}''',
        27: '''static void button(exam_button_t b,exam_button_event_t e){if(b==EXAM_BUTTON_INT0&&e==EXAM_PRESS)exam_events_set(1u);}int main(void){uint32_t started;exam_init();exam_buttons_confirmation_ms(40u);if(exam_rit_start()!=EXAM_OK)return 1;started=exam_rit_ticks();exam_buttons_start(button);exam_button_irq_start(EXAM_BUTTON_INT0);for(;;){if(exam_events_take(1u)){exam_leds_write((uint8_t)(exam_rit_ticks()-started));exam_rit_stop();for(;;)exam_idle();}exam_idle();}}''',
        28: '''int main(void){uint32_t last;exam_init();exam_systick_periodic_ms(1u);last=exam_systick_ticks();for(;;){uint32_t now=exam_systick_ticks();if((uint32_t)(now-last)>=250u){last+=250u;exam_led_toggle(0u);}exam_idle();}}''',
        29: '''static volatile uint8_t armed;static volatile uint32_t stamp;static void button(exam_button_t b,exam_button_event_t e){(void)b;if(e==EXAM_PRESS)armed=1u;}static void capture(uint8_t t,uint32_t f){if(armed&&timer_capture_occurred(f,0u)&&timer_read_capture(t,0u,(uint32_t*)&stamp)==BOARD_OK){armed=0u;exam_events_set(1u);}}int main(void){exam_init();exam_buttons_start(button);exam_button_irq_start(EXAM_BUTTON_INT0);timer_set_callback(0u,capture);timer_configure_capture(0u,0u,CAPTURE_RISING,1u);timer_start(0u);for(;;)if(exam_events_take(1u))exam_leds_write((uint8_t)stamp);}''',
        30: '''extern uint32_t scale_sample_asm(uint32_t sample,uint32_t maximum);static void button(exam_button_t b,exam_button_event_t e){(void)b;if(e==EXAM_PRESS)exam_events_set(1u);}int main(void){uint16_t sample;exam_init();exam_potentiometer_start();exam_buttons_start(button);exam_button_irq_start(EXAM_BUTTON_INT0);for(;;)if(exam_events_take(1u)&&exam_potentiometer_read_raw(&sample)==EXAM_OK)exam_leds_write((uint8_t)scale_sample_asm(sample,4095u));}''',
        31: '''static const uint16_t note[]={0u,256u,512u,768u,1023u,768u,512u,256u};static volatile uint8_t playing=1u;static uint8_t at;static void sample_tick(uint8_t t,uint32_t f){(void)t;if(timer_match_occurred(f,0u)){exam_dac_write_raw(playing?note[at]:0u);at=(uint8_t)((at+1u)%8u);}}static void duration_tick(uint8_t t,uint32_t f){(void)t;if(timer_match_occurred(f,0u))exam_events_set(1u);}static void envelope_tick(uint8_t t,uint32_t f){(void)t;if(timer_match_occurred(f,0u))exam_events_set(2u);}int main(void){exam_init();timer_start_periodic_interrupt_ms(0u,500u,duration_tick);timer_start_periodic_interrupt_ms(1u,100u,envelope_tick);timer_start_periodic_interrupt_hz(2u,8000u,1u,sample_tick);for(;;){uint32_t e=exam_events_take(3u);if(e&1u)playing^=1u;if(e&2u)exam_led_toggle(0u);exam_idle();}}''',
        32: '''typedef struct{const int32_t*data;uint32_t count;int32_t bias;}Job;extern int32_t weighted_sum_asm(const int32_t*a,uint32_t n,int32_t scale,int32_t offset,int32_t limit,const Job*job);int main(void){static const int32_t a[]={1,2,3,4};Job j={a,4u,1};int32_t r;exam_init();r=weighted_sum_asm(a,4u,2,3,100,&j);exam_leds_bar((uint32_t)(r<0?0:r),100u);for(;;)exam_idle();}''',
    }
    return common + _format_c_source(programs[number])


ASSEMBLY = {
    30: '''                AREA |.text.answers|, CODE, READONLY\n                THUMB\n                EXPORT scale_sample_asm\nscale_sample_asm\n                CMP r1, #0\n                MOVEQ r0, #0\n                BXEQ lr\n                MOV r2, #255\n                MUL r0, r0, r2\n                UDIV r0, r0, r1\n                BX lr\n                END\n''',
    32: '''                AREA |.text.answers|, CODE, READONLY\n                THUMB\n                EXPORT weighted_sum_asm\nweighted_sum_asm\n                PUSH {r4-r7,lr}\n                LDR r4, [sp, #20]      ; fifth argument: limit\n                LDR r5, [sp, #24]      ; sixth argument: Job pointer\n                MOVS r6, #0\nloop_ws         CMP r1, #0\n                BEQ done_ws\n                LDR r7, [r0], #4\n                MLA r6, r7, r2, r6\n                SUBS r1, r1, #1\n                B loop_ws\ndone_ws         ADD r0, r6, r3\n                CMP r0, r4\n                IT GT\n                MOVGT r0, r4\n                LDR r6, [r5, #8]\n                ADD r0, r0, r6\n                POP {r4-r7,pc}\n                END\n''',
}


def recipe_specs() -> list[dict[str, object]]:
    result = []
    for number, slug, title, components, ownership, flow, history, questions in RECIPE_META:
        result.append({
            "number": number,
            "slug": slug,
            "title": title,
            "summary": f"A complete exam-project example for {title.lower()} with explicit ownership and bounded foreground work.",
            "components": components,
            "ownership": ownership,
            "flow": flow,
            "history": history,
            "questions": questions,
            "initialization": "Call exam_init first, configure each owner once, clear state, then enable callbacks or sampling.",
            "conflicts": "Do not configure one peripheral through two interfaces, block inside a callback, or share multiword state without a deliberate snapshot.",
            "code": _program(number),
            "assembly": ASSEMBLY.get(number, ""),
        })
    return result
