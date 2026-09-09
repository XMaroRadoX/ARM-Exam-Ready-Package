
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

uint32_t shortestPath(uint32_t r,uint32_t c,uint8_t*m){
  uint8_t dist[72];for(uint32_t i=0;i<72;i++)dist[i]=255;dist[9]=0;
  for(uint32_t k=0;k<30;k++)for(uint32_t i=0;i<72;i++)if(dist[i]==k){int off[4]={1,-1,8,-8};for(int j=0;j<4;j++){uint32_t p=i+off[j];if(m[p]==' '&&dist[p]==255)dist[p]=(uint8_t)(k+1);}}
  for(uint32_t i=0;i<72;i++)if(m[i]==' '&&dist[i]!=255)m[i]=dist[i];return 8;}

#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

static void leds_fill(void)
{
  (void)exam_led_write(0xFFu);
}
#define ROWS 9u
#define COLS 8u
#define EVENT_HALF_SECOND (1u<<0)
extern uint32_t shortestPath(uint32_t rows,uint32_t columns,uint8_t *maze);
static uint8_t maze[ROWS][COLS]={"XXXXXXXX",{'X',0,' ',' ',' ',' ',' ','X'},"X XXXX X","X      X","XX X XXX","X  X  eX","X XX XXX","X      X","XXXXXXXX"};
static uint32_t position;
static int32_t step_value;
static uint8_t showing;

void TIMER0_IRQHandler(void)
{ if ((exam_timer_ack(EXAM_TIMER0) & 1u) != 0u) exam_events_set(EVENT_HALF_SECOND); }

static uint8_t find_entrance(void)
{ uint32_t i; uint8_t *cells=&maze[0][0]; for(i=0u;i<ROWS*COLS;++i)if(cells[i]=='e'){position=i;return 1u;} return 0u; }

static void show_next_move(void)
{
  uint32_t next=position; uint8_t board_label=4u;
  if(step_value<0){exam_led_clear();return;}
  uint8_t *cells=&maze[0][0];
  if(cells[position+1u]==(uint8_t)step_value){next=position+1u;board_label=4u;}
  else if(cells[position+COLS]==(uint8_t)step_value){next=position+COLS;board_label=5u;}
  else if(cells[position-1u]==(uint8_t)step_value){next=position-1u;board_label=6u;}
  else if(cells[position-COLS]==(uint8_t)step_value){next=position-COLS;board_label=7u;}
  else { step_value=-1; return; }
  position=next; (void)exam_led_on(board_label); showing=1u;
}

int answer_main(void)
{
  exam_init();
  step_value=(int32_t)shortestPath(ROWS,COLS,&maze[0][0]);
  showing=0u; exam_led_clear();
  if(step_value < 0 || !find_entrance() ||
     exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC)!=EXAM_OK) {
    leds_fill();
  } else {
    exam_timer_start(EXAM_TIMER0);
  }

  return 0;
}

static void review_step(void){
    if((exam_events_take(EVENT_HALF_SECOND)&EVENT_HALF_SECOND)==0u) {
      __WFI();
      return;
    }
    if(showing){exam_led_clear();showing=0u;--step_value;} else show_next_move();
    __WFI();
  }


__declspec(dllexport) int test_main(void){answer_main();
int expected[9]={6,6,7,7,6,6,6,7,7};CHECK(mock_period[0]==500);
for(int i=0;i<9;i++){TIMER0_IRQHandler();review_step();CHECK(mock_led==(1u<<(11-expected[i])));TIMER0_IRQHandler();review_step();CHECK(mock_led==0);}
TIMER0_IRQHandler();review_step();CHECK(mock_led==0);
return 0;}
