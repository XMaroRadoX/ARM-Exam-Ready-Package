"""Check actual generated controller C, project/source agreement and coverage."""
from pathlib import Path
import ctypes,hashlib,html,json,re,subprocess
from itertools import combinations
from scenario_library import FAMILIES,practice_specs
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
PORTAL=ROOT/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL'
FIELDS='ticks elapsed value samples sum minimum maximum mean alarm running phase digit_count entered result previous_buttons previous_joy held repeat deadline'.split()
class State(ctypes.Structure):
    _fields_=[(s,ctypes.c_uint32) for s in FIELDS]+[('history',ctypes.c_uint32*8)]+[(s,ctypes.c_uint32) for s in 'cursor filled output amplitude period'.split()]

def behavior(dll,mode):
    reset=dll.controller_reset;step=dll.controller_step
    step.argtypes=[ctypes.c_uint32]*4
    state=dll.state;checks=0
    def check(ok,message):
        nonlocal checks
        checks+=1
        if not ok:raise AssertionError(message)
    def tick(b=0,j=0,adc=None,n=1):
        for _ in range(n):step(b,j,adc is not None,adc or 0)
    def press(b=0,j=0):tick(b,j);tick()
    reset();check(state.minimum==4095 and state.samples==0,'Reset measurements')
    tick(adc=99999);check(state.maximum==4095 and state.amplitude==1023,'Clamp ADC before arithmetic')
    tick(7,31);check(state.value==0 and state.samples==0,'Simultaneous reset wins')
    reset()
    if mode==0:
        tick(adc=4095);check(state.value==255,'Monitor ADC scale')
        press(1);check(state.running==0,'Pause');press(1);check(state.running==1,'Resume')
    elif mode==1:
        press(1);press(1);check(state.value==2,'Counter two presses')
        tick(1,n=20);check(state.value==3,'Held input one edge');tick();press(2);check(state.value==2,'Decrement')
    elif mode==2:
        for one in [1,0,0,1,1,0]:press(0,16) if one else press(2)
        press(1);check(state.result==38,'Ordered binary identity')
        for _ in range(40):press(0,16)
        check(state.digit_count==32,'Bounded shift count')
    elif mode==3:
        tick(1,n=150);check(state.value==5,'Single long action');tick();check(state.value==7,'Release action')
    elif mode==4:
        tick(n=100);check(state.value==1,'One second');press(1);before=state.elapsed;tick(n=100);check(state.elapsed==before,'Pause excludes ticks')
    elif mode==5:
        tick(n=400);check(state.deadline==0 and state.alarm==1,'Timeout saturation')
    elif mode==6:
        tick(1);tick(n=99);check(state.phase==2,'Open reaction window');tick(n=7);tick(2);check(state.result==7,'Reaction duration')
        reset();tick(1);tick(2);check(state.phase==4 and state.result==255,'False start')
    elif mode==7:
        tick(j=8);check(state.value==1,'Right edge');tick(j=8,n=49);check(state.value==2,'Initial repeat delay');tick(j=8,n=200);check(state.value==7,'Right bound');tick();tick(j=4,n=200);check(state.value==0,'Left bound')
    elif mode==8:
        for j in [8,4,8,4]:press(j=j)
        press(j=1);check(state.result==1,'Exact code accepted');press(j=1);check(state.result==0,'Empty code rejected')
    elif mode==9:
        for adc,value in [(0,0),(2048,50),(4095,100)]:tick(adc=adc);check(state.value==value,'Rounded percent')
    elif mode==10:
        for adc,value in [(3000,1),(2500,1),(2000,0),(2500,0)]:tick(adc=adc);check(state.alarm==value,'Hysteresis retains state')
    elif mode==11:
        tick(adc=4095,n=8);check(state.mean==4095,'Window fill');tick(adc=0);check(state.mean==3583 and state.value==223,'Oldest sample evicted')
    elif mode==12:
        tick(adc=2048);press(1);tick(adc=4095);check(state.result==2048,'Captured result persists')
    elif mode==13:
        tick(adc=0,n=5);check(state.value==255 and state.period==5,'Short interval');tick(adc=4095);check(state.period==100,'Long interval bound')
    elif mode==14:
        check(state.running==0,'Burst initially silent');tick(1);tick(n=19);check(state.running==0,'Finite burst');tick(1);check(state.running==1,'Retrigger after completion')
    elif mode==15:
        tick(j=8,n=10);check(state.phase==1,'No repeated waveform edge');press(1);check(state.running==0,'Pause waveform')
    elif mode==16:
        tick(n=20);check(state.running==0,'Inter-note silence');tick(n=10);check(state.running==1 and state.phase==1,'Next note');tick(n=60);check(state.phase==0,'Three-note cycle')
    elif mode==17:
        tick(adc=1000);tick(adc=3000);check(state.minimum==1000 and state.maximum==3000,'Extrema');press(1);check(state.value==187,'Maximum selection')
    tick(4);check(state.samples==0 and state.value==0,'Restart clears persistent state')
    return checks

def main():
    records=json.loads((HERE/'SCENARIO_MANIFEST.json').read_text());matrix=json.loads((HERE/'PERIPHERAL_COMBINATIONS.json').read_text())
    results=[];issues=[];checks=0;folder=HERE/'.scenario-tests';folder.mkdir(exist_ok=True)
    expected={tuple(s) for n in range(2,9) for s in combinations(FAMILIES,n)}
    assert {tuple(r['features']) for r in matrix}==expected
    assert len({r['scenario'] for r in matrix})==247
    specs=practice_specs()
    # Compile every distinct generated controller configuration, not a separate
    # handwritten substitute. DLLs are local disposable test artifacts.
    for i,r in enumerate(records):
        project=ROOT/r['path'];page=PORTAL/r['route']
        try:
            text=page.read_text(encoding='utf-8')
            listings=[html.unescape(re.sub('<[^>]+>','',s)).strip() for s in re.findall(r'<code\b[^>]*>(.*?)</code>',text,re.S)]
            for name,digest in r['files'].items():
                f=project/name
                assert hashlib.sha256(f.read_bytes()).hexdigest()==digest,(r['id'],name,'hash')
                assert f.read_text(encoding='utf-8').strip() in listings,(r['id'],name,'listing')
                checks+=2
            if r['id'] in specs:
                lib=folder/(r['id']+'.exe')
                bridge=folder/(r['id']+'-bridge.c')
                source=(project/'Source/sample.c').read_text(encoding='utf-8')
                bridge.write_text('#define SCENARIO_TEST\n'+source+BRIDGE,encoding='utf-8')
                proc=subprocess.run(['C:/MinGW/bin/gcc.exe','-O0',str(bridge),'-o',str(lib)],capture_output=True,text=True)
                if proc.returncode:raise AssertionError(proc.stderr)
                runner=Runner(lib)
                try:checks+=behavior(runner,r['mode'])
                finally:runner.close()
                results.append({'project':r['id'],'status':'PASS','method':'Generated controller C executed with explicit input sequences','sourceHash':r['files']['Source/sample.c']})
            else:
                results.append({'project':r['id'],'status':'SOURCE_AGREEMENT_PASS','method':'Exact maintained historical sources; native and hardware-flow evidence reported separately'})
        except Exception as e:issues.append(r['id']+': '+str(e));results.append({'project':r['id'],'status':'FAIL','reason':str(e)})
        if (i+1)%25==0:print(i+1,len(records),'checked;',len(issues),'issues',flush=True)
    destinations=json.loads((HERE/'SECTION_DESTINATIONS.json').read_text())
    index=(PORTAL/'patterns/index.html').read_text()
    for title,d in destinations.items():
        if d['section']!='Solution Patterns':assert 'patterns/'+Path(d['route']).name not in index
    report={'status':'PASS' if not issues else 'FAIL','scenarios':len(records),'combinations':len(matrix),'checks':checks,'results':results,'issues':issues,'physicalBoard':'Not tested','limits':'Controller tests do not model analog signals, NVIC arbitration or electrical bounce. Native build results are separate.'}
    (HERE/'SCENARIO_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],checks,'checks',len(issues),'issues');print('\n'.join(issues[:20]))
    return bool(issues)
BRIDGE=r'''
#include <stdio.h>
#include <io.h>
#include <fcntl.h>
int main(void) {
  char command;unsigned b,j,v,a;
  _setmode(_fileno(stdout),_O_BINARY);
  while(scanf(" %c",&command)==1) {
    if(command=='q')break;
    if(command=='r')controller_reset();
    else if(scanf("%u %u %u %u",&b,&j,&v,&a)==4)controller_step(b,j,v,a);
    else return 2;
    fwrite(&app,sizeof(app),1,stdout);fflush(stdout);
  }
  return 0;
}
'''
class Runner:
    def __init__(self,path):
        self.process=subprocess.Popen([str(path)],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        self.state=State()
        self.controller_reset=lambda:self.command('r')
        self.controller_step=lambda b,j,v,a:self.command(f's {b} {j} {int(v)} {a}')
    def command(self,line):
        self.process.stdin.write((line+'\n').encode());self.process.stdin.flush()
        data=self.process.stdout.read(ctypes.sizeof(State))
        if len(data)!=ctypes.sizeof(State):raise AssertionError('Controller process terminated')
        ctypes.memmove(ctypes.addressof(self.state),data,len(data))
    def close(self):
        self.process.stdin.write(b'q\n');self.process.stdin.flush();self.process.wait(timeout=5)
        self.process.stdin.close();self.process.stdout.close()
if __name__=='__main__':raise SystemExit(main())
