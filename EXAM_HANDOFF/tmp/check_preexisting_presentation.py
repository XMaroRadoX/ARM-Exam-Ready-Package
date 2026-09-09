from pathlib import Path
import hashlib,json,re
W=Path('90_WORKING_PROJECTS/QUESTION_REVIEW_20260908');R=W/'EXAM_HANDOFF'
B=json.loads((W/'baseline.json').read_text(encoding='utf-8'))
P=R/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL'
paths=list(P.rglob('technique-*.html'))+[P/'algorithms/fixed-point-multiply-and-recurrence.html']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
issues=[]
for p in paths:
    s=p.read_text(encoding='utf-8')
    if len(re.findall(r'<pre\b',s))==len(re.findall(r'class="copy-code\b',s)):continue
    rel=p.relative_to(R).as_posix()
    issues.append({'path':rel,'finding':'Existing presentation audit reports unequal listing and copy-control counts','unchangedFromBaseline':sha(p)==B[rel],'originalStillUnchanged':sha(Path(rel))==B[rel]})
assert len(issues)==16 and all(x['unchangedFromBaseline'] and x['originalStillUnchanged'] for x in issues),issues
(R/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/99_MAINTENANCE/QUESTION_REVIEW_SCOPE_NOTES.json').write_text(json.dumps({'preexistingOutsideQuestionScope':issues},indent=2)+'\n',encoding='utf-8')
print('All 16 presentation findings are unchanged, outside the reviewed question pages.')
