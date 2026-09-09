
#include <stdint.h>
int _fltused=0;
void *memcpy(void*d,const void*s,__SIZE_TYPE__ n){unsigned char*a=d;const unsigned char*b=s;while(n--)*a++=*b++;return d;}
void *memset(void*d,int v,__SIZE_TYPE__ n){unsigned char*a=d;while(n--)*a++=(unsigned char)v;return d;}
#include "exam_api.h"
#define CHECK(x) do {if(!(x))return __LINE__;}while(0)
static uint32_t mock_budget, mock_joy, mock_led, mock_events, mock_buttons;
static uint32_t mock_pending[4]={1,1,1,1}, mock_counter[4], mock_period[4], mock_mode[4],mock_running[4];
static uint32_t mock_rit_running,mock_calls,mock_arg[8],mock_return, mock_adc_fresh,mock_adc_value,mock_dac,mock_dac_calls;
void exam_init(void) {}
void exam_led_write(uint8_t v){mock_led=v;}
uint8_t exam_led_read(void){return (uint8_t)mock_led;}
void exam_led_clear(void){mock_led=0;}
exam_status_t exam_led_on(uint8_t n){if(n<4||n>11)return EXAM_OUT_OF_RANGE;mock_led|=1u<<(11-n);return EXAM_OK;}
exam_status_t exam_led_off(uint8_t n){if(n<4||n>11)return EXAM_OUT_OF_RANGE;mock_led&=~(1u<<(11-n));return EXAM_OK;}
void exam_buttons_init(void){}
void exam_button_ack(exam_button_t b){(void)b;}
exam_status_t exam_debounce_config(uint32_t a,uint32_t b){return a==10&&b==50?EXAM_OK:EXAM_BAD_ARGUMENT;}
exam_status_t exam_debounce_begin(exam_button_t b){mock_arg[7]=b;return EXAM_OK;}
void exam_debounce_tick(void){}
uint32_t exam_button_events_take(void){uint32_t v=mock_buttons;mock_buttons=0;return v;}
exam_status_t exam_timer_config_ticks(exam_timer_t t,uint32_t n,exam_timer_mode_t m){mock_period[t]=n;mock_mode[t]=m;return EXAM_OK;}
exam_status_t exam_timer_config_ms(exam_timer_t t,uint32_t n,exam_timer_mode_t m){return exam_timer_config_ticks(t,n,m);}
void exam_timer_start(exam_timer_t t){mock_running[t]=1;}
void exam_timer_stop(exam_timer_t t){mock_running[t]=0;}
void exam_timer_reset(exam_timer_t t){mock_counter[t]=0;}
uint32_t exam_timer_read(exam_timer_t t){return mock_counter[t];}
uint32_t exam_timer_ack(exam_timer_t t){return mock_pending[t];}
uint8_t exam_timer_is_running(exam_timer_t t){return (uint8_t)mock_running[t];}
exam_status_t exam_rit_config_ms(uint32_t n){return n==10?EXAM_OK:EXAM_BAD_ARGUMENT;}
void exam_rit_start(void){mock_rit_running=1;}
void exam_rit_stop(void){mock_rit_running=0;}
void exam_rit_ack(void){}
void exam_joystick_init(void){}
uint32_t exam_joystick_read(void){return mock_joy;}
uint32_t exam_joystick_pressed_edges(uint32_t old,uint32_t now){return now&~old;}
void exam_adc_init(void){}
void exam_adc_start(void){}
void exam_adc_irq_capture(void){}
uint8_t exam_adc_take(uint16_t *v){if(!mock_adc_fresh)return 0;*v=(uint16_t)mock_adc_value;mock_adc_fresh=0;return 1;}
void exam_dac_init(void){}
exam_status_t exam_dac_write(int32_t v){mock_dac=(uint32_t)v;mock_dac_calls++;return EXAM_OK;}
void exam_events_set(uint32_t v){mock_events|=v;}
uint32_t exam_events_take(uint32_t mask){uint32_t v=mock_events&mask;mock_events&=~mask;return v;}
uint32_t exam_critical_enter(void){return 0;}
void exam_critical_exit(uint32_t saved){(void)saved;}
void NVIC_SetPriority(int irq,uint32_t p){(void)irq;(void)p;}
static void review_step(void);
int BullsAndCows(int*g,int*s,int*a,int*b){mock_calls++;for(int i=0;i<4;i++)if(a[i]||b[i])mock_arg[6]=1;return (int)mock_return;}
#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"
enum {
  EXAM_EVENT_JOYSTICK = 1u << 1
};

extern int BullsAndCows(int guess[4], int secret[4],
                        int guessFrequency[4], int secretFrequency[4]);

typedef enum {
  WAIT_START = 0,
  EDIT_GUESS,
  SHOW_RESULT,
  FINISHED
} game_state_t;

static int guess[4];
static int secret[4];
static int guessFrequency[4];
static int secretFrequency[4];
static volatile uint32_t joystick_press_edges;
static uint32_t previous_joystick;
static uint32_t candidate_joystick;
static uint32_t stable_samples;
static game_state_t game_state;

static void clear_words(int values[4])
{
  uint32_t i;
  for (i = 0u; i < 4u; ++i) values[i] = 0;
}

static void display_guess(void)
{
  uint8_t packed = (uint8_t)(((uint32_t)guess[0] << 0) |
                             ((uint32_t)guess[1] << 2) |
                             ((uint32_t)guess[2] << 4) |
                             ((uint32_t)guess[3] << 6));
  (void)exam_led_write(packed);
}

static void capture_secret(void)
{
  uint32_t timer_value = exam_timer_read(EXAM_TIMER1);
  uint32_t i;
  for (i = 0u; i < 4u; ++i) {
    secret[i] = (int)((timer_value >> (i * 4u)) & 0x3u);
  }
}

static void begin_guess(void)
{
  clear_words(guess);
  exam_led_clear();
  display_guess();
  game_state = EDIT_GUESS;
}

static void increment_digit(uint32_t index)
{
  guess[index] = (guess[index] + 1) & 0x3;
  display_guess();
}

static void evaluate_guess(void)
{
  int result;
  clear_words(guessFrequency);
  clear_words(secretFrequency);
  result = BullsAndCows(guess, secret, guessFrequency, secretFrequency);
  (void)exam_led_write((uint8_t)result);
  game_state = ((((uint32_t)result >> 4) & 0xFu) == 0xFu) ? FINISHED : SHOW_RESULT;
}

void RIT_IRQHandler(void)
{
  uint32_t current;
  uint32_t pressed;
  exam_rit_ack();
  current=exam_joystick_read();
  if (current != candidate_joystick) {
    candidate_joystick = current; stable_samples = 1u; return;
  }
  if (stable_samples < 3u) ++stable_samples;
  if (stable_samples < 3u) return;
  pressed=exam_joystick_pressed_edges(previous_joystick,current);
  previous_joystick=current;
  if(pressed!=0u){joystick_press_edges|=pressed;exam_events_set(EXAM_EVENT_JOYSTICK);}
}

int answer_main(void)
{
  exam_status_t timer_status;
  exam_status_t joystick_status;
  exam_init();

  clear_words(guess);
  clear_words(secret);
  clear_words(guessFrequency);
  clear_words(secretFrequency);
  joystick_press_edges = 0u;
  game_state = WAIT_START;
  exam_led_clear();

  timer_status=exam_timer_config_ticks(EXAM_TIMER1,UINT32_MAX,
                                       EXAM_TIMER_MODULO_NO_IRQ);
  if(timer_status==EXAM_OK)exam_timer_start(EXAM_TIMER1);
  exam_joystick_init();
  previous_joystick=exam_joystick_read();
  candidate_joystick=previous_joystick;
  stable_samples=3u;
  joystick_status=exam_rit_config_ms(10u);
  if(joystick_status==EXAM_OK)exam_rit_start();

  if (timer_status != EXAM_OK || joystick_status != EXAM_OK) {
    (void)exam_led_write(0xFFu);
    game_state = FINISHED;
  }

  return 0;
}

static void review_step(void){
    uint32_t edges;
    uint32_t saved;

    if ((exam_events_take(EXAM_EVENT_JOYSTICK) & EXAM_EVENT_JOYSTICK) == 0u) {
      __WFI();
      return;
    }

    saved = exam_critical_enter();
    edges = joystick_press_edges;
    joystick_press_edges = 0u;
    exam_critical_exit(saved);

    if ((edges & EXAM_JOY_SELECT) != 0u) {
      if (game_state == WAIT_START) {
        capture_secret();
        begin_guess();
      } else if (game_state == EDIT_GUESS) {
        evaluate_guess();
      } else if (game_state == SHOW_RESULT) {
        begin_guess();
      }
      __WFI();
      return;
    }

    if (game_state != EDIT_GUESS) {
      __WFI();
      return;
    }
    if ((edges & EXAM_JOY_DOWN) != 0u) increment_digit(0u);
    if ((edges & EXAM_JOY_LEFT) != 0u) increment_digit(1u);
    if ((edges & EXAM_JOY_RIGHT) != 0u) increment_digit(2u);
    if ((edges & EXAM_JOY_UP) != 0u) increment_digit(3u);
    __WFI();
  }


__declspec(dllexport) int test_main(void){answer_main();
mock_counter[1]=0x00121ab6;
mock_joy=EXAM_JOY_SELECT;RIT_IRQHandler();review_step();CHECK(game_state==WAIT_START);
RIT_IRQHandler();RIT_IRQHandler();review_step();CHECK(game_state==EDIT_GUESS&&secret[0]==2&&secret[1]==3&&secret[2]==2&&secret[3]==1);
for(int j=0;j<2;j++){mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_joy=EXAM_JOY_DOWN;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();}
CHECK(guess[0]==2&&mock_led==2);for(int k=0;k<8;k++)RIT_IRQHandler();review_step();CHECK(guess[0]==2);
mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_return=0x13;mock_joy=EXAM_JOY_SELECT;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();CHECK(game_state==SHOW_RESULT&&mock_led==0x13&&!mock_arg[6]);
mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_joy=EXAM_JOY_SELECT;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();CHECK(game_state==EDIT_GUESS&&guess[0]==0&&secret[0]==2);
mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_return=0xf0;mock_joy=EXAM_JOY_SELECT|EXAM_JOY_DOWN;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();CHECK(game_state==FINISHED&&mock_led==0xf0&&guess[0]==0);
mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_joy=EXAM_JOY_DOWN;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();CHECK(game_state==FINISHED&&mock_led==0xf0);
return 0;}
