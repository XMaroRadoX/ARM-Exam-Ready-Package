#include <stdint.h>
#include "exam_api.h"
#include "LPC17xx.h"

#define ROWS 3u
#define COLS 4u
extern void kruskal(uint8_t *maze,uint8_t *horizontal,uint8_t *vertical,
                    uint32_t rows,uint32_t columns,uint32_t increment,uint32_t offset);
static uint8_t maze[ROWS*COLS];
static uint8_t horizontal[ROWS*COLS];
static uint8_t vertical[ROWS*COLS];
static uint32_t increment;
static uint8_t selection_count;

static uint32_t button_value(exam_button_t b)
{ return b==EXAM_BUTTON_INT0?2u:(b==EXAM_BUTTON_KEY1?3u:4u); }

static void initialize_arrays(void)
{
  uint32_t r,c,k;
  for(r=0u;r<ROWS;++r)for(c=0u;c<COLS;++c){
    k=r*COLS+c; maze[k]=(uint8_t)k;
    horizontal[k]=(c==COLS-1u)?2u:1u;
    vertical[k]=(r==ROWS-1u)?2u:1u;
  }
}

static void handle_button(exam_button_t button)
{
  uint32_t value;
  value=button_value(button);
  if(selection_count==0u){increment=value;selection_count=1u;}
  else {selection_count=0u;kruskal(maze,horizontal,vertical,ROWS,COLS,increment,value);}
}

void EINT0_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_INT0); handle_button(EXAM_BUTTON_INT0); }
void EINT1_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_KEY1); handle_button(EXAM_BUTTON_KEY1); }
void EINT2_IRQHandler(void)
{ exam_button_ack(EXAM_BUTTON_KEY2); handle_button(EXAM_BUTTON_KEY2); }

int main(void)
{
  exam_init();
  initialize_arrays(); selection_count=0u; exam_led_clear();
  exam_buttons_init();

  for (;;) {
    __WFI();
  }
}
