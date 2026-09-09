"""Complete board baselines and variants. All handlers live in sample.c.

The project generator empties the replaced template IRQ files, retaining one
definition per vector. Shared code is expanded into self-contained files.
"""
COMMON = '''#include "exam_api.h"
#include "LPC17xx.h"
static void require(exam_status_t status) {
  if (status != EXAM_OK) { exam_led_write(0xFFu); for (;;) {} }
}
'''

TIMER = '''volatile uint32_t tick_count;
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_match_happened(flags, 0u)) {
    ++tick_count;
    exam_led_write((uint8_t)tick_count);
  }
}
int main(void) {
  exam_init();
  require(exam_timer_config_ms(EXAM_TIMER0, 500u, EXAM_TIMER_PERIODIC));
  exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
'''

BUTTONS = '''volatile uint8_t count;
void EINT0_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_INT0); }
void EINT1_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_KEY1); }
void EINT2_IRQHandler(void) { (void)exam_debounce_begin(EXAM_BUTTON_KEY2); }
void sample_inputs(void) {
  uint32_t events;
  exam_debounce_tick();
  events = exam_button_events_take();
  if (events & EXAM_BUTTON_EVENT_INT0) ++count;
  if (events & EXAM_BUTTON_EVENT_KEY1) exam_timer_stop(EXAM_TIMER0);
  if (events & EXAM_BUTTON_EVENT_KEY2) {
    exam_timer_reset(EXAM_TIMER0);
    (void)exam_timer_ack(EXAM_TIMER0);
    exam_timer_start(EXAM_TIMER0);
  }
}
void RIT_IRQHandler(void) { exam_rit_ack(); sample_inputs(); }
void TIMER0_IRQHandler(void) {
  uint32_t flags = exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_match_happened(flags, 0u)) exam_led_write(count);
}
int main(void) {
  exam_init(); exam_buttons_init();
  require(exam_debounce_config(10u,50u));
  require(exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC));
  require(exam_rit_config_ms(10u));
  exam_timer_start(EXAM_TIMER0); exam_rit_start();
  for (;;) {}
}
'''

RAW_CAPTURE = '''volatile uint32_t captured;
void EINT0_IRQHandler(void) {
  captured = exam_timer_read(EXAM_TIMER1);
  exam_button_ack(EXAM_BUTTON_INT0);
  exam_led_write((uint8_t)captured);
}
int main(void) {
  exam_init(); exam_buttons_init();
  require(exam_timer_config_ticks(EXAM_TIMER1, 0xFFu, EXAM_TIMER_MODULO_NO_IRQ));
  exam_timer_start(EXAM_TIMER1);
  for (;;) {}
}
'''

ORDERED = '''volatile uint32_t entered, bit_count, result;
/* Equal priorities prevent these handlers interrupting one another.
 * Hardware cannot reconstruct chronology of edges already pending together;
 * in that case the NVIC vector ordering decides. */
void EINT1_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_KEY1);
  if (bit_count < 32u) { entered <<= 1; ++bit_count; }
}
void EINT2_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_KEY2);
  if (bit_count < 32u) { entered = (entered << 1) | 1u; ++bit_count; }
}
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  result=entered; exam_led_write((uint8_t)result);
  entered=0u;bit_count=0u;
}
int main(void) {
  exam_init(); exam_buttons_init();
  NVIC_SetPriority(EINT0_IRQn,2u);NVIC_SetPriority(EINT1_IRQn,2u);NVIC_SetPriority(EINT2_IRQn,2u);
  for (;;) {}
}
'''

PARAMETERS = '''volatile uint32_t step, increment, offset, result;
void command(uint32_t identity) {
  if (step == 0u) { increment=identity+2u; step=1u; }
  else { offset=identity; result=increment*10u+offset; exam_led_write((uint8_t)result);step=0u; }
}
void EINT0_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_INT0);command(0u); }
void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1);command(1u); }
void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2);command(2u); }
int main(void) {
  exam_init();exam_buttons_init();
  NVIC_SetPriority(EINT0_IRQn,2u);NVIC_SetPriority(EINT1_IRQn,2u);NVIC_SetPriority(EINT2_IRQn,2u);
  for (;;) {}
}
'''

ADC_BUTTON = '''volatile uint16_t preview, captured;
volatile uint8_t preview_valid, sequence_active, sequence_index;
volatile uint32_t processed;
void ADC_IRQHandler(void) {
  uint16_t sample;
  exam_adc_irq_capture();
  if (exam_adc_take(&sample)) {
    preview=sample; preview_valid=1u;
    if (!sequence_active) exam_adc_show_high8(sample);
  }
  exam_adc_start();
}
void EINT0_IRQHandler(void) {
  exam_button_ack(EXAM_BUTTON_INT0);
  if (!preview_valid || sequence_active) return;
  captured=preview; /* Most recent completed conversion at raw IRQ entry. */
  processed=(uint32_t)(captured >> 4); /* Exam high-eight-bit extraction. */
  sequence_index=0u;sequence_active=1u;
  exam_led_write((uint8_t)processed);
  exam_timer_reset(EXAM_TIMER0);(void)exam_timer_ack(EXAM_TIMER0);exam_timer_start(EXAM_TIMER0);
}
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_match_happened(flags,0u) && sequence_active) {
    if (++sequence_index == 4u) {
      sequence_active=0u;exam_timer_stop(EXAM_TIMER0);exam_led_clear();
    } else exam_led_write((uint8_t)(processed+sequence_index));
  }
}
int main(void) {
  exam_init();exam_buttons_init();exam_adc_init();
  require(exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC));
  NVIC_SetPriority(ADC_IRQn,2u);NVIC_SetPriority(EINT0_IRQn,2u);NVIC_SetPriority(TIMER0_IRQn,2u);
  exam_adc_start();
  for (;;) {}
}
'''

JOYSTICK = '''volatile uint32_t held, pressed, released;
static uint32_t previous;
void RIT_IRQHandler(void) {
  uint32_t current;
  exam_rit_ack();current=exam_joystick_read();
  pressed=exam_joystick_pressed_edges(previous,current);
  released=exam_joystick_released_edges(previous,current);
  held=current;previous=current;
  if (pressed & EXAM_JOY_SELECT) exam_led_write(1u);
  if (released & EXAM_JOY_SELECT) exam_led_clear();
}
int main(void) {
  exam_init();exam_joystick_init();previous=exam_joystick_read();
  require(exam_rit_config_ms(10u));exam_rit_start();
  for (;;) {}
}
'''

DAC = '''static const uint16_t waveform[8]={512u,768u,1023u,768u,512u,256u,0u,256u};
volatile uint32_t sample_index, completed;
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_match_happened(flags,0u)) {
    (void)exam_dac_write(waveform[sample_index]);
    if (++sample_index == 8u) { sample_index=0u; ++completed; }
  }
}
void begin_wave(void) {
  sample_index=0u;completed=0u;
  exam_timer_reset(EXAM_TIMER0);(void)exam_timer_ack(EXAM_TIMER0);exam_timer_start(EXAM_TIMER0);
}
int main(void) {
  exam_init();exam_dac_init();
  require(exam_timer_config_ticks(EXAM_TIMER0,1263u,EXAM_TIMER_PERIODIC));
  begin_wave();
  for (;;) {}
}
'''

CAPTURE = '''volatile uint32_t last_capture, capture_count;
void TIMER0_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER0);
  if (exam_timer_capture_happened(flags,0u)) { last_capture=LPC_TIM0->CR0; ++capture_count; }
}
int main(void) {
  exam_init();
  require(exam_timer_config_ticks(EXAM_TIMER0,UINT32_MAX,EXAM_TIMER_MODULO_NO_IRQ));
  require(exam_timer_config_match(EXAM_TIMER0,0u,UINT32_MAX,0u));
  /* P1.26 function 3 is CAP0.0; capture TC on rising edges and interrupt. */
  LPC_PINCON->PINSEL3=(LPC_PINCON->PINSEL3 & ~(3u<<20)) | (3u<<20);
  LPC_GPIO1->FIODIR &= ~(1u<<26);
  LPC_TIM0->CCR=(LPC_TIM0->CCR & ~7u) | 5u;
  (void)exam_timer_ack(EXAM_TIMER0);NVIC_ClearPendingIRQ(TIMER0_IRQn);
  NVIC_EnableIRQ(TIMER0_IRQn);exam_timer_start(EXAM_TIMER0);
  for (;;) {}
}
'''

def board_projects():
    from peripheral_helper_docs import ADVANCED_EXAMPLE
    def spec(code,purpose,actions,resources):
        return dict(code=COMMON+code,assembly='        END\n',purpose=purpose,actions=actions,resources=resources)
    projects={
      'timer-periodic':spec(TIMER,'Count and display every half-second match.','After reset count=0; after two matches count=2 and display=0x02.',['Timer0: 500 ms; TIMER0_IRQHandler updates count; foreground idle']),
      'buttons-rit-timer':spec(BUTTONS,'Confirmed inputs and display timer with separate owners.','INT0 increases count once after 5 sampled lows; KEY1 pauses display; KEY2 resets and starts its interval. Release then press for another action.',['RIT: 10 ms debounce; RIT_IRQHandler calls sample_inputs','Timer0: 500 ms display; TIMER0_IRQHandler','EINT0..2: begin debounce only']),
      'raw-capture-ff':spec(RAW_CAPTURE,'Capture the modulo counter immediately on a raw button IRQ.','Set Timer1 TC=37 in debugger; INT0 saves and displays37. Counter resets at0xFF. Bounce intentionally produces raw IRQs.',['Timer1: MR0=0xFF, reset without IRQ','EINT0: capture before acknowledgement']),
      'ordered-binary':spec(ORDERED,'Process raw button commands without losing identity to merged bits.','KEY2,KEY1,KEY1,KEY2,KEY2,KEY1 then INT0 produces binary100110=38. At32 bits further digit commands are ignored.',['EINT1=append0; EINT2=append1; EINT0=submit','Equal NVIC priority; foreground idle']),
      'ordered-parameters':spec(PARAMETERS,'Two raw commands choose increment and offset.','KEY1 then KEY2 selects increment3,offset2; teaching computation3*10+2 displays32. This is a parameter-flow demonstration, not the complete Kruskal paper.',['EINT0..2 equal priority; command updates one phase per IRQ']),
      'adc-button-sequence':spec(ADC_BUTTON,'Preview ADC, capture the latest completed sample on a raw press, show four paced values.','ADC4095 previews255; INT0 captures4095, displays255,0,1,2 at500ms steps, then stops. Pot changes do not change the captured sequence.',['ADC: one conversion at a time; ADC_IRQHandler consumes then starts next','EINT0: capture and start sequence','Timer0: 500 ms; same priority as ADC and EINT0']),
      'joystick-release':spec(JOYSTICK,'Raw press, hold and release masks with periodic sampling.','Start with SELECT released; press lights LD11; hold leaves it on; release clears it. High bits never appear.',['RIT:10ms; RIT_IRQHandler owns joystick previous/current state']),
      'dac-stream':spec(DAC,'Explicit table playback with eight samples per waveform cycle.','Each Timer0 match writes the next table value; after8 matches index wraps and completed=1. Sample frequency=PCLK/1263; waveform frequency=sample frequency/8.',['Timer0: exact1263 ticks; TIMER0_IRQHandler writes one sample']),
      'timer-capture-pin':spec(CAPTURE,'Configure a real CAP0.0 input and interpret its saved flag.','Provide rising edges at P1.26; each saves TC in CR0 and updates last_capture. This owns P1.26, so do not initialize joystick in this project.',['P1.26: CAP0.0, CCR rising edge+interrupt','Timer0: PR0; no match actions; TIMER0_IRQHandler reads CR0']),
    }
    p=spec(TIMER.replace('EXAM_TIMER_PERIODIC','EXAM_TIMER_ONE_SHOT'),'One match then hardware stop.','After one500ms interval count=1; further time leaves it1. Reset/start permits another action.',['Timer0:500ms one-shot'])
    projects['timer-one-shot']=p
    projects['timer-exact-ticks']=spec(TIMER.replace('exam_timer_config_ms(EXAM_TIMER0, 500u','exam_timer_config_ticks(EXAM_TIMER0, 1263u'),'Preserve exact ticks rather than reinterpret them as milliseconds.','Each1263 peripheral-clock ticks increments count.',['Timer0:PR0,MR0=1263'])
    pause=TIMER.replace('int main(void)', '''void EINT0_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_INT0);exam_timer_stop(EXAM_TIMER0); }
void EINT1_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY1);exam_timer_start(EXAM_TIMER0); }
void EINT2_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_KEY2);exam_timer_reset(EXAM_TIMER0);(void)exam_timer_ack(EXAM_TIMER0);exam_timer_start(EXAM_TIMER0); }
int main(void)''').replace('exam_init();','exam_init();exam_buttons_init();')
    projects['timer-pause-resume']=spec(pause,'Pause/resume differs from clearing and starting a fresh interval.','INT0 pauses current TC; KEY1 continues it; KEY2 clears TC/PC and starts a full500ms interval.',['Timer0:500ms; raw EINT0/1/2 controls'])
    systick=BUTTONS.replace('void RIT_IRQHandler(void) { exam_rit_ack(); sample_inputs(); }','void SysTick_Handler(void) { sample_inputs(); }').replace('require(exam_rit_config_ms(10u));','require(exam_systick_config_ms(10u));').replace('exam_timer_start(EXAM_TIMER0); exam_rit_start();','exam_timer_start(EXAM_TIMER0);')
    projects['buttons-systick-timer']=spec(systick,projects['buttons-rit-timer']['purpose'],projects['buttons-rit-timer']['actions'],['SysTick:10ms; starts during config','Timer0:500ms; EINT0..2 begin debounce'])
    projects['raw-capture-ffff']=spec(RAW_CAPTURE.replace('0xFFu','0xFFFFu'),'Raw capture with the 16-bit match limit.','Timer1 resets at0xFFFF; INT0 captures TC immediately.',['Timer1:MR0=0xFFFF; EINT0 raw capture'])
    projects['adc-percentage']=spec(ADC_BUTTON.replace('(uint32_t)(captured >> 4)','((uint32_t)captured * 100u + 2047u) / 4095u'),'Scale a captured ADC sample to rounded percent.','ADC0=>0%,2048=>50%,4095=>100%; high8 preview remains unchanged.',['Same ownership as adc-button-sequence'])
    duration=DAC.replace('int main(void)', '''void TIMER1_IRQHandler(void) {
  uint32_t flags=exam_timer_ack(EXAM_TIMER1);
  if (exam_timer_match_happened(flags,0u)) { exam_timer_stop(EXAM_TIMER0);(void)exam_dac_write(512); }
}
int main(void)''').replace('  begin_wave();','  require(exam_timer_config_ms(EXAM_TIMER1,100u,EXAM_TIMER_ONE_SHOT));\n  begin_wave();exam_timer_start(EXAM_TIMER1);')
    projects['dac-duration']=spec(duration,'Waveform timer plus independent duration timer.','Timer0 streams; after100ms Timer1 stops Timer0 and writes midpoint512. No queued playback resumes afterward.',['Timer0:1263 ticks/sample','Timer1:100ms one-shot stops Timer0'])
    once=DAC.replace('++completed;','++completed; exam_timer_stop(EXAM_TIMER0);').replace('int main(void)', '''void EINT0_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_INT0);if (!exam_timer_is_running(EXAM_TIMER0)) begin_wave(); }
int main(void)''').replace('exam_init();exam_dac_init();','exam_init();exam_dac_init();exam_buttons_init();').replace('  begin_wave();','  /* Wait for an INT0 trigger; busy triggers are ignored. */')
    projects['dac-button-once']=spec(once,'A raw press starts one complete table traversal; busy presses are ignored.','INT0 then8 sample matches gives completed=1 and stopped Timer0. A later INT0 restarts at index0.',['EINT0: trigger','Timer0:1263 ticks/sample, stops after8 samples'])
    projects['timer-multiple-matches']=dict(code=ADVANCED_EXAMPLE,assembly='        END\n',purpose='Configure four match notifications using explicit PCLK and PR.',actions='At core100MHz,divider4,PR24, matches arrive at250us,500us,750us,1000us; MR0 resets the period.',resources=['Timer0:four match channels; one handler tests a single snapshot'])
    return projects
