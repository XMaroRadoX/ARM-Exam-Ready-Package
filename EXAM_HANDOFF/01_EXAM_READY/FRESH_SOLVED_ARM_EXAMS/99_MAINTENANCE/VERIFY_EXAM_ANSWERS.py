"""Check ARMASM syntax and execute translated instruction streams against independent paper-derived cases.

Requires installed Arm assembler, LLVM linker, pyelftools and Unicorn. No physical
interrupt, timing or board claim is made by instruction-stream execution.
"""
from pathlib import Path
import collections, hashlib, itertools, json, random, re, struct, subprocess, sys
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT.parents[1]/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/.test-deps'))
# The normal checkout already owns the shared test dependency directory.
for parent in [ROOT, *ROOT.parents]:
    deps=parent/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/.test-deps'
    if deps.exists():sys.path.insert(0,str(deps));break
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_MODE_MCLASS, UC_HOOK_CODE
from unicorn.arm_const import *
BIN=Path('C:/Users/marwa/AppData/Local/Keil_v5/ARM/ARMCLANG/bin')
LLD=Path('C:/Program Files/LLVM/bin/ld.lld.exe')
BUILD=HERE/'.question-tests'; BUILD.mkdir(exist_ok=True)
REVIEWS=json.loads((HERE/'QUESTION_REVIEWS.json').read_text(encoding='utf-8'))
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
SP=0x201F0000; STOP=0x20000F00; DATA=0x20080000
def run(args):
    p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    return p.stdout+p.stderr
class Machine:
    def __init__(self,path):
        self.path=path; self.cases=[]
        key=hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        obj=BUILD/(key+'.o');elf=BUILD/(key+'.elf')
        run([BIN/'armasm.exe','--cpu','Cortex-M3','--diag_suppress=A1950W',path,'-o',obj.with_suffix('.native.o')])
        from VERIFY_ALGORITHMS import gas
        asm=BUILD/(key+'.s');asm.write_text(gas(path.read_text()))
        run([LLD.with_name('clang.exe'),'--target=arm-none-eabi','-mcpu=cortex-m3','-mthumb','-c',asm,'-o',obj])
        first=re.findall(r'(?m)^\s*EXPORT\s+(\w+)',path.read_text())[0]
        run([LLD,'-Ttext=0x10000','-Tdata=0x20000000','--entry='+first,'--unresolved-symbols=ignore-all',obj,'-o',elf])
        self.uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB|UC_MODE_MCLASS)
        self.uc.mem_map(0x10000,0x200000);self.uc.mem_map(0x20000000,0x200000);self.uc.mem_map(0xE000E000,0x2000)
        with elf.open('rb') as f:
            e=ELFFile(f)
            for seg in e.iter_segments():
                if seg['p_type']=='PT_LOAD':
                    assert seg['p_vaddr']+seg['p_memsz']<=DATA or seg['p_vaddr']>=DATA+0x10000,'fixture buffer overlaps delivered image'
                    self.uc.mem_write(seg['p_vaddr'],seg.data())
            self.symbols={s.name:s['st_value'] for s in e.get_section_by_name('.symtab').iter_symbols()}
        exports=re.findall(r'(?m)^\s*EXPORT\s+(\w+)',path.read_text())
        addresses={self.symbols[n]&~1 for n in exports if n not in ('Reset_Handler','SVC_Handler')}
        def aligned(uc,address,size,data):
            if address in addresses:assert uc.reg_read(UC_ARM_REG_SP)%8==0,'unaligned public call'
        self.uc.hook_add(UC_HOOK_CODE,aligned)
    def write(self,a,values,words=False):self.uc.mem_write(a,struct.pack('<'+'I'*len(values),*[v&0xffffffff for v in values]) if words else bytes(v&255 for v in values))
    def read(self,a,n,words=False):return list(struct.unpack('<'+'I'*n,self.uc.mem_read(a,n*4))) if words else list(self.uc.mem_read(a,n))
    def call(self,name,args=(),except_regs=(),limit=10000000):
        u=self.uc;u.reg_write(UC_ARM_REG_SP,SP);u.reg_write(UC_ARM_REG_LR,STOP|1)
        for i,r in enumerate(SAVED):u.reg_write(r,0x41410000+i)
        for r,x in zip(REGS,args):u.reg_write(r,x&0xffffffff)
        for i,x in enumerate(args[4:]):self.write(SP+4*i,[x],True)
        u.emu_start(self.symbols[name]|1,STOP,count=limit)
        assert u.reg_read(UC_ARM_REG_PC)==STOP,(name,'did not terminate')
        assert u.reg_read(UC_ARM_REG_SP)==SP,(name,'SP changed')
        for i,r in enumerate(SAVED):
            if r not in except_regs:assert u.reg_read(r)==0x41410000+i,(name,'saved register changed',r)
        return u.reg_read(UC_ARM_REG_R0)
    def check(self,label,fn):
        fn();self.cases.append(label)

def reference_digits(n,swap=False):
    groups=[(len(list(g)),int(d)) for d,g in itertools.groupby(str(n))]
    return int(''.join(str(d)+str(c) if swap else str(c)+str(d) for c,d in groups))
def signed(v):return v-(1<<32) if v&(1<<31) else v
def trunc(n,d):return (-1 if (n<0)!=(d<0) else 1)*(abs(n)//abs(d))
def expect(a,b):assert a==b,(a,b)
def matrix_product(a,b):return [__import__('functools').reduce(int.__xor__,[b[k] for k in range(8) if row&(128>>k)],0) for row in a]
def transpose(a):return [sum(((a[i]>>(7-j))&1)<<(7-i) for i in range(8)) for j in range(8)]
def affine(a,b,c):return c^sum(((a[i]&b).bit_count()%2)<<(7-i) for i in range(8))

def test_machine(m):
    names=m.symbols; rng=random.Random(20260908)
    if 'copyData' in names:
        for xs in [[],[4],[3,-14,15,-92,65,35,-89],[-128,127,0,-1,-128],[2,2,1,1]]:
            m.write(DATA,xs);m.write(DATA+256,[0xAA]*32)
            m.call('copyData',[DATA,DATA+256,len(xs)]);expect(m.read(DATA+256,len(xs)),[x&255 for x in xs]);expect(m.read(DATA+256+len(xs),1),[0xAA])
            m.call('insertionSort',[DATA+256,len(xs)]);expect(m.read(DATA+256,len(xs)),[x&255 for x in sorted(xs)])
        m.cases.append('Signed byte copy/sort: paper vector, empty, one, duplicates, -128/127; output guard intact')
    if 'KaprekarRoutine' in names:
        for n in [0,1,1111,3075,6174,9999,*range(1000,10000,31)]:
            ds=sorted(f'{n:04d}');expected=int(''.join(ds[::-1]))-int(''.join(ds))
            expect(m.call('KaprekarRoutine',[n]),expected)
        m.cases.append('Kaprekar single transform: paper3075->7173, zero digits, equal digits,291 sampled four-digit inputs')
        m.uc.mem_write(0x30000,b'\x32\xdf');m.write(SP,[3075,0,0,0,0,0,0x30002,0x01000000],True)
        m.call('SVC_Handler',except_regs=[UC_ARM_REG_R6]);expect(m.uc.reg_read(UC_ARM_REG_R6),5);expect(m.read(SP,1,True),[6174])
        m.uc.mem_write(0x30000,b'\x31\xdf');m.write(SP,[3075,0,0,0,0,0,0x30002,0x01000000],True)
        m.call('SVC_Handler');expect(m.read(SP,1,True),[3075])
        m.cases.append('SVC50 handler body: constructed MSP frame, five calls, liveR6=5, savedR7 restored; other service ignored (not hardware exception entry)')
    if 'SDIV64' in names:
        pairs=[(-38,-5),(-38,5),(-38,2),(0,1),(1,1),(-(1<<32),2),(0x7fffffff,1),(-(1<<31),1)]
        pairs += [(rng.randrange(-(1<<45),1<<45),rng.randrange(1<<16,1<<30)) for _ in range(300)]
        for n,d in pairs:
            q=trunc(n,d)
            if not -(1<<31)<=q<(1<<31):continue
            args=[(n>>32)&0xffffffff,n&0xffffffff,d&0xffffffff]
            expect(signed(m.call('SDIV64',args)),q)
            m.uc.reg_write(UC_ARM_REG_APSR,0x08000000)
            expect(signed(m.call('SDIV64S',args)),q)
            flags=m.uc.reg_read(UC_ARM_REG_APSR)
            v=int(abs(d)//2<=abs(signed(args[0])))
            expect(flags&0xF8000000,((int(q<0)<<31)|(int(q==0)<<30)|(v<<28)|0x08000000))
        m.cases.append('Signed64/32: signs, low-word carry, zero, INT32 boundary,300 deterministic cases; NZCV follows explicit paper rule and Q is preserved')
    if 'isSociable' in names:
        for n,v in [(1,0),(2,0),(28,1),(220,2),(12496,5),(100,0),(8128,1)]:expect(m.call('isSociable',[n],limit=20000000),v)
        m.cases.append('Sociable:1 termination, prime2, perfect28/8128, amicable220, five-cycle12496, terminating100')
    if 'digitSum' in names:
        for n in [0,47,1000,4294967295]:expect(m.call('digitSum',[n]),sum(map(int,str(n))))
        for seed,count in [(47,5),(47,1),(47,50),(0,1),(4294967295,2),(4294967250,10),(99,0)]:
            xs=[seed];total=sum(map(int,str(seed))) if count else 0
            for i in range(1,count):
                nxt=xs[-1]+sum(map(int,str(xs[-1])))
                if nxt>0xffffffff:total=0;break
                xs.append(nxt);total+=sum(map(int,str(nxt)))
            m.write(DATA,[0xACACACAC]*52,True);m.write(DATA,[seed],True)
            expect(m.call('digitaddition',[DATA,count]),total)
            if count:expect(m.read(DATA,len(xs),True),xs)
            expect(m.read(DATA+max(count,1)*4,1,True),[0xACACACAC])
        m.cases.append('Digit addition:47/5 returns62, one/empty,50 terms, zero, overflow does not store invalid term; guards intact')
    if 'mazeSolver' in names:
        for rows in [['*n*','* *','***'],['*****','*   *','*****'],['*n***','*   *','*** *','***s*']]:
            cells=list(''.join(rows).encode());r=len(rows);c=len(rows[0]);expected=cells[:];waves=0
            while True:
                updates={}
                for i,x in enumerate(expected):
                    if x!=32:continue
                    for off,d in [(-c,110),(1,101),(c,115),(-1,119)]:
                        if 97<=expected[i+off]<=122:updates[i]=d;break
                if not updates:break
                for i,x in updates.items():expected[i]=x
                waves+=1
            m.write(DATA,cells);expect(m.call('mazeSolver',[r,c,DATA]),waves);expect(m.read(DATA,len(cells)),expected)
        m.cases.append('Directional maze: one wave, no exit, multiple exits; independent simultaneous-wave model')
    if 'shortestPath' in names:
        rows=['XXXXXXXX',bytes([88,0,32,32,32,32,32,88]),'X XXXX X','X      X','XX X XXX','X  X  eX','X XX XXX','X      X','XXXXXXXX']
        cells=b''.join(r.encode() if isinstance(r,str) else r for r in rows)
        m.uc.mem_write(DATA,cells);expect(m.call('shortestPath',[9,8,DATA]),8)
        state=m.read(DATA,72);pos=state.index(101);route=[]
        for k in range(8,-1,-1):
            for off,led in [(1,4),(8,5),(-1,6),(-8,7)]:
                if state[pos+off]==k:pos+=off;route.append(led);break
            else:raise AssertionError('route missing')
        expect(route,[6,6,7,7,6,6,6,7,7])
        cells=b'XXXXX'+bytes([88,0,88,101,88])+b'XXXXX';m.uc.mem_write(DATA,cells);expect(m.call('shortestPath',[3,5,DATA]),0xffffffff)
        m.cases.append('Shortest path: original9x8 returns8 and nine specified LED moves; disconnected entrance returnsUINT32_MAX')
    if 'depthFirstSearch' in names:
        for flags in itertools.product([0,1],repeat=4):
            eligible=[i+1 for i,x in enumerate(flags) if not x]
            expect(m.call('chooseNeighbor',flags),eligible[0] if eligible else 0)
            for val in range(5):
                m.write(0xE000E018,[val],True);expect(m.call('chooseRandomNeighbor',flags),eligible[::-1][val%len(eligible)] if eligible else 0)
        cells=[255 if r in (0,5) or c in (0,4) else 0 for r in range(6) for c in range(5)];m.write(DATA,cells)
        m.call('depthFirstSearch',[DATA,6,5,7]);expected=[255]*5+[255,5,3,13,255]+[255,19,13,21,255]+[255,7,25,21,255]+[255,19,11,25,255]+[255]*5
        expect(m.read(DATA,30),expected)
        m.cases.append('DFS: paper6x5 final matrix; all16 visited-flag combinations; five SysTick values per random choice and exact stack-push order')
    if 'kruskal' in names:
        for y,x in itertools.product([2,3,4],repeat=2):
            n=12;maze=list(range(n));h=[2 if i%4==3 else 1 for i in range(n)];v=[2 if i>=8 else 1 for i in range(n)]
            mm,hh,vv=maze[:],h[:],v[:];xx=x;yy=y
            for it in range(10000):
                xx+=yy;wall=hh;offset=1
                if xx>=n:
                    xx-=n;wall=vv;offset=4
                    if xx>=n and yy>=n:break
                if xx<n:
                    if wall[xx]==0:yy+=1
                    elif wall[xx]==1 and mm[xx]!=mm[xx+offset]:
                        lo,hi=sorted([mm[xx],mm[xx+offset]]);wall[xx]=0;mm=[lo if a==hi else a for a in mm]
                if not any(mm):break
            else:raise AssertionError('paper model did not terminate')
            m.write(DATA,maze);m.write(DATA+32,h);m.write(DATA+64,v)
            m.call('kruskal',[DATA,DATA+32,DATA+64,3,4,y,x]);expect(m.read(DATA,12),mm);expect(m.read(DATA+32,12),hh);expect(m.read(DATA+64,12),vv)
        m.cases.append('Kruskal: all nine3x4 button pairs: five complete and four explicit partial-maze exits when x>=N,y>=N; arrays match the paper model up to its nonconverging state')
    if 'bitwiseAffineTransformation' in names:
        a=[0xF8,0x7C,0x3E,0x1F,0x8F,0xC7,0xE3,0xF1]
        for matrix in [a,a[4:]+a[:4],[128>>i for i in range(8)],[0]*8,[255]*8]:
            m.write(DATA,matrix)
            for b in range(256):expect(m.call('bitwiseAffineTransformation',[DATA,b,0x63]),affine(matrix,b,0x63))
            expect(m.read(DATA,8),matrix)
        expect(affine(a,0xAA,0x63),0xC9)
        m.cases.append('Affine: all256 input bytes across five matrices including both paper matrices; original exampleC9; input unchanged')
    if 'bitMatrixMultiplication' in names:
        vectors=[([0x20,0x3f,0xc8,0x4d,0x76,0x58,0x48,0x50],[0xf8,0x7c,0x3e,0x1f,0x8f,0xc7,0xe3,0xf1])]
        vectors += [([rng.randrange(256) for _ in range(8)],[rng.randrange(256) for _ in range(8)]) for _ in range(64)]
        vectors += [([128>>i for i in range(8)],[255]*8),([0]*8,[255]*8)]
        for a,b in vectors:
            m.write(DATA,a);m.write(DATA+32,b);m.write(DATA+64,[0xA5]*12)
            m.call('bitMatrixMultiplication',[DATA,DATA+32,DATA+64]);expect(m.read(DATA+64,8),matrix_product(a,b));expect(m.read(DATA,8),a);expect(m.read(DATA+32,8),b);expect(m.read(DATA+72,4),[0xA5]*4)
        m.cases.append('GF2 product: original example, identity/zero and64 deterministic matrix pairs; input and output guards preserved')
    if 'transposition' in names:
        for a in [[0]*8,[255]*8,[128>>i for i in range(8)],*[[(rng.randrange(256)) for i in range(8)] for _ in range(64)]]:
            m.write(DATA,a);m.write(DATA+32,[0xA5]*12);m.call('transposition',[DATA,DATA+32]);expect(m.read(DATA+32,8),transpose(a));expect(m.read(DATA,8),a);expect(m.read(DATA+40,4),[0xA5]*4)
        m.cases.append('Transpose: exact paper export, zero/all-one/identity and64 random matrices; guards and source preserved')
    for name,cos in [('Maclaurin',False),('Maclaurin_cos',True)]:
        if name not in names:continue
        for y,n in [(20,3),(25,4),*[(y,n) for y in range(-31,32) for n in range(5)]]:
            term=100 if cos else 10*y;total=term
            for i in range(1,n+1):term=trunc(-term*y*y,((2*i-1)*(2*i) if cos else (2*i)*(2*i+1))*100);total+=term
            expect(signed(m.call(name,[y,n])),total)
        m.cases.append('Maclaurin: signed truncated recurrence, paper example, y=-31..31 at orders0..4')
    for name,variant in [('nextElementLCG',1),('LCGsequence',2)]:
        if name not in names:continue
        previous=1 if variant==1 else 6;values=[]
        for i in range(10):
            args=[previous,131,7,i,255] if variant==1 else [previous,157,3,3,256]
            previous=m.call(name,args);values.append(previous)
        expect(values,[138,234,63,103,236,71,126,198,182,125] if variant==1 else [177,134,33,68,191,49,22,131,74,108])
        m.cases.append('LCG: all ten paper sequence values and fifth stack argument')
    for name,swap in [('Look_and_Say',False),('run_length_encoding',True)]:
        if name not in names:continue
        for n in [0,1,111,101,1000,3668999,2222779,*range(256)]:
            expected=reference_digits(n,swap)
            if expected<=0xffffffff:expect(m.call(name,[n]),expected)
        m.cases.append('Decimal runs: paper examples,0, trailing/internal zeros, repeated run and all256 ADC inputs')
    if 'Recaman' in names:
        for n in [0,1,2,8,25,255]:
            expected=[]
            for i in range(n):
                candidate=expected[-1]-i if i else 0
                expected.append(0 if not i else candidate if candidate>0 and candidate not in expected else expected[-1]+i)
            m.write(DATA,[0xA5A5A5A5]*256,True);m.call('Recaman',[DATA,n]);expect(m.read(DATA,n,True),expected);expect(m.read(DATA+4*n,1,True),[0xA5A5A5A5])
        m.cases.append('Recaman: lengths0,1,2,8,25,255; independent sequence including repeated addition values; output guard intact')
    for name,conway in [('HofstadterQ',False),('HofstadterConway',True)]:
        if name not in names:continue
        for n in [-1,0,1,2,8,1000]:
            seq=[0]+[1]*max(0,min(2,n))
            for i in range(3,n+1):seq.append(seq[seq[i-1]]+seq[i-seq[i-1]] if conway else seq[i-seq[i-1]]+seq[i-seq[i-2]])
            m.write(DATA,[0xA5A5A5A5]*1001,True);expect(m.call(name,[DATA,n]),max(seq));expect(m.read(DATA,max(n,0),True),seq[1:]);expect(m.read(DATA+4*max(n,0),1,True),[0xA5A5A5A5])
        m.cases.append('Hofstadter: signed dimensions-1,0,1,2,8,1000; independent one-based recurrence and prefix maximum; output guard intact')
    for name in ['BullsAndCows','Mastermind']:
        if name not in names:continue
        codes=list(itertools.product(range(4),repeat=4))
        pairs=[((0,1,2,3),(1,2,2,0)),*((a,a) for a in codes)]
        pairs += [(rng.choice(codes),rng.choice(codes)) for _ in range(2048)]
        for a,b in pairs:
            exact=sum(x==y for x,y in zip(a,b));partial=sum((collections.Counter(a)&collections.Counter(b)).values())-exact
            expected=(((1<<exact)-1)<<4)+((1<<partial)-1)
            for off,x in [(0,a),(32,b),(64,[0]*4),(96,[0]*4)]:m.write(DATA+off,x,True)
            expect(m.call(name,[DATA,DATA+32,DATA+64,DATA+96]),expected);expect(m.read(DATA,4,True),list(a));expect(m.read(DATA+32,4,True),list(b))
            if name=='BullsAndCows':
                expect(m.read(DATA+64,4,True),[sum(a[i]==d and a[i]!=b[i] for i in range(4)) for d in range(4)])
            else:expect(sum(m.read(DATA+64,4,True)),exact+partial)
        m.cases.append('Game scoring: paper example, all256 exact codes,2048 deterministic duplicate-heavy pairs; scratch effects and unchanged inputs checked')
    if 'Reset_Handler' in names and any(n in names for n in ('review_finished','lcg_finished','finished')):
        stop=next(names[n]&~1 for n in ('review_finished','lcg_finished','finished') if n in names)
        if 'review_scratch' in names:m.write(names['review_scratch'],[0xA5]*32)
        m.uc.reg_write(UC_ARM_REG_SP,SP)
        m.uc.emu_start(names['Reset_Handler']|1,stop,count=1000000)
        expect(m.uc.reg_read(UC_ARM_REG_PC),stop);expect(m.uc.reg_read(UC_ARM_REG_SP),SP)
        if 'review_scratch' in names:expect(m.uc.reg_read(UC_ARM_REG_R0),19)
        if 'review_series' in names:
            values=[47]
            for i in range(49):values.append(values[-1]+sum(map(int,str(values[-1]))))
            expect(m.read(names['review_series'],50,True),values)
            expect(m.uc.reg_read(UC_ARM_REG_R0),sum(sum(map(int,str(v))) for v in values))
        if 'sequence' in names:expect(m.read(names['sequence'],10),[138,234,63,103,236,71,126,198,182,125])
        if 'lcg_test_values' in names:expect(m.read(names['lcg_test_values'],10),[177,134,33,68,191,49,22,131,74,108])
        m.cases.append('Standalone Reset_Handler executed to its inspection loop: expected result/data and balanced stack; game scratch starts dirty and is cleared before scoring (not hardware reset-vector entry).')

def main():
    from question_review import assembly_dependency
    results=json.loads((HERE/'QUESTION_EXECUTION_RESULTS.json').read_text()) if (HERE/'QUESTION_EXECUTION_RESULTS.json').exists() else {};cache={}
    for qid,r in REVIEWS.items():
        if len(sys.argv)>1 and qid not in sys.argv[1:]:continue
        sources=[ROOT/s for s in r['sources'] if s.endswith('.s')]
        if not sources:
            dependency=assembly_dependency(r)
            if dependency:sources=[dependency]
        if not sources:continue
        for path in sources:
            key=hashlib.sha256(path.read_bytes()).hexdigest()
            if key not in cache:
                try:
                    m=Machine(path);test_machine(m)
                    cache[key]={'status':'PASS','cases':m.cases,'nativeAssembly':'Native ARMASM syntax accepted separately; LLVM directive translation executes the delivered instruction stream','limits':'Does not simulate hardware exception entry, IRQ timing, peripherals, or the physical board.'}
                except Exception as e:cache[key]={'status':'FAIL','error':str(e)}
            results[qid]=dict(cache[key],source=path.relative_to(ROOT).as_posix(),sourceSha256=key)
            print(qid,results[qid]['status'],results[qid].get('error',''),flush=True)
    (HERE/'QUESTION_EXECUTION_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    return int(any(r['status']!='PASS' for r in results.values()))
if __name__=='__main__':raise SystemExit(main())
