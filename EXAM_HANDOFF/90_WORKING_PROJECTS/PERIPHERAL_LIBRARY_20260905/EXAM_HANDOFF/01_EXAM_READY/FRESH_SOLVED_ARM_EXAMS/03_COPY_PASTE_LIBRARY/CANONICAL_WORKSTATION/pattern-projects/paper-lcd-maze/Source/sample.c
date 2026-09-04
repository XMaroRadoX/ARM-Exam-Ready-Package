#include "exam_api.h"
#include "GLCD/GLCD.h"
#define ROWS 6u
#define COLS 5u
#define CELL 16u
extern void depthFirstSearch(uint8_t*,uint32_t,uint32_t,uint32_t);
uint8_t maze[ROWS][COLS];
uint32_t current_row=1u,current_column=2u;
static volatile uint32_t moves[8],head,tail;
volatile uint32_t dropped_moves;
void RIT_IRQHandler(void) {
  static uint32_t previous;
  uint32_t now,edges,next;
  exam_rit_ack();now=exam_joystick_read();edges=exam_joystick_pressed_edges(previous,now);previous=now;
  if(!edges)return;
  next=(head+1u)&7u;
  if(next==tail){++dropped_moves;return;}
  moves[head]=edges;__DMB();head=next;
}
/* Passage bits 1,2,3,4 mean right, down, left, up. A zero bit is a wall.
 * Independent bounds checks prevent an invalid maze from leaving the array.
 * Simultaneous directions have the fixed priority right, down, left, up.
 */
uint32_t move_player(uint32_t edges) {
  uint32_t r=current_row,c=current_column,cell=maze[r][c];
  if((edges&EXAM_JOY_RIGHT)&&(cell&2u)&&c+1u<COLS-1u)++c;
  else if((edges&EXAM_JOY_DOWN)&&(cell&4u)&&r+1u<ROWS-1u)++r;
  else if((edges&EXAM_JOY_LEFT)&&(cell&8u)&&c>1u)--c;
  else if((edges&EXAM_JOY_UP)&&(cell&16u)&&r>1u)--r;
  if(r==current_row&&c==current_column)return 0u;
  draw_position((int)current_column,(int)current_row,CELL,Black);
  current_row=r;current_column=c;
  draw_position((int)c,(int)r,CELL,White);return 1u;
}
int main(void) {
  uint32_t r,c;
  exam_init();
  for(r=0u;r<ROWS;++r)for(c=0u;c<COLS;++c)maze[r][c]=(r==0u||c==0u||r==ROWS-1u||c==COLS-1u)?255u:0u;
  depthFirstSearch(&maze[0][0],ROWS,COLS,current_row*COLS+current_column);
  LCD_Initialization();LCD_Clear(Black);LCD_draw_maze(ROWS,COLS,maze,CELL);
  draw_position((int)current_column,(int)current_row,CELL,White);
  exam_joystick_init();
  if(exam_rit_config_ms(50u)!=EXAM_OK)for(;;){}
  exam_rit_start();
  for(;;) {
    uint32_t saved=exam_critical_enter(),edges;
    if(tail==head){exam_critical_exit(saved);continue;}
    edges=moves[tail];tail=(tail+1u)&7u;exam_critical_exit(saved);
    (void)move_player(edges);
  }
}
