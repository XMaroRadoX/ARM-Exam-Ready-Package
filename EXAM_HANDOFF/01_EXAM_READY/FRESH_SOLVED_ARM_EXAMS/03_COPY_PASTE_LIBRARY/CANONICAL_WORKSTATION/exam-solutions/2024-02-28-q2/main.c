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

int main(void)
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

  for (;;) {
    if((exam_events_take(EVENT_HALF_SECOND)&EVENT_HALF_SECOND)==0u) {
      __WFI();
      continue;
    }
    if(showing){exam_led_clear();showing=0u;--step_value;} else show_next_move();
    __WFI();
  }
}
