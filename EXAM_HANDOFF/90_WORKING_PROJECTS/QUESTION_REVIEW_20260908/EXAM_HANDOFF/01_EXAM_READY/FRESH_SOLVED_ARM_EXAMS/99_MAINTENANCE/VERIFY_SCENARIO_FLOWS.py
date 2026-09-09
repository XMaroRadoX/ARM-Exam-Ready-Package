"""Explicit input/IRQ flows through the native complete application images."""
import ctypes,hashlib,json
from VERIFY_PERIPHERAL_HELPERS import Board,HERE,ROOT
from VERIFY_SCENARIOS import State
OUT=ROOT/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects'
class Application(Board):
    def __init__(self,key):
        super().__init__(OUT/key/'Objects/sample.axf');self.mock_clock=True
        self.put(0x2009C034,0xFFFFFFFF);self.put(0x2009C054,0xFFFFFFFF)
        self.uc.reg_write(self.sp,0x20018000);self.uc.reg_write(self.lr,0x300001)
        self.uc.emu_start(self.syms['main']|1,0x300000,count=100000)
        self.foreground=self.uc.context_save()
    def resume(self):
        self.uc.context_restore(self.foreground)
        self.uc.emu_start(self.uc.reg_read(self.pc)|1,0x300002,count=60000)
        self.foreground=self.uc.context_save()
    def var(self,name):return self.get(self.syms[name])
    def state(self):return State.from_buffer_copy(bytes(self.uc.mem_read(self.syms['app'],ctypes.sizeof(State))))
    def tick(self,n=1):
        for _ in range(n):
            self.put(self.rit+8,self.get(self.rit+8)|1);self.call('RIT_IRQHandler');self.resume()
    def buttons(self,mask):self.put(0x2009C054,0xFFFFFFFF^(mask<<10))
    def adc(self,value):self.put(0x40034004,(1<<31)|(value<<4));self.call('ADC_IRQHandler')
    def timer(self,n):self.put(self.timers[n],1);self.call('TIMER'+str(n)+'_IRQHandler')

def main():
    results=[]
    def run(key,fn):
        try:
            count=fn(key);result=dict(project=key,status='PASS',checks=count,imageSha256=hashlib.sha256((OUT/key/'Objects/sample.axf').read_bytes()).hexdigest())
        except Exception as e:result=dict(project=key,status='FAIL',reason=str(e))
        results.append(result);print(result,flush=True)
    def monitor(key):
        b=Application(key);checks=0
        def check(ok):
            nonlocal checks
            checks+=1
            if not ok:raise AssertionError('Monitor flow check '+str(checks))
        check(b.state().running==1)
        # A one-sample bounce followed by release must not act.
        b.buttons(1);b.tick();b.buttons(0);b.tick();check(b.state().running==1)
        b.buttons(1);b.tick(4);check(b.state().running==1)
        b.tick();check(b.state().running==0)
        b.tick(10);check(b.state().running==0)
        b.buttons(0);b.tick(5);b.buttons(1);b.tick(5);check(b.state().running==1)
        b.adc(4095);b.tick();check(b.state().value==255 and b.state().amplitude==1023)
        expected=[512,874,1023,874,512,150,0,150]
        for value in expected:
            b.timer(1);check(((b.get(0x4008C000)>>6)&1023)==value)
        b.timer(0);check(b.var('output_ticks')==1)
        b.call('SysTick_Handler');check(b.var('supervisor_ticks')==1)
        b.buttons(0);b.tick(5);b.buttons(1);b.tick(5);b.timer(1);check(b.get(0x4008C000)==0)
        b=Application(key)
        for _ in range(40):b.put(b.rit+8,b.get(b.rit+8)|1);b.call('RIT_IRQHandler')
        check(b.var('lost_inputs')==9)
        b.resume();check(b.var('head')==b.var('tail') and b.state().ticks==31)
        return checks
    run('mix-led-buttons-joystick-timer-rit-systick-adc-dac',monitor)
    def polling(key):
        b=Application(key)
        b.buttons(1);b.tick(5);assert b.state().value==1
        b.tick(30);assert b.state().value==1
        b.buttons(0);b.tick(5);b.buttons(1);b.tick(5);assert b.state().value==2
        b.buttons(7);b.tick(5);assert b.state().value==0
        return 4
    run('task-counter-polling',polling)
    def maze(key):
        b=Board(OUT/key/'Objects/sample.axf')
        data=bytearray(255 if r in (0,5) or c in (0,4) else 0 for r in range(6) for c in range(5))
        b.uc.mem_write(b.syms['maze'],bytes(data));b.call('depthFirstSearch',b.syms['maze'],6,5,7)
        data=bytes(b.uc.mem_read(b.syms['maze'],30));checks=0
        for r in range(1,5):
            for c in range(1,4):
                v=data[r*5+c];assert v&1;checks+=1
                for bit,dr,dc,back in [(2,0,1,8),(4,1,0,16),(8,0,-1,2),(16,-1,0,4)]:
                    if v&bit:
                        assert 1<=r+dr<5 and 1<=c+dc<4
                        assert data[(r+dr)*5+c+dc]&back;checks+=2
        # Substitute physical drawing only; execute native movement and bounds.
        from unicorn import UC_HOOK_CODE
        def draw(uc,a,size,user):uc.reg_write(b.pc,uc.reg_read(b.lr))
        addr=b.syms['draw_position']&~1;b.uc.hook_add(UC_HOOK_CODE,draw,begin=addr,end=addr)
        b.put(b.syms['current_row'],1);b.put(b.syms['current_column'],2)
        b.uc.mem_write(b.syms['maze']+7,b'\x02')
        assert b.call('move_player',8)==1 and b.get(b.syms['current_column'])==3;checks+=1
        b.uc.mem_write(b.syms['maze']+8,b'\x02')
        assert b.call('move_player',8)==0 and b.get(b.syms['current_column'])==3;checks+=1
        return checks
    run('paper-lcd-maze',maze)
    report=dict(status='PASS' if all(r['status']=='PASS' for r in results) else 'FAIL',results=results,method='Actual native complete images; input registers and IRQ calls driven explicitly; physical LCD drawing stubbed only in movement test',physicalBoard='Not tested',limitations='No automatic interrupt arbitration, electrical bounce, real-time passage or analog quality model.')
    (HERE/'SCENARIO_FLOW_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    return report['status']!='PASS'
if __name__=='__main__':raise SystemExit(main())
