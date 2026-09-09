"""Build isolated copies of the current Keil template for all reviewed questions."""
from pathlib import Path
import json,re,shutil
from concurrent.futures import ThreadPoolExecutor,as_completed
import BUILD_NATIVE_SCENARIOS as native
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
REVIEWS=json.loads((HERE/'QUESTION_REVIEWS.json').read_text(encoding='utf-8'))
TEMPLATE=ROOT/'01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API'
OUT=ROOT/'90_WORKING_PROJECTS/EXAM_REVIEW_BUILDS'
def remove_function(text,name):
    match=re.search(r'\bvoid\s+'+re.escape(name)+r'\s*\([^)]*\)\s*\{',text)
    if not match:return text
    depth=1;i=match.end()
    while depth:
        if text[i]=='{':depth+=1
        if text[i]=='}':depth-=1
        i+=1
    return text[:match.start()]+text[i:]
def prepare(qid,r):
    folder=OUT/qid;folder.mkdir(parents=True,exist_ok=True)
    shutil.copytree(TEMPLATE/'Source',folder/'Source',dirs_exist_ok=True,ignore=shutil.ignore_patterns('Objects','Listings','__pycache__'))
    for name in ['sample.uvprojx','sample.sct']:shutil.copy2(TEMPLATE/name,folder/name)
    c=next((ROOT/p for p in r['sources'] if p.endswith('/main.c')),None)
    asm=next((ROOT/p for p in r['sources'] if p.endswith('.s')),None)
    if asm is None and c:
        asm=c.with_name('assembly.s')
        if not asm.exists():asm=c.parent.parent/'assembly.s'
    target=folder/'Source/ASM_funct.s'
    if asm and asm.exists():shutil.copy2(asm,target)
    else:target.write_text(' AREA |.text|, CODE, READONLY\n THUMB\n END\n')
    if c:shutil.copy2(c,folder/'Source/sample.c')
    else:(folder/'Source/sample.c').write_text('#include "LPC17xx.h"\nint main(void) {for (;;) __WFI();}\n')
    supplied=[folder/'Source/sample.c']
    for source in r['sources']:
        if Path(source).name.startswith('IRQ_'):
            destinations=list((folder/'Source').rglob(Path(source).name));assert len(destinations)==1,(source,destinations)
            shutil.copy2(ROOT/source,destinations[0]);supplied.append(destinations[0])
    owners={name:p for p in supplied for name in re.findall(r'\bvoid\s+(\w+_IRQHandler)\s*\(',p.read_text())}
    for p in (folder/'Source').rglob('*.c'):
        if p in supplied:continue
        text=p.read_text(encoding='utf-8-sig')
        for name in owners:text=remove_function(text,name)
        p.write_text(text,encoding='utf-8')
    return {'id':'question-'+qid,'path':folder.relative_to(ROOT).as_posix()}
def main():
    native.CACHE.mkdir(exist_ok=True)
    results={}
    records=[prepare(q,r) for q,r in REVIEWS.items()]
    with ThreadPoolExecutor(max_workers=3) as pool:
        tasks={pool.submit(native.build,record,{}):record for record in records}
        for f in as_completed(tasks):
            record=tasks[f];qid=record['id'][9:]
            try:result=f.result()
            except Exception as e:result={'status':'FAIL','reason':str(e)}
            result['integration']='Current template copy; answer files installed, matching duplicate IRQ owners removed only in this disposable build copy.'
            results[qid]=result
            print(qid,result['status'],result.get('reason','')[-1000:],flush=True)
            (HERE/'QUESTION_NATIVE_BUILDS.json').write_text(json.dumps(results,indent=2)+'\n')
    return int(any(r['status']!='PASS' for r in results.values()))
if __name__=='__main__':raise SystemExit(main())
