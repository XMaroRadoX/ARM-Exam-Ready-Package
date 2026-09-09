"""Run the actual answer C against explicit hardware/algorithm mocks on the host.
These tests check state and API contracts, not electrical timing or board behavior.
"""
from pathlib import Path
import ctypes,hashlib,json,re,subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
OUT=HERE/'.question-c-tests';OUT.mkdir(exist_ok=True)
API=ROOT/'01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/Source/exam_api'
CLANG=Path('C:/Program Files/LLVM/bin/clang.exe')
REVIEWS=json.loads((HERE/'QUESTION_REVIEWS.json').read_text(encoding='utf-8'))
MOCK=r'''
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
'''
HEADER='''#ifndef MOCK_LPC_H
#define MOCK_LPC_H
#include <stdint.h>
#define __WFI() ((void)0)
#define TIMER0_IRQn 1
#define TIMER1_IRQn 2
#define RIT_IRQn 3
void NVIC_SetPriority(int,uint32_t);
#endif
'''
(OUT/'LPC17xx.h').write_text(HEADER)
FIXTURES={}
def fixture(key,stub,checks,label):FIXTURES[key]=(stub,checks,label)
fixture('2023-02-07-Q2',r'''
void copyData(const int8_t*a,int8_t*b,uint32_t n){while(n--)*b++=*a++;}
void insertionSort(int8_t*a,uint32_t n){mock_calls++;mock_arg[0]=n;for(uint32_t i=1;i<n;i++){int8_t x=a[i];uint32_t j=i;while(j&&a[j-1]>x){a[j]=a[j-1];j--;}a[j]=x;}}
''',r'''
CHECK(mock_period[1]==255&&mock_mode[1]==EXAM_TIMER_MODULO_NO_IRQ);
mock_counter[1]=254;EINT0_IRQHandler();CHECK(values[0]==-2&&mock_led==(1u<<5));
mock_counter[1]=3;EINT0_IRQHandler();CHECK(values[1]==3&&mock_led==(1u<<4));
EINT1_IRQHandler();CHECK(mock_arg[0]==2&&mock_led==1);
for(int i=0;i<30;i++)EINT0_IRQHandler();CHECK(value_count==20);
''','Capture signed bytes, LED6/7 alternation, initialized-prefix sort, full buffer ignored')
fixture('2023-07-04-Q2','uint32_t isSociable(uint32_t n){mock_arg[0]=n;mock_calls++;return mock_return;}',r'''
CHECK(mock_period[1]==2000);mock_return=1;TIMER1_IRQHandler();CHECK(mock_arg[0]==8128&&mock_led==128);
mock_return=0;TIMER1_IRQHandler();CHECK(mock_led==0);
for(int i=0;i<6;i++)TIMER1_IRQHandler();CHECK(mock_arg[0]==8128);
mock_pending[1]=0;TIMER1_IRQHandler();CHECK(mock_calls==8);
''','Seven-value wrap, result1/0 LED mapping, unrelated IRQ ignored; computation stubbed')
fixture('2023-09-18-Q2',r'''
uint32_t digitSum(uint32_t n){uint32_t s=0;do{s+=n%10;n/=10;}while(n);return s;}
uint32_t digitaddition(uint32_t*a,uint32_t n){mock_calls++;if(mock_return==1)return 0;uint32_t sum=digitSum(a[0]);for(uint32_t i=1;i<n;i++){a[i]=a[i-1]+digitSum(a[i-1]);sum+=digitSum(a[i]);}return sum;}
''',r'''
EINT2_IRQHandler();EINT1_IRQHandler();EINT1_IRQHandler();EINT2_IRQHandler();EINT2_IRQHandler();EINT1_IRQHandler();CHECK(entered_value==38);
EINT0_IRQHandler();CHECK(mock_led==128);
mock_return=1;EINT0_IRQHandler();CHECK(mock_led==64);
entered_value=0;mock_return=0;EINT0_IRQHandler();CHECK(mock_led==128&&series[9]==0);
''','Binary input 100110, identity success including zero seed, generation failure displays LED5 without using unfinished tail')
fixture('2024-02-12-Q2','uint32_t mazeSolver(uint32_t r,uint32_t c,uint8_t*m){mock_calls++;mock_arg[0]=r;mock_arg[1]=c;return 0;}',r'''
CHECK(mock_mode[0]==EXAM_TIMER_MODULO_NO_IRQ);mock_counter[0]=300;EINT2_IRQHandler();
CHECK(maze[0][0]=='*'&&maze[0][4]=='n'&&maze[0][6]=='n'&&maze[0][7]=='*');CHECK(mock_calls==1);
mock_counter[0]=0xffffffffu;EINT2_IRQHandler();CHECK(maze[0][1]=='n'&&maze[0][2]=='n'&&maze[0][3]=='*'&&maze[0][4]=='*'&&maze[0][5]=='*'&&maze[0][6]=='*');
CHECK(lcg_next(0xffffffffu)==((0xffffffffu%101u)*18u)%101u);
''','Original seed300 first row and UINT32_MAX seed modulo regression; solver stubbed')
fixture('2024-02-28-Q2',r'''
uint32_t shortestPath(uint32_t r,uint32_t c,uint8_t*m){
  uint8_t dist[72];for(uint32_t i=0;i<72;i++)dist[i]=255;dist[9]=0;
  for(uint32_t k=0;k<30;k++)for(uint32_t i=0;i<72;i++)if(dist[i]==k){int off[4]={1,-1,8,-8};for(int j=0;j<4;j++){uint32_t p=i+off[j];if(m[p]==' '&&dist[p]==255)dist[p]=(uint8_t)(k+1);}}
  for(uint32_t i=0;i<72;i++)if(m[i]==' '&&dist[i]!=255)m[i]=dist[i];return 8;}
''',r'''
int expected[9]={6,6,7,7,6,6,6,7,7};CHECK(mock_period[0]==500);
for(int i=0;i<9;i++){TIMER0_IRQHandler();review_step();CHECK(mock_led==(1u<<(11-expected[i])));TIMER0_IRQHandler();review_step();CHECK(mock_led==0);}
TIMER0_IRQHandler();review_step();CHECK(mock_led==0);
''','Exact nine-direction LED playback with a blank phase between moves; distance labeling supplied by mock')
fixture('2024-07-09-Q2','void depthFirstSearchRandom(uint8_t*m,uint32_t r,uint32_t c,uint32_t s){mock_calls++;mock_arg[0]=r;mock_arg[1]=c;mock_arg[2]=s;}',r'''
CHECK(mock_calls==1&&mock_arg[0]==6&&mock_arg[1]==5&&mock_arg[2]==7);
CHECK(maze[0][0]==255&&maze[1][1]==0);
''','C initializes6x5 borders and calls random DFS from7; SysTick startup verified separately in assembly')
fixture('2024-09-16-Q2','void kruskal(uint8_t*m,uint8_t*h,uint8_t*v,uint32_t r,uint32_t c,uint32_t y,uint32_t x){mock_calls++;mock_arg[0]=r;mock_arg[1]=c;mock_arg[2]=y;mock_arg[3]=x;}',r'''
EINT2_IRQHandler();CHECK(mock_calls==0);EINT0_IRQHandler();CHECK(mock_calls==1&&mock_arg[0]==3&&mock_arg[1]==4&&mock_arg[2]==4&&mock_arg[3]==2);
CHECK(horizontal[3]==2&&vertical[8]==2&&maze[11]==11);
''','Two-button argument order, border markers, distinct starting labels; Kruskal stubbed')
fixture('2025-01-29_ARM1-Q2',r'''
uint32_t bitwiseAffineTransformation(const uint8_t*a,uint32_t b,uint32_t c){mock_calls++;mock_arg[0]=b;mock_arg[1]=a[0];mock_arg[2]=a[7];uint32_t d=c;for(int i=0;i<8;i++){uint32_t v=a[i]&b,p=0;for(int j=0;j<8;j++)p^=(v>>j)&1;d^=p<<(7-i);}return d;}
''',r'''
mock_counter[1]=0x123442aa;EINT0_IRQHandler();CHECK(mock_led==0xe8);EINT1_IRQHandler();CHECK(mock_arg[0]==0xe8&&mock_arg[1]==0x8f&&mock_arg[2]==0x1f&&mock_led==0x56);
CHECK(mock_period[0]==250);TIMER0_IRQHandler();CHECK(mock_led==0);TIMER0_IRQHandler();CHECK(mock_led==0x56);
''','Low16-bit capture, Q2-specific matrix, expected0x56 and250 ms blink phases')
fixture('2025-01-29_ARM2-Q2','void bitMatrixMultiplication(const uint8_t*a,const uint8_t*b,uint8_t*c){mock_calls++;for(int i=0;i<8;i++)c[i]=(uint8_t)(i+1);}',r'''
EINT1_IRQHandler();CHECK(mock_calls==0);for(int i=0;i<8;i++){mock_counter[1]=0x4200+i;EINT0_IRQHandler();}EINT0_IRQHandler();CHECK(input_rows==8&&matrix_a[0]==0x42&&matrix_b[7]==7);
EINT1_IRQHandler();CHECK(mock_led==1&&mock_period[0]==500);for(int i=2;i<=8;i++){TIMER0_IRQHandler();CHECK(mock_led==(uint32_t)i);}TIMER0_IRQHandler();CHECK(mock_led==0&&!mock_running[0]);
''','Early KEY1, exactly eight captures, rows0..7 once, final blank and stop; product stubbed')
fixture('2025-01-29_ARM3-Q2',r'''
void transposition(const uint8_t*a,uint8_t*b){mock_calls++;for(int j=0;j<8;j++){b[j]=0;for(int i=0;i<8;i++)b[j]|=((a[i]>>(7-j))&1)<<(7-i);}}
''',r'''
EINT0_IRQHandler();CHECK(mock_calls==0);for(int i=0;i<8;i++){mock_counter[2]=i;EINT1_IRQHandler();mock_counter[2]=i*3;EINT2_IRQHandler();}EINT0_IRQHandler();CHECK(mock_calls==3&&mock_led==128);
EINT1_IRQHandler();EINT2_IRQHandler();CHECK(count_a==8&&count_b==8);
''','Independent capture counts, three transposition calls, XOR identity, full-buffer guards')
for variant,wave,timer,button in [('ARM1','sine',0,0),('ARM2','cosine',1,1)]:
    name='Maclaurin' if timer==0 else 'Maclaurin_cos'
    fixture('2025-02-12_'+variant+'-Q2',f'int32_t {name}(int32_t y,uint32_t n){{mock_calls++;mock_arg[0]=(uint32_t)y;mock_arg[1]=n;return y;}}',f'''
EINT{button}_IRQHandler();CHECK(mock_period[{timer}]=={1263 if timer==0 else 1592});
for(int i=0;i<8978;i++)TIMER{timer}_IRQHandler();CHECK(mock_calls==8978&&repeat_count==200&&mock_arg[1]==3);
TIMER{timer}_IRQHandler();CHECK(mock_dac==0&&!mock_running[{timer}]);EINT{button}_IRQHandler();CHECK(!mock_running[{timer}]);
CHECK({wave}Values[22]==500);
''','8978 samples from initial half-cycle, order3, output array populated, completion silence, repeated button ignored; recurrence stubbed')
for variant,timer in [('ARM1',0),('ARM2',1)]:
    name='nextElementLCG' if timer==0 else 'LCGsequence'
    stub=f'uint32_t {name}(uint32_t p,uint32_t a,uint32_t c,uint32_t n,uint32_t m){{mock_calls++;return ((p*a+c)^'+('n' if timer==0 else '(p>>n)')+')%m;}'
    expected=[9,9,8,8,11,8,9,9,9,10] if timer==0 else [5,6,5,4,7,5,6,7,6,4]
    fixture('2025-07-01_'+variant+'-Q2',stub,f'''
int expected[10]={{{','.join(map(str,expected))}}};CHECK(mock_period[{timer}]=={3000 if timer==0 else 2500});
for(int i=0;i<10;i++){{TIMER{timer}_IRQHandler();CHECK(mock_led==(1u<<(11-expected[i])));}}CHECK(mock_calls==10&&!mock_running[{timer}]);TIMER{timer}_IRQHandler();CHECK(mock_calls==10);
''','All ten paper LED values, correct timer period, exact call count and stop')
    good='num_correct' if timer==0 else 'hit';bad='num_wrong' if timer==0 else 'miss';led=5 if timer==0 else 11
    fixture('2025-07-01_'+variant+'-Q3',stub,f'''
TIMER{timer}_IRQHandler();CHECK(waiting_for_move==1);mock_joy=expected_direction;RIT_IRQHandler();CHECK({good}==1&&waiting_for_move==0&&mock_led==0);
mock_joy=0;RIT_IRQHandler();mock_joy=EXAM_JOY_UP|EXAM_JOY_DOWN;RIT_IRQHandler();CHECK({bad}==0);
for(int i=1;i<10;i++){{TIMER{timer}_IRQHandler();mock_joy=0;RIT_IRQHandler();mock_joy=EXAM_JOY_UP|EXAM_JOY_DOWN;RIT_IRQHandler();}}
CHECK(mock_calls==10&&{bad}==9);TIMER{timer}_IRQHandler();CHECK(mock_led==(1u<<(11-{led}))&&!mock_running[{timer}]&&!mock_rit_running);
mock_joy=0;RIT_IRQHandler();mock_joy=EXAM_JOY_LEFT;RIT_IRQHandler();CHECK(mock_led==(1u<<(11-{led}))&&mock_calls==10);
''','First response only, nine wrong rounds, tenth full window, final score and post-game input ignored')
for variant,name,button,bit in [('ARM1','Look_and_Say',0,1),('ARM2','run_length_encoding',1,2)]:
    fixture('2026-02-03_'+variant+'-Q2',f'uint32_t {name}(uint32_t v){{mock_arg[0]=v;mock_calls++;return 0x1234;}}',f'''
mock_buttons={bit};review_step();CHECK(mock_calls==0);mock_adc_value=0x7b0;mock_adc_fresh=1;review_step();CHECK(mock_led==123);
EINT{button}_IRQHandler();CHECK(mock_arg[7]=={button});mock_buttons={bit};review_step();CHECK(mock_arg[0]==123&&mock_led==0x34);
mock_adc_fresh=1;review_step();CHECK(mock_led==0x34);mock_adc_value=0x7c0;mock_adc_fresh=1;review_step();CHECK(mock_led==124);
''','Fresh ADC high8, no pre-sample call, confirmed-button routing, low-byte result and hold-until-change; debounce API mocked')
fixture('2026-02-03_ARM3-Q2','void Recaman(uint32_t*a,uint8_t n){mock_calls++;mock_arg[0]=n;uint32_t v[4]={0,1,3,6};for(int i=0;i<n;i++)a[i]=i<4?v[i]:(uint32_t)i;}',r'''
mock_adc_value=0x40;mock_adc_fresh=1;review_step();mock_buttons=4;review_step();CHECK(mock_arg[0]==4&&mock_led==0&&display_index==1);
uint32_t expected[3]={1,3,6};for(int i=0;i<3;i++){TIMER0_IRQHandler();review_step();CHECK(mock_led==expected[i]);}CHECK(!mock_running[0]);
mock_adc_value=0;mock_adc_fresh=1;review_step();mock_buttons=4;review_step();CHECK(mock_led==0&&!sequence_active);
''','Immediate a0,2-second playback through final element, zero-length no read; sequence mocked')
for variant,name in [('ARM1','HofstadterQ'),('ARM2','HofstadterConway')]:
    fixture('2026-02-18_'+variant+'-Q2',f'uint32_t {name}(uint32_t*a,int n){{for(int i=0;i<n;i++)a[i]=100;return 100;}}',r'''
CHECK(mock_period[0]==50);TIMER0_IRQHandler();CHECK(sequence_index==1&&mock_period[1]==1062&&mock_period[2]==125000&&mock_mode[2]==EXAM_TIMER_ONE_SHOT);
TIMER0_IRQHandler();CHECK(sequence_index==1);TIMER1_IRQHandler();CHECK(mock_dac==410);TIMER1_IRQHandler();CHECK(mock_dac==467);
TIMER2_IRQHandler();CHECK(!mock_running[1]&&!mock_running[2]&&mock_dac==0);TIMER1_IRQHandler();CHECK(mock_dac==0);
sequence_index=999;TIMER0_IRQHandler();CHECK(sequence_index==1000&&!mock_running[0]);mock_running[1]=mock_running[2]=0;TIMER0_IRQHandler();CHECK(sequence_index==1000);
''','Threshold endpoints, B/C active guard, sine sample order, stop/silence, stale B and final A interrupts; sequence mocked')
for variant,name,scratch,direction in [('ARM1','BullsAndCows','guessFrequency','EXAM_JOY_DOWN'),('ARM2','Mastermind','usedGuess','EXAM_JOY_UP')]:
    fixture('2026-06-25_'+variant+'-Q2',f'int {name}(int*g,int*s,int*a,int*b){{mock_calls++;for(int i=0;i<4;i++)if(a[i]||b[i])mock_arg[6]=1;return (int)mock_return;}}',f'''
mock_counter[1]=0x00121ab6;
mock_joy=EXAM_JOY_SELECT;RIT_IRQHandler();review_step();CHECK(game_state==WAIT_START);
RIT_IRQHandler();RIT_IRQHandler();review_step();CHECK(game_state==EDIT_GUESS&&secret[0]==2&&secret[1]==3&&secret[2]==2&&secret[3]==1);
for(int j=0;j<2;j++){{mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_joy={direction};for(int k=0;k<3;k++)RIT_IRQHandler();review_step();}}
CHECK(guess[0]==2&&mock_led==2);for(int k=0;k<8;k++)RIT_IRQHandler();review_step();CHECK(guess[0]==2);
mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_return=0x13;mock_joy=EXAM_JOY_SELECT;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();CHECK(game_state==SHOW_RESULT&&mock_led==0x13&&!mock_arg[6]);
mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_joy=EXAM_JOY_SELECT;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();CHECK(game_state==EDIT_GUESS&&guess[0]==0&&secret[0]==2);
mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_return=0xf0;mock_joy=EXAM_JOY_SELECT|{direction};for(int k=0;k<3;k++)RIT_IRQHandler();review_step();CHECK(game_state==FINISHED&&mock_led==0xf0&&guess[0]==0);
mock_joy=0;for(int k=0;k<3;k++)RIT_IRQHandler();review_step();mock_joy={direction};for(int k=0;k<3;k++)RIT_IRQHandler();review_step();CHECK(game_state==FINISHED&&mock_led==0xf0);
''','Debounce/held select, nibble secret extraction, variant direction mapping, scratch cleared, next guess retains secret, SELECT priority and finished state ignores input; scorer mocked')

def bounded_main(text):
    text=text.replace('int main(void)','int answer_main(void)')
    start=text.index('int answer_main(void)')
    # The final main loop is the foreground step; preserve its actual statements.
    matches=list(re.finditer(r'(?:for\s*\(\s*;\s*;\s*\)|while\s*\(\s*1\s*\))\s*\{',text[start:]))
    if not matches:return text+'\nstatic void review_step(void){}\n'
    match=matches[-1];a=start+match.start();b=start+match.end();depth=1;i=b
    while depth:
        if text[i]=='{':depth+=1
        if text[i]=='}':depth-=1
        i+=1
    body=text[b:i-1].replace('continue;','return;')
    text=text[:a]+'return 0;'+text[i:]
    return text+'\nstatic void review_step(void){'+body+'}\n'
def main():
    results=json.loads((HERE/'QUESTION_PERIPHERAL_RESULTS.json').read_text()) if (HERE/'QUESTION_PERIPHERAL_RESULTS.json').exists() else {}
    for qid,(stub,checks,label) in FIXTURES.items():
        if len(sys.argv)>1 and qid not in sys.argv[1:]:continue
        r=REVIEWS[qid];paths=[ROOT/s for s in r['sources'] if s.endswith('.c')]
        mainfile=next(p for p in paths if p.name=='main.c')
        text=bounded_main(mainfile.read_text(encoding='utf-8-sig'))
        text+='\n'+'\n'.join(p.read_text(encoding='utf-8-sig') for p in paths if p!=mainfile)
        # Expose actual static helpers/state within the same test translation unit.
        fixture_text=MOCK+stub+'\n'+text+'\n__declspec(dllexport) int test_main(void){answer_main();'+checks+'return 0;}\n'
        c=OUT/(qid+'.c');dll=c.with_suffix('.dll');c.write_text(fixture_text)
        cmd=[CLANG,'-ffreestanding','-fno-builtin','-O0','-Wno-return-type','-shared','-nostdlib','-fuse-ld=lld','-Wl,/noentry','-I',API,'-I',OUT,c,'-o',dll]
        try:
            p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
            if p.returncode:raise RuntimeError(p.stdout+p.stderr)
            lib=ctypes.CDLL(str(dll));value=lib.test_main();assert value==0,f'C assertion failed at fixture line{value}'
            results[qid]={'status':'PASS','cases':[label],'sourceHashes':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'limits':'Actual C logic with mocked peripherals and separate algorithm implementations; no physical timing claim.'}
        except Exception as e:results[qid]={'status':'FAIL','error':str(e)}
        print(qid,results[qid]['status'],results[qid].get('error','')[-1600:],flush=True)
        (HERE/'QUESTION_PERIPHERAL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    (HERE/'QUESTION_PERIPHERAL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    return int(any(r['status']!='PASS' for r in results.values()))
if __name__=='__main__':raise SystemExit(main())
