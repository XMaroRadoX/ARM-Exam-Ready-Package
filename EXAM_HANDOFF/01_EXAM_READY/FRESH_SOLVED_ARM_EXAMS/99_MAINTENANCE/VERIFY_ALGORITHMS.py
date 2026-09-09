"""Execute C fixtures and the delivered Thumb instruction streams separately.

LLVM requires GNU spelling for section/export/data directives. The conversion
does not compile C into the delivered assembly or alter instructions. Native
Keil ARMASM validation is a separate, explicitly reported gate.
"""
from __future__ import annotations
import argparse, ctypes, hashlib, importlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE / '.test-deps'))
CLANG = Path('C:/Program Files/LLVM/bin/clang.exe')
LLD = CLANG.with_name('ld.lld.exe')
BUILD = HERE / '.algorithm-tests'

def gas(text):
    output=['.syntax unified', '.cpu cortex-m3', '.thumb']
    for line in text.splitlines():
        line=line.split(';')[0].rstrip()
        if not line.strip(): continue
        s=line.strip()
        if s.startswith('AREA '):
            output.append('.section .rodata' if 'DATA' in s and 'READONLY' in s else '.section .data' if 'DATA' in s else '.text')
        elif s.startswith(('PRESERVE8','THUMB','END','ENTRY','REQUIRE8')): continue
        elif s.startswith(('EXPORT ', 'GLOBAL ')): output.append('.global '+s.split()[1])
        elif s.startswith('IMPORT '): output.append('.extern '+s.split()[1])
        elif s in ('ENDP', 'ENDFUNC'): continue
        elif ' EQU ' in s:
            key,value=s.split(' EQU ',1); output.append('.equ '+key.strip()+','+value.strip())
        elif re.search(r'\b(DCD|DCW|DCB|SPACE)\b',s):
            m=re.match(r'(?:(\w+)\s+)?(DCD|DCW|DCB|SPACE)\s+(.+)',s)
            if not m: raise ValueError(s)
            label,kind,value=m.groups()
            if label: output.append(label+':')
            output.append({'DCD':'.word','DCW':'.hword','DCB':'.byte','SPACE':'.space'}[kind]+' '+value)
        elif s.startswith('ALIGN'): output.append('.balign 4')
        elif s.startswith('LTORG'): output.append('.ltorg')
        elif not line[0].isspace() and not s.startswith(('.', '@')):
            fields=s.split(None,1)
            output += [fields[0]+':']
            if len(fields)>1 and fields[1] not in ('PROC','FUNCTION'): output += [fields[1]]
        else: output.append(line)
    return '\n'.join(output)+'\n'

RUNTIME = '''#include <stddef.h>
void *memset(void*d,int c,size_t n){unsigned char*p=d;while(n--)*p++=(unsigned char)c;return d;}
void *memcpy(void*d,const void*s,size_t n){unsigned char*p=d;const unsigned char*q=s;while(n--)*p++=*q++;return d;}
void __aeabi_memset4(void*d,size_t n,int c){memset(d,c,n);}
void __aeabi_memset(void*d,size_t n,int c){memset(d,c,n);}
void __aeabi_memclr8(void*d,size_t n){memset(d,0,n);}
void __aeabi_memcpy8(void*d,const void*s,size_t n){memcpy(d,s,n);}
void __aeabi_memclr4(void*d,size_t n){memset(d,0,n);}
void __aeabi_memclr(void*d,size_t n){memset(d,0,n);}
void __aeabi_memcpy4(void*d,const void*s,size_t n){memcpy(d,s,n);}
void __aeabi_memcpy(void*d,const void*s,size_t n){memcpy(d,s,n);}
'''

def run(cmd):
    p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
    if p.returncode: raise RuntimeError((p.stdout+p.stderr)[-3000:])
    return p

def emulate(elf, exports):
    from elftools.elf.elffile import ELFFile
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_MODE_MCLASS, UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11
    uc=Uc(UC_ARCH_ARM, UC_MODE_THUMB|UC_MODE_MCLASS)
    uc.mem_map(0x10000,0x200000)
    uc.mem_map(0x20000000,0x200000)
    with elf.open('rb') as f:
        e=ELFFile(f)
        for seg in e.iter_segments():
            if seg['p_type']=='PT_LOAD': uc.mem_write(seg['p_vaddr'],seg.data())
        symbols={s.name:s['st_value'] for s in e.get_section_by_name('.symtab').iter_symbols()}
        functions={}
        for sym in e.get_section_by_name('.symtab').iter_symbols():
            idx=sym['st_shndx']
            if sym.name in exports and isinstance(idx,int) and e.get_section(idx)['sh_flags'] & 4:
                functions[sym.name]=sym['st_value']&~1
    # Keil runtime ABI helpers use four result registers, not C struct return.
    from unicorn.arm_const import UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
    def divide(uc,address,size,signed):
        rr=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]
        a=uc.reg_read(rr[0])|(uc.reg_read(rr[1])<<32)
        b=uc.reg_read(rr[2])|(uc.reg_read(rr[3])<<32)
        if signed:
            if a>>63:a-=1<<64
            if b>>63:b-=1<<64
        if not b: raise RuntimeError('runtime division by zero')
        q=abs(a)//abs(b)
        if (a<0)!=(b<0):q=-q
        rem=a-q*b
        for reg,val in zip(rr,[q,q>>32,rem,rem>>32]):uc.reg_write(reg,val&0xffffffff)
    for name,signed in [('__aeabi_uldivmod',False),('__aeabi_ldivmod',True)]:
        if name in symbols:
            address=symbols[name]&~1
            uc.hook_add(UC_HOOK_CODE,divide,user_data=signed,begin=address,end=address)
    sp=0x201f0000; stop=0x20000f00
    uc.reg_write(UC_ARM_REG_SP,sp); uc.reg_write(UC_ARM_REG_LR,stop|1)
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    for i,r in enumerate(regs): uc.reg_write(r,0x44440000+i)
    addresses={address:name for name,address in functions.items()}
    active=[]; called=set()
    def check_calls(uc,address,size,data):
        # Check each public callee before the C fixture can restore its own frame.
        returning = bool(active and address==active[-1][1])
        while returning:
            name,ret,entry_sp,saved=active.pop()
            if uc.reg_read(UC_ARM_REG_SP)!=entry_sp:
                raise RuntimeError(name+': SP not restored')
            for reg,value in zip(regs,saved):
                if uc.reg_read(reg)!=value: raise RuntimeError(name+': callee-saved register changed')
            # Recursive invocations can share a return PC. Only a tail-call
            # chain also shares the just-restored entry SP.
            returning = bool(active and address==active[-1][1] and uc.reg_read(UC_ARM_REG_SP)==active[-1][2])
        if address in addresses:
            name=addresses[address]; called.add(name)
            if uc.reg_read(UC_ARM_REG_SP)&7:raise RuntimeError(name+': SP not aligned at public entry')
            active.append((name,uc.reg_read(UC_ARM_REG_LR)&~1,uc.reg_read(UC_ARM_REG_SP),
                           [uc.reg_read(reg) for reg in regs]))
    uc.hook_add(UC_HOOK_CODE,check_calls)
    uc.emu_start(symbols['test_main']|1,stop,count=20000000)
    from unicorn.arm_const import UC_ARM_REG_PC
    if uc.reg_read(UC_ARM_REG_PC)!=stop: raise RuntimeError('instruction budget exceeded')
    if uc.reg_read(UC_ARM_REG_SP)!=sp: raise RuntimeError('SP not restored')
    for i,r in enumerate(regs):
        if uc.reg_read(r)!=0x44440000+i: raise RuntimeError('callee-saved register changed')
    return uc.reg_read(UC_ARM_REG_R0), sorted(called), sorted(set(functions)-called)

def verify_entry(entry):
    folder=BUILD/entry['slug']; folder.mkdir(parents=True,exist_ok=True)
    check='#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)\n'
    fixture=entry['test']
    if entry.get('reuse_build') and all((folder/name).exists() and (folder/name).read_text()==value for name,value in
        [('reference.c',entry['code']),('test.c',check+fixture),('implementation.s',entry['assembly'])]):
        host=subprocess.run([str(folder/'host.exe')],capture_output=True)
        if host.returncode:raise RuntimeError('Cached C assertion failed: '+str(host.returncode))
        result,called,untested=emulate(folder/'test.elf',re.findall(r'(?m)^\s*EXPORT\s+(\w+)',entry['assembly']))
        if result:raise RuntimeError('Cached ARM assertion failed: '+str(result))
        return dict(slug=entry['slug'],status='C_AND_THUMB_EXECUTION_PASS',assembly_sha256=hashlib.sha256(entry['assembly'].encode()).hexdigest(),c_sha256=hashlib.sha256(entry['code'].encode()).hexdigest(),assertions=len(re.findall(r'\bCHECK\(',fixture)),executed_exports=called,untested_exports=untested,build='reused matching source and fixture artifacts')
    (folder/'reference.c').write_text(entry['code'],encoding='utf-8')
    (folder/'test.c').write_text(check+fixture,encoding='utf-8')
    (folder/'implementation.s').write_text(entry['assembly'],encoding='utf-8')
    (folder/'implementation.gnu.s').write_text(gas(entry['assembly']),encoding='utf-8')
    (folder/'host.c').write_text(entry['code']+'\n'+check+fixture.replace('#include <stdint.h>','')+'\nint main(void){return test_main();}\n',encoding='utf-8')
    gcc=shutil.which('gcc')
    (folder/'host_main.c').write_text('int test_main(void); int main(void){return test_main();}')
    run([gcc,'-std=c11','-O0','-Wall','-Wextra',folder/'reference.c',folder/'test.c',folder/'host_main.c','-o',folder/'host.exe'])
    host=subprocess.run([str(folder/'host.exe')],capture_output=True)
    if host.returncode: raise RuntimeError(f'C assertion failed (line modulo 256): {host.returncode}')
    flags=['--target=arm-none-eabi','-mcpu=cortex-m3','-mthumb','-O0','-ffreestanding','-fno-builtin','-fno-stack-protector']
    run([CLANG,*flags,'-c',folder/'test.c','-o',folder/'test.o'])
    run([CLANG,*flags,'-c',folder/'implementation.gnu.s','-o',folder/'asm.o'])
    (folder/'runtime.c').write_text(RUNTIME,encoding='utf-8')
    run([CLANG,*flags,'-c',folder/'runtime.c','-o',folder/'runtime.o'])
    (folder/'abi.s').write_text('.syntax unified\n.thumb\n.text\n.global __aeabi_uldivmod\n.thumb_func\n__aeabi_uldivmod:\n bx lr\n.global __aeabi_ldivmod\n.thumb_func\n__aeabi_ldivmod:\n bx lr\n')
    run([CLANG,*flags,'-c',folder/'abi.s','-o',folder/'abi.o'])
    run([LLD,'-Ttext=0x10000','--entry=test_main',folder/'test.o',folder/'asm.o',folder/'runtime.o',folder/'abi.o','-o',folder/'test.elf'])
    result,called,untested=emulate(folder/'test.elf',re.findall(r'(?m)^\s*EXPORT\s+(\w+)',entry['assembly']))
    if result: raise RuntimeError(f'ARM assertion failed at fixture line {result}')
    return dict(slug=entry['slug'],status='C_AND_THUMB_EXECUTION_PASS',assembly_sha256=hashlib.sha256(entry['assembly'].encode()).hexdigest(),c_sha256=hashlib.sha256(entry['code'].encode()).hexdigest(),assertions=len(re.findall(r'\bCHECK\(',entry['test'])), executed_exports=called, untested_exports=untested)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--match',default=''); ap.add_argument('--legacy',action='store_true'); ap.add_argument('--existing',action='store_true'); ap.add_argument('--published',action='store_true'); ap.add_argument('--reuse-build',action='store_true'); args=ap.parse_args()
    from algorithm_catalog import ENTRIES
    import exam_algorithms_numeric, exam_algorithms_arrays, exam_algorithms_strings, exam_algorithms_matrices
    import exam_algorithms_fundamentals_arrays
    import exam_algorithms_fundamentals_strings
    import exam_algorithms_fundamentals_arithmetic
    import exam_algorithms_fundamentals_bits
    import exam_algorithms_fundamentals_matrices
    selected=ENTRIES
    if args.legacy:
        from legacy_algorithm_tests import entries
        selected=entries()
    if args.existing:
        import existing_algorithm_repairs
        selected=existing_algorithm_repairs.EXISTING
    if args.published:
        raw=HERE.parent/"03_COPY_PASTE_LIBRARY"/"CANONICAL_WORKSTATION"/"algorithms"
        selected=[dict(slug="published-"+p.name,code=(p/"reference.c").read_text(encoding="utf-8"),
                    assembly=(p/"implementation.s").read_text(encoding="utf-8"),
                    test=(p/"test_vectors.c").read_text(encoding="utf-8")) for p in sorted(raw.iterdir()) if p.is_dir()]
    from concurrent.futures import ThreadPoolExecutor, as_completed
    def task(e):
        try: return verify_entry(e)
        except Exception as exc: return dict(slug=e['slug'],status='FAIL',reason=str(exc))
    from algorithm_property_vectors import augment
    selected=[dict(augment(e),reuse_build=args.reuse_build) for e in selected if not args.match or args.match in e['slug']]
    results=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(task,e) for e in selected]):
            result=future.result(); results.append(result)
            print(result['slug'],result['status'],result.get('reason',''),flush=True)
    results.sort(key=lambda r:r['slug'])
    (HERE/('PUBLISHED_ALGORITHM_TEST_RESULTS.json' if args.published else 'LEGACY_ALGORITHM_TEST_RESULTS.json' if args.legacy else 'EXISTING_ALGORITHM_TEST_RESULTS.json' if args.existing else 'ALGORITHM_TEST_RESULTS.json')).write_text(json.dumps(dict(native_armasm='NOT_RUN: Keil ARMASM not located',results=results),indent=2)+'\n')
    return int(any(r['status']=='FAIL' for r in results))

if __name__=='__main__': raise SystemExit(main())
