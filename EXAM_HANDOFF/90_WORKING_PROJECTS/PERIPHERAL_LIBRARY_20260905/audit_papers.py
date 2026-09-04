from pathlib import Path
import csv,json,re,hashlib
from pypdf import PdfReader
work=Path(__file__).resolve().parent;root=work/'EXAM_HANDOFF'
maint=root/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE'
rows=list(csv.DictReader((root/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/EXAM_COURSE/REVIEWED_EXAM_INDEX.csv').open(encoding='utf-8-sig')))
reviewed={r['source_pdf']:r['exam_id'] for r in rows};records=[]
for p in sorted((root/'02_ORIGINAL_MATERIALS/Exams').rglob('*.pdf')):
    rel=p.relative_to(root).as_posix()
    try:
        pages=[page.extract_text() or '' for page in PdfReader(p).pages]
        evidence=[]
        for n,text in enumerate(pages,1):
            lines=text.splitlines()
            hits=[i for i,line in enumerate(lines) if re.search(r'\b(?:timer\d*|systick|rit|adc|dac|joystick|button|leds?|eint\d*|svc)\b',line,re.I)]
            excerpt='\n'.join(lines[i] for i in sorted({j for i in hits for j in range(max(0,i-1),min(len(lines),i+3))}))
            if hits:evidence.append({'page':n,'excerpt':excerpt})
        programming=bool(re.search(r'\b(?:LandTiger|LPC1768|joystick|EINT[012]|SysTick|DAC|potentiometer)\b',' '.join(pages),re.I))
        records.append(dict(path=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),examId=reviewed.get(rel),pages=len(pages),emptyPages=[n+1 for n,t in enumerate(pages) if not t.strip()],hardwareEvidence=evidence,status='Reviewed question mapping' if rel in reviewed else 'Board extension: paper-lcd-maze' if p.name=='20240709 board extension.pdf' else 'Needs content classification' if programming else 'Theory or administrative material; no board-programming question identified'))
    except Exception as e:records.append(dict(path=rel,error=str(e),status='Extraction failed'))
(maint/'PAPER_INVENTORY.json').write_text(json.dumps(records,indent=2)+'\n')
print('ARM paper inventory:',len(records))
for r in records:
    if r['status']=='Needs content classification':print(r['path'],r['status'],'hardware pages',len(r.get('hardwareEvidence',[])))
