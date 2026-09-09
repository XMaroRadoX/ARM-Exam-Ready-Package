"""Retain existing newline bytes while binding search evidence to the served files."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path.cwd();WORK=ROOT/'90_WORKING_PROJECTS/QUESTION_REVIEW_20260908';STAGE=WORK/'EXAM_HANDOFF'
rel='01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/SEARCH_COVERAGE.json'
coverage=json.loads((ROOT/rel).read_text(encoding='utf-8'));changes=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for entry in coverage['inventory']:
    if not entry.get('hash'):continue
    source=ROOT/entry['path'];actual=sha(source)
    if actual==entry['hash']:continue
    staged=STAGE/entry['path']
    assert source.read_text(encoding='utf-8-sig')==staged.read_text(encoding='utf-8-sig'),('substantive unindexed difference',source)
    assert sha(staged)==entry['hash'],('unexplained index difference',source)
    changes.append(entry['path']);entry['hash']=actual
    # Keep the staging evidence reproducible without modifying the preserved original.
    shutil.copy2(source,staged)
text=json.dumps(coverage,indent=2,ensure_ascii=False)
for base in (ROOT,STAGE):(base/rel).write_text(text,encoding='utf-8')
p=WORK/'published.json';log=json.loads(p.read_text(encoding='utf-8'))
next(x for x in log['files'] if x['path']==rel)['after']=sha(ROOT/rel)
log['preservedNewlineBytes']=changes
p.write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'reconciledUnchangedTextFiles':len(changes),'paths':changes},indent=2))
