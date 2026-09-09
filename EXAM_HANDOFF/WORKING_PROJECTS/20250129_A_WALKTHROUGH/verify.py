from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAINT = ROOT / '01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE'
sys.path.insert(0, str(MAINT))
from VERIFY_ALGORITHMS import gas, run, emulate, CLANG, LLD

BUILD = HERE / '.verification'
BUILD.mkdir(exist_ok=True)
(BUILD / 'LPC17xx.h').write_text('''
#ifndef MOCK_LPC
#define MOCK_LPC
#include <stdint.h>
typedef enum { EINT0_IRQn, EINT1_IRQn, EINT2_IRQn, RIT_IRQn, TIMER0_IRQn, TIMER1_IRQn } IRQn_Type;
static inline void __disable_irq(void) {}
static inline void __enable_irq(void) {}
static inline void __WFI(void) {}
static inline void NVIC_DisableIRQ(IRQn_Type x) { (void)x; }
static inline void NVIC_ClearPendingIRQ(IRQn_Type x) { (void)x; }
static inline void NVIC_SetPriority(IRQn_Type x, uint32_t p) { (void)x; (void)p; }
#endif
''')
(BUILD / 'fixture.c').write_text(r'''
#define main application_main
#include "../sample.c"
#undef main
#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)
static uint32_t input_counter, button_events, timer_flags;
static uint8_t output_leds, running;
uint32_t exam_timer_read(exam_timer_t t) { (void)t; return input_counter; }
exam_status_t exam_debounce_begin(exam_button_t b) { (void)b; return EXAM_OK; }
void exam_timer_stop(exam_timer_t t) { (void)t; running=0; }
void exam_timer_start(exam_timer_t t) { (void)t; running=1; }
void exam_timer_reset(exam_timer_t t) { (void)t; running=0; }
uint32_t exam_timer_ack(exam_timer_t t) { uint32_t f=timer_flags; (void)t; timer_flags=0; return f; }
void exam_led_write(uint8_t x) { output_leds=x; }
void exam_rit_ack(void) {}
void exam_debounce_tick(void) {}
uint32_t exam_button_events_take(void) { uint32_t e=button_events; button_events=0; return e; }
static uint32_t reference(const uint8_t *a, uint32_t b, uint32_t c) {
    uint32_t out=c & 255u, row, k, parity;
    for(row=0;row<8;row++) {
        parity=0;
        for(k=0;k<8;k++) parity ^= ((a[row]>>k)&1u) & ((b>>k)&1u);
        out ^= parity << (7-row);
    }
    return out;
}
int test_main(void) {
    static const uint8_t matrices[4][8] = {
        {0xF8,0x7C,0x3E,0x1F,0x8F,0xC7,0xE3,0xF1},
        {0x8F,0xC7,0xE3,0xF1,0xF8,0x7C,0x3E,0x1F},
        {128,64,32,16,8,4,2,1},
        {0,255,1,128,85,170,15,240}
    };
    uint32_t m,b,c;
    for(m=0;m<4;m++) for(b=0;b<256;b++) for(c=0;c<256;c+=51)
        CHECK(bitwiseAffineTransformation(matrices[m],b,c)==reference(matrices[m],b,c));
    CHECK(bitwiseAffineTransformation(matrices[0],0xAA,0x63)==0xC9);
    CHECK(bitwiseAffineTransformation(matrices[1],0xE8,0x63)==0x56);
    CHECK(bitwiseAffineTransformation(matrices[1],0x1234E8,0xABC063)==0x56);
    input_counter=0xABCD42AA;
    EINT0_IRQHandler();
    CHECK(timer1_sample==0x42AA);
    button_events=EXAM_BUTTON_EVENT_INT0;
    RIT_IRQHandler();
    CHECK(displayed_value==0xE8 && output_leds==0xE8 && !running && !blinking);
    button_events=EXAM_BUTTON_EVENT_KEY1;
    RIT_IRQHandler();
    CHECK(displayed_value==0x56 && output_leds==0x56 && running && blinking);
    timer_flags=1; TIMER0_IRQHandler();
    CHECK(output_leds==0 && displayed_value==0x56);
    timer_flags=1; TIMER0_IRQHandler();
    CHECK(output_leds==0x56);
    timer_flags=1; TIMER0_IRQHandler();
    button_events=EXAM_BUTTON_EVENT_KEY1; RIT_IRQHandler();
    CHECK(displayed_value==reference(matrices[1],0x56,0x63));
    CHECK(output_leds==displayed_value && running && leds_on);
    input_counter=0x1234; EINT0_IRQHandler();
    button_events=EXAM_BUTTON_EVENT_INT0; RIT_IRQHandler();
    CHECK(displayed_value==0x26 && output_leds==0x26 && !blinking && !running);
    timer_flags=1; TIMER0_IRQHandler();
    CHECK(output_leds==0x26);
    return 0;
}
''')
(BUILD / 'affine.s').write_text(gas((HERE / 'bitwiseAffineTransformation.s').read_text()))
api = ROOT / '01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/Source/exam_api'
flags = ['--target=arm-none-eabi','-mcpu=cortex-m3','-mthumb','-O1','-ffreestanding','-fno-builtin','-fno-stack-protector','-ffunction-sections','-fdata-sections']
run([CLANG,*flags,'-Wall','-Wextra','-Werror','-I',BUILD,'-I',api,'-c',BUILD/'fixture.c','-o',BUILD/'fixture.o'])
run([CLANG,*flags,'-c',BUILD/'affine.s','-o',BUILD/'affine.o'])
run([LLD,'-Ttext=0x10000','--entry=test_main','--gc-sections',BUILD/'fixture.o',BUILD/'affine.o','-o',BUILD/'test.elf'])
result,called,untested=emulate(BUILD/'test.elf',['bitwiseAffineTransformation'])
assert result == 0, f'Failed at fixture line {result}'
assert not untested
print('PASS: 6144 reference comparisons; example/upper-bit checks; assembly ABI and stack preservation; mocked button/blink/restart scenarios.')
print('C compiled for Cortex-M3 with warnings treated as errors. Native Keil and physical-board execution not performed.')
