"""Exercise complete native example images with explicit peripheral inputs.

Interrupt entry is driven by the test; PLL startup and passage of real time
are outside the model. Production main/handler/algorithm code is executed.
"""
import json
from pathlib import Path
from VERIFY_PERIPHERAL_HELPERS import Board, HERE, ROOT
OUT=ROOT/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects'

class Example(Board):
    def __init__(self,key):
        super().__init__(HERE/'.pattern-flow-images'/(key+'.axf'))
        self.put(0x2009C034,0xFFFFFFFF);self.put(0x2009C054,0xFFFFFFFF)
        self.uc.reg_write(self.sp,0x20018000);self.uc.reg_write(self.lr,0x300001)
        self.uc.emu_start(self.syms.get('__main',self.syms['main'])|1,0x300000,count=300000)
        self.foreground=self.uc.context_save()
    def irq(self,name,flag=None):
        if flag is not None:self.put(flag,(self.get(flag)|1) if flag==self.rit+8 else 1)
        self.call(name)
    def resume(self):
        self.uc.context_restore(self.foreground)
        self.uc.emu_start(self.uc.reg_read(self.pc)|1,0x300002,count=6000)
        self.foreground=self.uc.context_save()
    def var(self,name,width=4):return int.from_bytes(self.uc.mem_read(self.syms[name],width),'little')
    def joy(self,value):
        self.put(0x2009C034,(0xFFFFFFFF & ~(31<<25)) | ((~value&31)<<25))
        self.irq('RIT_IRQHandler',self.rit+8)
        self.resume()

def main():
    results=[]
    def run(key,test):
        try:
            b=Example(key);test(b);result=dict(project=key,status='PASS')
        except Exception as exc:result=dict(project=key,status='FAIL',reason=str(exc))
        results.append(result);print(result,flush=True)
    def timer(b):
        for i in range(3):b.irq('TIMER0_IRQHandler',b.timers[0])
        assert b.var('tick_count')==3
    run('timer-periodic',timer)
    run('timer-exact-ticks',timer)
    def one_shot(b):
        # Model hardware match reset/stop before entering the IRQ.
        mcr=b.get(b.timers[0]+0x14);assert mcr&7==7
        b.put(b.timers[0]+8,0);b.put(b.timers[0]+0x10,0);b.put(b.timers[0]+4,0)
        b.irq('TIMER0_IRQHandler',b.timers[0]);assert b.var('tick_count')==1 and b.get(b.timers[0]+4)==0
    run('timer-one-shot',one_shot)
    def pause(b):
        b.put(b.timers[0]+8,23);b.put(b.timers[0]+0x10,9)
        b.irq('EINT0_IRQHandler');assert b.get(b.timers[0]+4)==0 and b.get(b.timers[0]+8)==23
        b.irq('EINT1_IRQHandler');assert b.get(b.timers[0]+4)==1 and b.get(b.timers[0]+8)==23
        b.irq('EINT2_IRQHandler');assert b.get(b.timers[0]+4)==1 and b.get(b.timers[0]+8)==0 and b.get(b.timers[0]+0x10)==0
    run('timer-pause-resume',pause)
    def multi(b):
        assert b.get(b.timers[0]+12)==24
        b.put(b.timers[0],15);b.irq('TIMER0_IRQHandler')
        assert [b.get(b.syms['matches']+4*i) for i in range(4)]==[1,1,1,1] and b.get(b.timers[0])==0
    run('timer-multiple-matches',multi)
    def capture(b):
        assert (b.get(0x4002C00C)>>20)&3==3 and b.get(b.timers[0]+0x28)==5
        b.put(b.timers[0]+0x2C,321);b.put(b.timers[0],16);b.irq('TIMER0_IRQHandler')
        assert b.var('last_capture')==321 and b.get(b.timers[0])==0
    run('timer-capture-pin',capture)
    def event(b):
        for i in range(3):b.irq('TIMER0_IRQHandler',b.timers[0])
        b.resume();assert b.var('consumed')==1
    run('event-handoff',event)
    def raw(b):
        b.put(b.timers[1]+8,37);b.irq('EINT0_IRQHandler');assert b.var('captured')==37
    run('raw-capture-ff',raw);run('raw-capture-ffff',raw)
    def binary(b):
        for bit in (1,0,0,1,1,0):b.irq('EINT2_IRQHandler' if bit else 'EINT1_IRQHandler')
        b.irq('EINT0_IRQHandler');assert b.var('result')==38 and b.var('bit_count')==0
    run('ordered-binary',binary)
    def parameters(b):
        b.irq('EINT1_IRQHandler');b.irq('EINT2_IRQHandler')
        assert b.var('increment')==3 and b.var('offset')==2 and b.var('result')==32 and b.var('step')==0
    run('ordered-parameters',parameters)
    def adc(b):
        b.irq('EINT0_IRQHandler');assert b.var('sequence_active',1)==0
        b.put(0x40034004,(4095<<4)|(1<<31));b.irq('ADC_IRQHandler');b.irq('EINT0_IRQHandler')
        assert b.var('captured',2)==4095 and b.var('processed')==255
        b.put(0x40034004,1<<31);b.irq('ADC_IRQHandler')
        assert b.var('captured',2)==4095
        for i in range(4):b.irq('TIMER0_IRQHandler',b.timers[0])
        assert b.var('sequence_active',1)==0 and b.get(b.timers[0]+4)==0
    run('adc-button-sequence',adc)
    def percentage(b):
        for value,expected in [(0,0),(2048,50),(4095,100)]:
            b.put(0x40034004,(value<<4)|(1<<31));b.irq('ADC_IRQHandler');b.irq('EINT0_IRQHandler')
            assert b.var('processed')==expected
            for i in range(4):b.irq('TIMER0_IRQHandler',b.timers[0])
    run('adc-percentage',percentage)
    def release(b):
        b.joy(1);assert b.var('pressed')==1 and b.var('released')==0
        b.joy(1);assert b.var('pressed')==0 and b.var('released')==0
        b.joy(0);assert b.var('released')==1 and b.var('held')==0
        b.joy(6);b.joy(10);assert b.var('pressed')==8 and b.var('released')==4
    run('joystick-release',release)
    def buttons(b,systick=False):
        b.put(0x2009C054,0xFFFFFBFF);b.irq('EINT0_IRQHandler')
        for i in range(5):b.irq('SysTick_Handler' if systick else 'RIT_IRQHandler')
        assert b.var('count',1)==1
        for i in range(20):b.irq('SysTick_Handler' if systick else 'RIT_IRQHandler')
        assert b.var('count',1)==1
    run('buttons-rit-timer',buttons);run('buttons-systick-timer',lambda b:buttons(b,True))
    def dac(b):
        for i in range(8):b.irq('TIMER0_IRQHandler',b.timers[0])
        assert b.var('completed')==1 and b.var('sample_index')==0
        assert (b.get(0x4008C000)>>6)&1023==256
    run('dac-stream',dac)
    def duration(b):
        dac(b);b.irq('TIMER1_IRQHandler',b.timers[1])
        assert b.get(b.timers[0]+4)==0 and ((b.get(0x4008C000)>>6)&1023)==512
    run('dac-duration',duration)
    def once(b):
        assert b.get(b.timers[0]+4)==0
        b.irq('EINT0_IRQHandler');b.irq('TIMER0_IRQHandler',b.timers[0]);b.irq('EINT0_IRQHandler');assert b.var('sample_index')==1
        for i in range(7):b.irq('TIMER0_IRQHandler',b.timers[0])
        assert b.var('completed')==1 and b.get(b.timers[0]+4)==0
        b.irq('EINT0_IRQHandler');assert b.var('sample_index')==0 and b.var('completed')==0
    run('dac-button-once',once)
    def game(b):
        b.put(b.timers[1]+8,0x1111);b.joy(1);b.joy(0)
        assert b.var('game_state',1)==1
        secret=bytes(b.uc.mem_read(b.syms['secret'],16))
        # A zero guess cannot win against four ones; show then start a new round.
        b.joy(1);b.joy(0);assert b.var('game_state',1)==2
        b.joy(1);b.joy(0);assert b.var('game_state',1)==1
        assert bytes(b.uc.mem_read(b.syms['secret'],16))==secret
        for direction in (2,4,8,16):b.joy(direction);b.joy(0)
        b.joy(1);assert b.var('game_state',1)==3
    run('game-bulls-cows',game);run('game-mastermind',game)
    def rhythm(b):
        b.irq('TIMER0_IRQHandler',b.timers[0]);expected=b.var('expected_direction')
        b.joy(expected);assert b.var('num_correct')==1
        b.joy(0);b.joy(31);assert b.var('num_correct')==1 and b.var('num_wrong')==0
    run('rhythm-first-movement',rhythm)
    def notes(b):
        b.irq('TIMER0_IRQHandler',b.timers[0]);index=b.var('sequence_index')
        assert index==1 and b.get(b.timers[1]+4)==1 and b.get(b.timers[2]+4)==1
        b.irq('TIMER0_IRQHandler',b.timers[0]);assert b.var('sequence_index')==index
        for i in range(45):b.irq('TIMER1_IRQHandler',b.timers[1])
        assert b.var('sample_index')==44
        b.irq('TIMER2_IRQHandler',b.timers[2]);assert b.get(b.timers[1]+4)==0
    run('dac-three-timer-notes',notes)
    try:
        from unicorn import UC_HOOK_CODE
        from unicorn.arm_const import UC_ARM_REG_MSP,UC_ARM_REG_PSP
        b=Board(HERE/'.pattern-flow-images/svc-frame.axf')
        for exc,expected in [(0xFFFFFFF9,0x20018000),(0xFFFFFFFD,0x20017000)]:
            b.uc.reg_write(UC_ARM_REG_MSP,0x20018000);b.uc.reg_write(UC_ARM_REG_PSP,0x20017000)
            b.uc.reg_write(b.lr,exc)
            def stop_at_decoder(uc,address,size,user):
                if address==(b.syms['exam_svc_capture_from_exception']&~1):uc.emu_stop()
            h=b.uc.hook_add(UC_HOOK_CODE,stop_at_decoder)
            b.uc.emu_start(b.syms['SVC_Handler']|1,0,count=100)
            assert b.uc.reg_read(b.regs[0])==expected
            b.uc.hook_del(h)
        frame=0x20016000;b.uc.mem_write(0x80000,bytes([7,0xDF]));b.put(frame+24,0x80002)
        b.call('exam_svc_capture_from_exception',frame)
        assert b.get(b.syms['svc_result'])==7 and b.get(frame)==8
        results.append(dict(project='svc-frame',status='PASS',checks='Actual wrapper MSP/PSP selection and native C decoder/dispatcher; hardware entry/return not modeled'))
    except Exception as exc:results.append(dict(project='svc-frame',status='FAIL',reason=str(exc)))
    report=dict(method='Production C compiled at O0 with native Arm Compiler and native assembly; explicit IRQs and modeled MMIO; SystemInit substituted with100MHz clock. Normal Keil project builds verified separately.',results=results,physicalBoard='Not tested',exceptionEntry='SVC hardware entry not modeled; native wrapper build checked separately')
    (HERE/'PATTERN_FLOW_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    return int(any(r['status']=='FAIL' for r in results))
if __name__=='__main__':raise SystemExit(main())
