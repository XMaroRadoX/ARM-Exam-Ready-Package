"""Validate search source coverage, relationships, and movable local links."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import csv,json,re,hashlib
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
BASE=ROOT/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS'; PORTAL=BASE/'01_GUIDES_AND_INDEXES/PORTAL'
raw=(PORTAL/'assets/portal-data.js').read_text(encoding='utf-8'); items=json.loads(raw.removeprefix('window.ARM_PORTAL_DATA=').rstrip(';\n'))['items']
coverage=json.loads((HERE/'SEARCH_COVERAGE.json').read_text(encoding='utf-8'))
checks=0

def check(ok,message):
    global checks
    checks+=1
    if not ok: raise AssertionError(message)

catalog={i['id']:i for i in items}; identities=[i for item in items for i in [item]+item.get('alternateSources',[]) if 'id' in i]
check(len({i['id'] for i in identities})==len(identities),'Unique source identities')
with (BASE/'01_GUIDES_AND_INDEXES/QUESTION_INDEX.csv').open(encoding='utf-8-sig',newline='') as stream:
    questions=list(csv.DictReader(stream))
for q in questions:
    key='question-'+re.sub('[^a-z0-9]+','-',q['question_id'].lower()).strip('-'); item=catalog[key]
    for column,field in [('interrupt_tags','interrupts'),('peripheral_tags','peripherals'),('timing_tags','timing'),('architecture_tags','architecture'),('algorithm_tags','algorithms')]:
        expected={t.strip() for t in re.split('[|;]',q[column]) if t.strip()}
        check(expected==set(item[field]),f'{key}: tags lost or invented in {field}')
    check(all(t in item['components'] for t in item['interrupts']),key+': interrupt filters')
    check(item['metadataScope']=='Question',key+': question tag scope')
    check(bool(item['paperRoute']) and bool(item['solutionRoutes']),key+': paper/answer relationships')
for item in identities:
    for route in [item['route']]+item.get('solutionRoutes',[])+item.get('scopeRoutes',[])+([item['paperRoute']] if item.get('paperRoute') else []):
        parts=urlsplit(route); target=(PORTAL/unquote(parts.path)).resolve()
        check(not parts.scheme and target.is_relative_to(ROOT),f'Nonportable path: {route}')
        check(target.is_file(),f'Missing target: {route}')
        if parts.fragment and target.suffix.lower() in {'.html','.htm'}:
            check('id="'+unquote(parts.fragment)+'"' in target.read_text(encoding='utf-8',errors='replace'),f'Missing anchor: {route}')
    check(not item.get('sourcePath','').startswith('90_WORKING_PROJECTS/'),'Working copy indexed')
    if item.get('materialType')=='Original paper' and item.get('examId'):
        check(item.get('metadataScope')=='Whole paper' and not item.get('question'),'Unverified PDF question tags')
inventory={entry['path']:entry for entry in coverage['inventory']}
for folder in ['01_EXAM_READY','02_ORIGINAL_MATERIALS','03_ADDITIONAL_STUDY_MATERIAL']:
    for p in (ROOT/folder).rglob('*'):
        if not p.is_file() or '99_MAINTENANCE' in p.parts or p.is_relative_to(PORTAL/'assets'): continue
        relative=p.relative_to(ROOT).as_posix()
        check(relative in inventory,'Unaccounted source: '+relative)
for entry in coverage['inventory']:
    p=ROOT/entry['path']
    if entry.get('hash'): check(hashlib.sha256(p.read_bytes()).hexdigest()==entry['hash'],'Stale source: '+entry['path'])
check(coverage['reviewedExams']==23 and coverage['reviewedQuestions']==48,'Reviewed exam coverage')
check(len(items)==coverage['catalogRecords']+coverage['sectionRecords'],'Corpus count')
check(len(coverage['attachments'])>0,'Attachment coverage explicit')
check(len(coverage['unindexed'])>=2,'Retain PDF extraction limitations')
report={'status':'PASS','checks':checks,'records':len(items),'sourceIdentities':len(identities),'inventoriedFiles':len(inventory),'reviewedExams':23,'reviewedQuestions':48,'attachments':len(coverage['attachments']),'unmappedExamSources':len(coverage['unmappedMaterial'])}
(HERE/'SEARCH_INTEGRITY_RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
