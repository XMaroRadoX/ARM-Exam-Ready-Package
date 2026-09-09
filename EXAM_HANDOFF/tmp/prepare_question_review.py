from pathlib import Path
import csv, json, hashlib, shutil, os
from pypdf import PdfReader

root=Path(__file__).resolve().parents[1]
work=root/'90_WORKING_PROJECTS/QUESTION_REVIEW_20260908'
stage=work/'EXAM_HANDOFF'
base=root/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS'
def rows(p): return list(csv.DictReader(p.open(encoding='utf-8-sig')))
questions=rows(base/'01_GUIDES_AND_INDEXES/QUESTION_INDEX.csv')
exams=rows(base/'01_GUIDES_AND_INDEXES/EXAM_COURSE/REVIEWED_EXAM_INDEX.csv')
solutions={r['exam_id']:r for r in rows(base/'01_GUIDES_AND_INDEXES/CURRENT_TEMPLATE_SOLUTION_INDEX.csv')}
work.mkdir(parents=True,exist_ok=True)
baseline={}
for folder in ['01_EXAM_READY','02_ORIGINAL_MATERIALS','03_ADDITIONAL_STUDY_MATERIAL']:
    for directory,dirs,files in os.walk(root/folder):
        dirs[:]=[d for d in dirs if not d.startswith('.') and d not in ('Objects','Listings','__pycache__')]
        for name in files:
            src=Path(directory)/name
            dest=stage/src.relative_to(root)
            dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists() or dest.stat().st_size!=src.stat().st_size: shutil.copy2(src,dest)
            baseline[src.relative_to(root).as_posix()]=hashlib.sha256(src.read_bytes()).hexdigest()
for name in ['START_HERE.html','README.md']:
    shutil.copy2(root/name,stage/name)
    baseline[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
(work/'baseline.json').write_text(json.dumps(baseline,indent=2))
mapping=[]
for e in exams:
    pdf=root/e['source_pdf']
    prefix='_'.join(e['project'].split('_')[:2])
    qs=[q for q in questions if q['question_id'].startswith(prefix+'-Q')]
    if not qs: qs=[q for q in questions if q['question_id'].startswith(e['exam_id'])]
    if not qs: qs=[q for q in questions if q['date']==e['date']]
    s=solutions[e['exam_id']]
    text='\n'.join(f'\n--- PDF PAGE {i+1} ---\n'+(p.extract_text() or '') for i,p in enumerate(PdfReader(pdf).pages))
    parts=[json.dumps(e),text]
    for q in qs:
        c=root/s['current_c_source']; asm=root/s['current_assembly_source']
        specific=c.parent/q['question']
        sources=[]
        for name,default in [('main.c',c),('assembly.s',asm)]:
            if (name=='main.c' and '.c' not in q['answer_file']) or (name=='assembly.s' and '.s' not in q['answer_file']):continue
            src=specific/name if (specific/name).exists() else default
            sources.append(src)
        if specific.exists(): sources+=list(specific.glob('IRQ_*.c'))
        mapping.append(dict(question=q,exam=e['exam_id'],pdf=e['source_pdf'],sources=[p.relative_to(root).as_posix() for p in sources]))
        parts+=['\n--- QUESTION ---\n'+json.dumps(q)]
        for src in sources: parts+=['\n--- SOURCE '+src.relative_to(root).as_posix()+' ---\n'+src.read_text(encoding='utf-8-sig')]
    out=work/'inputs'/f"{e['exam_id']}.txt";out.parent.mkdir(exist_ok=True);out.write_text('\n'.join(parts),encoding='utf-8')
(work/'mapping.json').write_text(json.dumps(mapping,indent=2),encoding='utf-8')
print(json.dumps({'stage':str(stage),'files':len(baseline),'papers':len(exams),'questions':len(mapping)}))
