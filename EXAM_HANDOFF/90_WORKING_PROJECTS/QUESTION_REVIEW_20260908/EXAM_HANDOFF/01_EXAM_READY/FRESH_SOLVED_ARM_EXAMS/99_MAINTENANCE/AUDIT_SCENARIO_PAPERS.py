"""Inventory all supplied exam PDFs; retain explicit evidence and exclusions."""
from pathlib import Path
import csv,hashlib,json,re
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def main():
    with (HERE.parent/'01_GUIDES_AND_INDEXES/EXAM_COURSE/REVIEWED_EXAM_INDEX.csv').open(encoding='utf-8-sig') as f:reviewed={r['source_pdf']:r['exam_id'] for r in csv.DictReader(f)}
    records=[]
    for p in sorted((ROOT/'02_ORIGINAL_MATERIALS/Exams').rglob('*.pdf')):
        rel=p.relative_to(ROOT).as_posix();record=dict(path=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),examId=reviewed.get(rel))
        try:
            pages=[page.extract_text() or '' for page in PdfReader(p).pages]
            record.update(pages=len(pages),emptyPages=[i+1 for i,t in enumerate(pages) if not t.strip()])
            hardware=bool(re.search(r'\b(?:LandTiger|LPC1768|joystick|EINT[012]|SysTick|DAC|potentiometer)\b',' '.join(pages),re.I))
            if rel in reviewed:record['status']='Reviewed question mapping'
            elif p.name=='20240709 board extension.pdf':record.update(status='Additional board question mapped',scenario='paper-lcd-maze',question='Q5')
            elif p.parent.name=='ARM questions' and p.name=='20250701.pdf':record.update(status='Equivalent reviewed hardware exercise',scenario='paper-e2025-07-01-a1',evidence='nextElementLCG, seed 1, multiplier 131, increment 7, XOR iteration, modulus 255, Timer0 3 seconds, first joystick movement, 10 rounds. File labels differ; the behavior maps explicitly.')
            elif p.name in ('Exam rules.pdf','Exam rules v3.pdf','extrapoint_v2.pdf'):record.update(status='Administrative material',evidence='Exam rules or grading sheet, not an additional programming question.')
            elif hardware:record['status']='Needs content classification'
            else:record['status']='No board-programming exercise identified; standalone algorithms, theory or administrative material'
            if record['status'] not in ('Administrative material',):
                record['hardwareEvidence']=[]
                for i,t in enumerate(pages,1):
                    lines=t.splitlines();hits=[j for j,line in enumerate(lines) if re.search(r'\b(?:timer\d*|systick|rit|adc|dac|joystick|buttons?|leds?|eint\d*|svc)\b',line,re.I)]
                    if hits:record['hardwareEvidence'].append(dict(page=i,excerpt='\n'.join(lines[j] for j in sorted({n for j in hits for n in range(max(0,j-1),min(len(lines),j+3))}))))
        except Exception as e:record.update(status='Extraction failed',error=str(e))
        records.append(record)
    (HERE/'PAPER_INVENTORY.json').write_text(json.dumps(records,indent=2)+'\n')
    pending=[r['path'] for r in records if r['status'] in ('Needs content classification','Extraction failed')]
    print(len(records),'PDFs audited;',len(pending),'unresolved board candidates',pending)
    return bool(pending)
if __name__=='__main__':raise SystemExit(main())
