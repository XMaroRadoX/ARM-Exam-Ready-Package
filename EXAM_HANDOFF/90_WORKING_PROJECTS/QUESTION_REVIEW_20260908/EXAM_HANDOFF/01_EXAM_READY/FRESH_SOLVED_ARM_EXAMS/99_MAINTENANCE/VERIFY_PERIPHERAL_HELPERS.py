"""Compile production peripheral sources, execute Thumb code with modeled MMIO.

Device headers are supplied externally; no fake native-build headers are used.
The model handles write-one-to-clear, NVIC set/clear and timer reset semantics.
It does not claim electrical, autonomous timing, or physical-board validation.
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess, sys
from VERIFY_ALGORITHMS import CLANG, LLD, RUNTIME

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / '01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/Source'
sys.path.insert(0, str(HERE / '.test-deps'))

def build(device, runtime):
    folder = HERE / '.peripheral-tests'; folder.mkdir(exist_ok=True)
    support = '''#include <stdint.h>
uint32_t SystemFrequency=100000000u;
void SystemInit(void) { SystemFrequency=100000000u; }
uint64_t __aeabi_uldivmod(uint64_t n, uint64_t d) {
  uint64_t q=0, r=0; unsigned i;
  if (!d) return 0;
  for(i=0;i<64;i++) { unsigned carry=(unsigned)(r>>63); r=(r<<1)|(n>>63); n<<=1; q<<=1; if(carry || r>=d) {r-=d; q|=1;} }
  return q;
}
'''
    (folder/'support.c').write_text(support+RUNTIME)
    flags=['--target=arm-none-eabi','-mcpu=cortex-m3','-mthumb','-O0','-ffreestanding','-fno-builtin','-D__ARMCC_VERSION=6100100']
    includes=[SOURCE, *[p for p in SOURCE.iterdir() if p.is_dir()], device, runtime]
    for p in includes: flags += ['-I',str(p)]
    files=[SOURCE/'exam_api/exam_api.c',SOURCE/'RIT/lib_RIT.c',SOURCE/'timer/lib_timer.c',SOURCE/'led/lib_led.c',SOURCE/'led/funct_led.c',SOURCE/'button_EXINT/lib_button.c',SOURCE/'systick/lib_systick.c',SOURCE/'joystick/lib_joystick.c',SOURCE/'adc/lib_adc.c',folder/'support.c']
    objects=[]
    for i,p in enumerate(files):
        obj=folder/f'{i}.o'; objects.append(obj)
        subprocess.run([str(CLANG),*flags,'-c',str(p),'-o',str(obj)],check=True,capture_output=True)
    elf=folder/'peripherals.elf'
    subprocess.run([str(LLD),'-Ttext=0x10000','--entry=exam_init',*[str(o) for o in objects],'-o',str(elf)],check=True,capture_output=True)
    return elf, {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_relative_to(ROOT) and p != folder/'support.c'}

class Board:
    timers=[0x40004000,0x40008000,0x40090000,0x40094000]
    rit=0x400B0000
    sc=0x400FC000
    def __init__(self,elf):
        from elftools.elf.elffile import ELFFile
        from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_MODE_MCLASS, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
        from unicorn.arm_const import UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PRIMASK
        self.regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
        self.sp,self.lr,self.pc,self.mask=UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_PRIMASK
        self.uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB|UC_MODE_MCLASS)
        for a,n in [(0,0x400000),(0x10000000,0x10000),(0x20000000,0x100000),(0x40000000,0x100000),(0xE000E000,0x2000)]:self.uc.mem_map(a,n)
        with elf.open('rb') as f:
            e=ELFFile(f)
            for seg in e.iter_segments():
                if seg['p_type']=='PT_LOAD':self.uc.mem_write(seg['p_vaddr'],seg.data())
            self.syms={s.name:s['st_value'] for s in e.get_section_by_name('.symtab').iter_symbols()}
        self.fixups=[]; self.writes=[]; self.called=set()
        self.mock_clock=False
        self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write,begin=0x40000000,end=0xFFFFFFFF)
        # Only ADGDR has a read side effect in this model. A global read hook
        # also interferes with conditional loads in optimized native images
        # in Unicorn 2.1.4; ordinary RAM/timer reads need no interception.
        self.uc.hook_add(UC_HOOK_MEM_READ,self.read,begin=0x40034004,end=0x40034007)
        self.uc.hook_add(UC_HOOK_CODE,self.step)
    def get(self,a):return int.from_bytes(self.uc.mem_read(a,4),'little')
    def put(self,a,v):self.uc.mem_write(a,(v&0xFFFFFFFF).to_bytes(4,'little'))
    def step(self,uc,a,size,user):
        while self.fixups:
            address,value=self.fixups.pop(0);self.put(address,value)
        if a==0x300000:uc.emu_stop()
        if self.mock_clock and a==(self.syms.get('SystemInit',1)&~1):
            if 'SystemFrequency' in self.syms:self.put(self.syms['SystemFrequency'],100000000)
            uc.reg_write(self.pc,uc.reg_read(self.lr))
    def read(self,uc,access,a,size,value,user):
        if a==0x40034004:self.fixups.append((a,self.get(a)&0x3FFFFFFF))
    def write(self,uc,access,a,size,value,user):
        if a>=0x40000000:self.writes.append((a,value))
        if a==0x40034000:self.fixups.append((0x40034004,self.get(0x40034004)&0x7FFFFFFF))
        if a in [t for t in self.timers]+[self.sc+0x140]:
            self.fixups.append((a,self.get(a)&~value))
        if a==self.rit+8:
            self.fixups.append((a,(value&0xE)|((self.get(a)&1)&~value)))
        for t in self.timers:
            if a==t+4 and value&2:self.fixups.extend([(t+8,0),(t+0x10,0)])
        for base,clear in [(0xE000E100,False),(0xE000E180,True),(0xE000E200,False),(0xE000E280,True)]:
            if base<=a<base+8:
                canonical=a-(0x80 if clear else 0)
                result=(self.get(canonical)&~value) if clear else (self.get(canonical)|value)
                self.fixups.extend([(canonical,result),(canonical+0x80,result)])
    def call(self,name,*args):
        self.called.add(name);self.writes=[]
        for reg,v in zip(self.regs,args):self.uc.reg_write(reg,v&0xFFFFFFFF)
        self.uc.reg_write(self.sp,0x20010000);self.uc.reg_write(self.lr,0x300001)
        self.uc.emu_start(self.syms[name]|1,0x300000,count=1000000)
        assert self.uc.reg_read(self.pc)==0x300000, name+' did not return'
        return self.uc.reg_read(self.regs[0])

def verify(b):
    n=0
    def check(condition):
        nonlocal n
        n+=1
        if not condition:raise AssertionError(f'check {n}')
    b.call('exam_init')
    for timer,t in enumerate(b.timers):
        check(b.call('exam_timer_set_prescaler',timer,1)==3)
        check(b.call('exam_timer_config_ticks',timer,1000,0)==0)
        for mask in (0,1):
            b.uc.reg_write(b.mask,mask)
            for channel in range(4):
                for action in range(8):
                    b.put(t+8,67); b.put(t+0x10,9); b.put(t+0x14,0xABC); b.put(t,0x3F)
                    others=[b.get(t+0x18+i*4) for i in range(4)]
                    check(b.call('exam_timer_config_match',timer,channel,333+channel,action)==0)
                    check(b.get(t+0x14)==((0xABC&~(7<<(channel*3)))|(action<<(channel*3))))
                    check(b.get(t)==(0x3F&~(1<<channel)))
                    check(b.get(t+8)==67 and b.get(t+0x10)==9 and b.get(t+4)==0)
                    check(b.uc.reg_read(b.mask)==mask)
                    for i in range(4):check(b.get(t+0x18+i*4)==(333+i if i==channel else others[i]))
            for pr in (0,24,0xFFFFFFFF):
                b.put(t+0x10,17)
                check(b.call('exam_timer_set_prescaler',timer,pr)==0)
                check(b.get(t+0xC)==pr and b.get(t+0x10)==0 and b.get(t+8)==67)
            clock=b.sc+(0x1A8 if timer<2 else 0x1AC);shift=[2,4,12,14][timer]
            for div,encoding in [(1,1),(2,2),(4,0),(8,3)]:
                b.put(clock,0xA55AA55A)
                check(b.call('exam_timer_set_clock_divider',timer,div)==0)
                check(b.get(clock)==((0xA55AA55A&~(3<<shift))|(encoding<<shift)))
                check(b.uc.reg_read(b.mask)==mask)
        b.uc.reg_write(b.mask,0)
        for tcr in (1,2,3):
            b.put(t+4,tcr)
            for name,args in [('exam_timer_config_match',(timer,2,99,7)),('exam_timer_set_prescaler',(timer,88)),('exam_timer_set_clock_divider',(timer,8))]:
                before=bytes(b.uc.mem_read(t,0x78)); check(b.call(name,*args)==3);check(bytes(b.uc.mem_read(t,0x78))==before)
        b.put(t+4,0)
        for name,args,status in [('exam_timer_config_match',(timer,4,99,1),1),('exam_timer_config_match',(timer,1,0,1),2),('exam_timer_config_match',(timer,1,99,8),1),('exam_timer_set_clock_divider',(timer,3),1),('exam_timer_config_ticks',(timer,0,0),2),('exam_timer_config_ticks',(timer,99,99),1)]:
            before=bytes(b.uc.mem_read(t,0x78));check(b.call(name,*args)==status);check(bytes(b.uc.mem_read(t,0x78))==before)
        b.put(t,0x35);check(b.call('exam_timer_ack',timer)==0x35);check(b.get(t)==0)
        b.put(t+8,123);b.put(t+0x10,4)
        b.call('exam_timer_start',timer);check(b.get(t+8)==123 and b.get(t+4)==1)
        b.call('exam_timer_stop',timer);check(b.get(t+8)==123 and b.get(t+4)==0)
        b.call('exam_timer_reset',timer);check(b.get(t+8)==0 and b.get(t+0x10)==0 and b.get(t+4)==0)
        for div in (1,2,4,8):
            b.call('exam_timer_set_clock_divider',timer,div)
            check(b.call('exam_timer_config_ms',timer,1,0)==0);check(b.get(t+0x18)==100000000//div//1000 and b.get(t+0xC)==0)
    for flags in range(64):
        for i in range(256):
            check(b.call('exam_timer_match_happened',flags,i)==int(i<4 and bool(flags&(1<<i))))
            check(not b.writes)
            check(b.call('exam_timer_capture_happened',flags,i)==int(i<2 and bool(flags&(1<<(i+4)))))
            check(not b.writes)
    for previous in range(32):
        for current in range(32):
            check(b.call('exam_joystick_released_edges',previous|0xFFFF0000,current)==(previous&~current&31))
            check(not b.writes)
    for stale in (False,True):
        b.put(b.rit+4,0xFFFFFFFF if stale else 0);b.put(b.rit+8,15 if stale else 0);b.put(b.rit+0xC,123)
        b.put(0xE000E200,1<<29)
        check(b.call('exam_rit_config_ticks',1234)==0)
        check(b.get(b.rit)==1234 and b.get(b.rit+4)==0 and b.get(b.rit+8)==6 and b.get(b.rit+0xC)==0)
        check(not(b.get(0xE000E200)&(1<<29)) and bool(b.get(0xE000E100)&(1<<29)))
        before=bytes(b.uc.mem_read(b.rit,16));check(b.call('exam_rit_config_ticks',0)==2);check(bytes(b.uc.mem_read(b.rit,16))==before)
        b.call('exam_rit_start');check(b.get(b.rit+8)&8)
        b.put(b.rit+0xC,54);b.call('exam_rit_reset');check(b.get(b.rit+0xC)==0 and b.get(b.rit+8)&8)
        b.call('exam_rit_stop');check(not(b.get(b.rit+8)&8))
    for mask in (0,1):
        b.uc.reg_write(b.mask,mask); b.call('exam_events_set',3);b.call('exam_events_set',1)
        check(b.call('exam_events_take',1)==1);check(b.call('exam_events_take',1)==0);check(b.call('exam_events_take',2)==2)
        check(b.uc.reg_read(b.mask)==mask)
    b.uc.reg_write(b.mask,0)
    b.call('exam_adc_init');out=0x20001000;b.put(out,0xDEADBEEF)
    check(b.call('exam_adc_take',out)==0 and b.get(out)==0xDEADBEEF)
    b.put(0x40034004,(4095<<4)|(1<<31));b.call('exam_adc_irq_capture')
    check(b.call('exam_adc_take',out)==1 and b.get(out)&65535==4095);check(b.call('exam_adc_take',out)==0)
    b.call('exam_dac_init');b.put(0x4008C000,1<<16)
    check(b.call('exam_dac_write',1023)==0 and b.get(0x4008C000)==((1<<16)|(1023<<6)))
    before=b.get(0x4008C000);check(b.call('exam_dac_write',1024)==2 and b.get(0x4008C000)==before)
    b.call('exam_buttons_init')
    gpio=0x2009C054
    b.put(gpio,0xFFFFFFFF)
    check(b.call('exam_debounce_config',10,50)==0)
    for button in range(3):
        b.put(gpio,0xFFFFFFFF & ~(1<<(10+button)))
        check(b.call('exam_debounce_begin',button)==0)
        for tick in range(4):b.call('exam_debounce_tick');check(b.call('exam_button_events_take')==0)
        b.call('exam_debounce_tick');check(b.call('exam_button_events_take')==(1<<button))
        for tick in range(20):b.call('exam_debounce_tick');check(b.call('exam_button_events_take')==0)
        b.put(gpio,0xFFFFFFFF);b.call('exam_debounce_tick')
        b.put(gpio,0xFFFFFFFF & ~(1<<(10+button)));b.call('exam_debounce_begin',button)
        for tick in range(5):b.call('exam_debounce_tick')
        check(b.call('exam_button_events_take')==(1<<button))
        b.put(gpio,0xFFFFFFFF);b.call('exam_debounce_tick')
    # Press bounce cancels the current attempt; a new EINT begins a fresh one.
    b.put(gpio,0xFFFFFBFF);b.call('exam_debounce_begin',0);b.call('exam_debounce_tick')
    b.put(gpio,0xFFFFFFFF);b.call('exam_debounce_tick');check(b.call('exam_button_events_take')==0)
    b.put(gpio,0xFFFFE3FF)
    for button in range(3):b.call('exam_debounce_begin',button)
    for tick in range(5):b.call('exam_debounce_tick')
    check(b.call('exam_button_events_take')==7)
    check(b.call('exam_debounce_config',20,40)==0)
    for tick in range(5):b.call('exam_debounce_tick')
    check(b.call('exam_button_events_take')==0)
    for timer,t in enumerate(b.timers):
        b.put(t+4,0);power=b.get(b.sc+0xC4);b.put(b.sc+0xC4,power&~(1<<[1,2,22,23][timer]))
        check(b.call('exam_timer_set_prescaler',timer,9)==3)
        b.put(b.sc+0xC4,power)
    for bad in (4,255,0xFFFFFFFF):
        check(b.call('exam_timer_config_match',bad,0,1,0)==1)
        check(b.call('exam_timer_set_prescaler',bad,0)==1)
        check(b.call('exam_timer_set_clock_divider',bad,4)==1)
    return n

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--device-include',type=Path,required=True);ap.add_argument('--runtime-include',type=Path,required=True);args=ap.parse_args()
    try:
        elf,hashes=build(args.device_include,args.runtime_include);b=Board(elf);checks=verify(b)
    except subprocess.CalledProcessError as exc:
        print(exc.stdout.decode(errors='replace'));print(exc.stderr.decode(errors='replace'));raise
    report=dict(status='PASS',checks=checks,executed_exports=sorted(b.called),sources=hashes,method='Production C compiled by LLVM for Cortex-M3; simulated MMIO with W1C, NVIC set/clear and counter reset semantics',nativeKeil='Reported separately',physicalBoard='Not tested')
    (HERE/'PERIPHERAL_HELPER_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='sources'},indent=2))
if __name__=='__main__':main()
