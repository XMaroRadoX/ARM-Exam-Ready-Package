"""Inventory this review's changes and check protected inputs before integration."""
from pathlib import Path
import hashlib,json,os
ROOT=Path.cwd();WORK=ROOT/'90_WORKING_PROJECTS/QUESTION_REVIEW_20260908';STAGE=WORK/'EXAM_HANDOFF'
baseline=json.loads((WORK/'baseline.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(root):
    for base,dirs,names in os.walk(root):
        dirs[:]=[x for x in dirs if not x.startswith('.') and x not in ['__pycache__','Objects','Listings']]
        for name in names:
            if not name.startswith('.'):yield Path(base)/name
prefix='01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/'
roots=[STAGE/prefix/'99_MAINTENANCE',STAGE/prefix/'01_GUIDES_AND_INDEXES',STAGE/prefix/'03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/exam-solutions']
candidates={p for root in roots for p in files(root)}
candidates.update(p for p in files(STAGE/'03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams') if '/Answer Source/' in p.as_posix())
changes=[]
for p in sorted(candidates):
    rel=p.relative_to(STAGE).as_posix();after=sha(p);before=baseline.get(rel)
    if after==before:continue
    original=ROOT/rel
    # A text-only newline conversion is not part of this review.
    if original.exists() and p.suffix in ['.html','.md','.csv','.js','.c','.s','.py','.json','.cjs','.log']:
        try:
            if original.read_text(encoding='utf-8-sig')==p.read_text(encoding='utf-8-sig'):continue
        except UnicodeError:pass
    actual=sha(original) if original.exists() else None
    assert actual==before,(rel,'changed outside staging since the snapshot')
    changes.append({'path':rel,'before':before,'after':after,'bytes':p.stat().st_size})
protected={p:h for p,h in baseline.items() if p.startswith('01_EXAM_READY/02_STARTING_TEMPLATES/') or p.startswith('02_ORIGINAL_MATERIALS/')}
for rel,expected in protected.items():assert sha(ROOT/rel)==expected,('protected original changed',rel)
assert not any(x['path'] in protected for x in changes)
report={'files':changes,'protectedFilesVerified':len(protected),'scope':'Maintained exam answers, question content pipeline, regenerated guide/search and recorded validation only.'}
(WORK/'publish-candidates.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'changedFiles':len(changes),'protectedFilesVerified':len(protected),'newFiles':sum(x['before'] is None for x in changes),'totalBytes':sum(x['bytes'] for x in changes)}))
for x in changes:
    if '/PORTAL/' not in x['path'] and '/exam-solutions/' not in x['path'] and '/scenario-native-logs/' not in x['path']:print(x['path'])
