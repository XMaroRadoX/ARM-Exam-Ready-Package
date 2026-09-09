
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
