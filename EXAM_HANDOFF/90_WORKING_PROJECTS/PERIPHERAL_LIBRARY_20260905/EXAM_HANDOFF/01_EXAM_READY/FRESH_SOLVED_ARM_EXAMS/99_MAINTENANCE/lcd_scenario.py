"""July 2024 supplied LCD extension, adapted to the maintained project."""
import zipfile
CODE='''#include "exam_api.h"
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
'''
def spec(c):
    archive=next((c['ROOT']/'02_ORIGINAL_MATERIALS/Exams').rglob('20240709 board extension.zip'))
    files={}
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            if '/Source/GLCD/' in name and name.endswith(('.c','.h')):
                rel='Source/GLCD/'+name.rsplit('/',1)[1]
                files[rel]=z.read(name).decode('utf-8',errors='replace').replace('\r\r\n','\n').replace('\r\n','\n')
    assembly=(c['ROOT']/'03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams/2024-07-09_DFS_SysTick/Answer Source/assembly.s').read_text()
    paper=next((c['ROOT']/'02_ORIGINAL_MATERIALS/Exams').rglob('20240709 board extension.pdf'))
    return dict(code=CODE,assembly=assembly,extra_files=files,title='2024-07-09 Q5 — LCD maze and legal joystick movement',purpose='Generate the maze with the supplied ARM depthFirstSearch interface, draw walls at 16-pixel cell size, and move a white square only through open passages.',actions='Start at row 1, column 2. A blocked direction leaves the square still. A legal edge moves one cell. A hold does not repeat. All four outer boundaries remain inaccessible.',features=['Joystick','RIT','LCD'],group='Past exams',history='Appeared in past exams',questions=[],externalQuestion='2024-07-09-Q5',resources=['LCD: supplied GLCD parallel driver; P0.0–P0.7 data, P0.19–P0.25 control; see driver pin masks','RIT:50 ms joystick sampling; IRQ queues edges; foreground performs drawing','ARM depthFirstSearch: original four-argument maze generation contract','Queue:seven usable direction snapshots; dropped_moves reports overflow'],timing='Supplied extension: 16-pixel example cells and 50 ms joystick sampling. Maintained configuration derives the threshold from the actual clock.',states='Initialize boundary sentinels, generate passages, draw maze and initial square. Each queued direction checks both passage bits and array bounds before erasing and redrawing the square.',source=archive.relative_to(c['ROOT']).as_posix(),paper=paper.relative_to(c['ROOT']).as_posix(),notes=[])
