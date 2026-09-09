from pathlib import Path
import json,hashlib
W=Path('90_WORKING_PROJECTS/QUESTION_REVIEW_20260908');R=W/'EXAM_HANDOFF';B=R/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS';M=B/'99_MAINTENANCE';G=B/'01_GUIDES_AND_INDEXES'
paths=[M/'QUESTION_REVIEWS.json',G/'QUESTION_REVIEW_REPORT.md',G/'PORTAL/exams/2024-09-16-q1.html',G/'PORTAL/assets/portal-data.js']
before='The other five2..4 button pairs converge.'
after='The other five parameter pairs, with both choices in 2..4, converge.'
for p in paths:
    s=p.read_text(encoding='utf-8');assert before in s,p
    p.write_text(s.replace(before,after),encoding='utf-8',newline='\n')
coverage=M/'SEARCH_COVERAGE.json';d=json.loads(coverage.read_text(encoding='utf-8'))
for entry in d['inventory']:
    if entry.get('hash') and R/entry['path'] in paths:entry['hash']=hashlib.sha256((R/entry['path']).read_bytes()).hexdigest()
coverage.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
p=M/'QUESTION_REVIEW_SCOPE_NOTES.json';d=json.loads(p.read_text(encoding='utf-8'))
rel='01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL/algorithms/index.html'
baseline=json.loads((W/'baseline.json').read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(R/rel)==baseline[rel] and sha(Path(rel))==baseline[rel]
d['preexistingBrowserTestAssumption']={'script':'BROWSER_SEARCH_QA.cjs','finding':'The broad browser script expects a data-filter=text control on algorithms/index.html, but that unchanged index uses the current static algorithm navigation. The script passes its exam-search checks before timing out there. BROWSER_QUESTION_REVIEW_QA.cjs covers the changed question pages and their exam/global search flows.','algorithmIndexUnchanged':True}
p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Polished one Kruskal sentence in the keyed source, page, report and existing search records; updated the report content hash.')
