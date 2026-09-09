"""Coverage, compilation and execution checks for the displayed ASM reference."""
from pathlib import Path
import json,re,sys
from asm_reference import ENTRIES, CONDITIONS
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE/'.test-deps'))
PORTAL=HERE.parent/'01_GUIDES_AND_INDEXES/PORTAL'
BUILD=HERE/'.asm-reference-tests'
NAMES={n.upper():e['id'] for e in ENTRIES for n in e['names']}
CONDS={x[0] for x in CONDITIONS}|{'AL'}
def resolve(token):
    token=re.sub(r'\.(W|N)$','',token.upper())
    if token in NAMES:return NAMES[token]
    if len(token)>2 and token[-2:] in CONDS and token[:-2] in NAMES:return NAMES[token[:-2]]
    return None
def coverage():
    from pypdf import PdfReader
    from course_arm import ARM
    sources={};unknown={};found={};pdfs=[];unextractable=[]
    def add(token,path):
        token=token.upper().strip(',;:')
        if not token:return
        (found if resolve(token) else unknown).setdefault(token,set()).add(path)
    def assembly(text,path):
        for line in text.splitlines():
            code=line.split(';')[0].rstrip()
            if not code.strip():continue
            words=code.split()
            if not code[0].isspace() and not resolve(words[0]):words=words[1:]
            if words:add(words[0],path)
    maintained=HERE.parent/'03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION'
    template=ROOT/'01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/Source'
    for p in [*maintained.rglob('*.s'),*template.glob('*.s')]:
        key=p.relative_to(ROOT).as_posix();sources[key]='assembly';assembly(p.read_text(encoding='utf-8',errors='replace'),key)
    for lesson in ARM:
        key='course_arm.py#'+lesson['id'];sources[key]='lesson';assembly(lesson['code'],key)
    vocabulary=set(NAMES)|set('ARM CODE32 MRC MCR CDP LDC STC SWI SWP SWPB LDMIB LDMDA STMIB STMDA RSC SETEND SRS RFE LDRT LDRBT LDRHT LDRSBT LDRSHT STRT STRBT STRHT TBB TBH DCI DCQ DCQU GBLA GBLL GBLS LCLA LCLL LCLS SETA SETL SETS ASSERT TTL SUBT DCFD DCFS ADRL MOV32 QADD QSUB SADD16'.split())
    for p in sorted((ROOT/'02_ORIGINAL_MATERIALS/ARM').glob('*.pdf')):
        m=re.match(r'(\d+)_',p.name)
        if not m or int(m[1])>12:continue
        reader=PdfReader(p);pdfs.append(p.name)
        for i,page in enumerate(reader.pages):
            text=page.extract_text() or '';key=p.relative_to(ROOT).as_posix()+'#page='+str(i+1);sources[key]='lecture'
            if not text.strip():unextractable.append(key)
            for token in re.findall(r'\b[A-Z][A-Z0-9]+(?:\.[WN])?\b',text):
                base=re.sub(r'\.[WN]$','',token)
                if base in vocabulary or resolve(token):add(token,key)
    report=dict(sourceCount=len(sources),lecturePdfs=pdfs,unextractablePages=unextractable,method='Assembly opcode fields, authored lesson code, and recognized mnemonic tokens in the 12 core lecture PDFs; images are not OCRed.',spellings={k:sorted(v) for k,v in sorted(found.items())},unresolved={k:sorted(v) for k,v in sorted(unknown.items())})
    (HERE/'ASM_REFERENCE_COVERAGE.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report
def execute():
    from VERIFY_ALGORITHMS import CLANG,LLD,gas as existing_gas,run,emulate
    def gas(source):
        # Preserve each standalone ARMASM ALIGN byte value in the test translation.
        aligns=iter(re.findall(r'(?m)^\s*ALIGN(?:\s+(\d+))?\s*$',source))
        return re.sub(r'(?m)^\.balign 4$',lambda m:'.balign '+(next(aligns,'4') or '4'),existing_gas(source))
    BUILD.mkdir(exist_ok=True);compiled=[];skipped={};errors={}
    flags=['--target=arm-none-eabi','-mcpu=cortex-m3','-mthumb']
    for e in ENTRIES:
        if e['category']=='ARMASM directives' or e['id'] in ('adrl','mov32'):
            skipped[e['id']]='ARMASM-only directive/pseudo-instruction example; checked against documentation, not natively assembled';continue
        source=gas(e['example'])
        if e['id']=='registers':source+='\nhelper:\n bx lr\n'
        path=BUILD/(e['id']+'.s')
        if path.exists() and path.read_text(encoding='utf-8')==source and path.with_suffix('.o').exists():compiled.append(e['id']);continue
        path.write_text(source,encoding='utf-8')
        try:run([CLANG,*flags,'-c',path,'-o',path.with_suffix('.o')]);compiled.append(e['id'])
        except RuntimeError as ex:errors[e['id']]=str(ex)
    parts=[];exports=['plus_one','fifth','sum_words','max_signed']
    for ident in ['function-template','fifth-argument','array-loop','if-else']:
        parts.append(gas(next(e for e in ENTRIES if e['id']==ident)['example']).replace('.global plus_one',''))
    for ident,symbol in [('add','carry_case'),('sub','borrow_case'),('adc','wide_case'),('ldrb','signed_load_case'),('bvs','overflow_case'),('lsl','shift_case'),('remainder','remainder_case')]:
        text=next(e for e in ENTRIES if e['id']==ident)['example']
        if ident in ('add','sub'):text+='\n        MRS R0, APSR'
        if ident=='adc':text+='\n        MOV R0, R1'
        if ident=='ldrb':text+='\n        MOV R0, R2'
        if ident in ('bvs','lsl'):text+='\n        MOV R0, R2'
        parts.append('.text\n.global '+symbol+'\n.thumb_func\n'+symbol+':\n'+gas(text)+'\n BX LR\n');exports.append(symbol)
    parts.append('.text\n.global nested\n.thumb_func\nnested:\n'+gas(next(e for e in ENTRIES if e['id']=='bl')['example']));exports+=['nested','helper']
    source='\n'.join(parts)
    for name in ['plus_one','fifth','sum_words','max_signed','helper']:source=source.replace(name+':','.global '+name+'\n.thumb_func\n'+name+':')
    (BUILD/'combined.s').write_text(source)
    fixture='''#include <stdint.h>
extern uint32_t plus_one(uint32_t),fifth(uint32_t,uint32_t,uint32_t,uint32_t,uint32_t),sum_words(const uint32_t*,uint32_t),nested(uint32_t);
extern int32_t max_signed(int32_t,int32_t),signed_load_case(void);
extern uint32_t carry_case(void),borrow_case(void),wide_case(void),overflow_case(void),shift_case(void),remainder_case(uint32_t,uint32_t);
#define CHECK(x) do {if(!(x))return __LINE__;}while(0)
int test_main(void){
 uint32_t a[]={3,5,7},b[]={0xffffffffu,1};
 CHECK(plus_one(41)==42);CHECK(plus_one(0xffffffffu)==0);CHECK(fifth(1,2,3,4,99)==99);
 CHECK(sum_words(a,3)==15);CHECK(sum_words(a,0)==0);CHECK(sum_words(a,1)==3);CHECK(sum_words(b,2)==0);
 CHECK(max_signed(-1,2)==2);CHECK(max_signed(9,-1)==9);CHECK(max_signed(-7,-7)==-7);CHECK(max_signed(INT32_MIN,INT32_MAX)==INT32_MAX);
 CHECK((carry_case()>>28)==6);CHECK((borrow_case()>>28)==8);CHECK(wide_case()==1);CHECK(signed_load_case()==-2);
 CHECK(nested(41)==42);CHECK(overflow_case()==1);CHECK(shift_case()==0xfffffffeu);
 CHECK(remainder_case(47,10)==7);CHECK(remainder_case(0,10)==0);CHECK(remainder_case(9,10)==9);return 0;
}'''
    (BUILD/'fixture.c').write_text(fixture)
    run([CLANG,*flags,'-c',BUILD/'combined.s','-o',BUILD/'combined.o'])
    run([CLANG,*flags,'-O0','-ffreestanding','-c',BUILD/'fixture.c','-o',BUILD/'fixture.o'])
    run([LLD,'-Ttext=0x10000','-e','test_main',BUILD/'combined.o',BUILD/'fixture.o','-o',BUILD/'test.elf'])
    result,called,untested=emulate(BUILD/'test.elf',exports)
    if result:errors['execution']='C assertion failed at line '+str(result)
    return dict(compiledExamples=compiled,compilationErrors=errors,directiveReview=skipped,executedFunctions=called,unexecutedFunctions=untested,assertions=fixture.count('CHECK(')-1,execution='PASS' if not result else 'FAIL',toolchain='LLVM Cortex-M3 with ARMASM directive translation; Unicorn execution and ABI checks',nativeKeil='Not run: assembler not found in standard installed locations',physicalBoard='Not tested')
def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--coverage-only',action='store_true');args=parser.parse_args()
    cov=coverage();print('Coverage unresolved:',json.dumps(cov['unresolved'],indent=2))
    if args.coverage_only:return
    result=execute();raw=(PORTAL/'asm/index.html').read_text(encoding='utf-8');errors=[]
    for e in ENTRIES:
        if 'id="'+e['id']+'"' not in raw:errors.append('Missing entry '+e['id'])
        if not all(e[k] for k in ('purpose','syntax','rules','flags','example','result','mistake')):errors.append('Incomplete entry '+e['id'])
    if raw.count('<h1>')!=1:errors.append('Expected one h1')
    report=dict(entries=len(ENTRIES),names=len(NAMES),coverageUnresolved=cov['unresolved'],structuralErrors=errors,**result)
    (HERE/'ASM_REFERENCE_VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
    if errors or cov['unresolved'] or result['compilationErrors']:raise SystemExit(1)
if __name__=='__main__':main()
