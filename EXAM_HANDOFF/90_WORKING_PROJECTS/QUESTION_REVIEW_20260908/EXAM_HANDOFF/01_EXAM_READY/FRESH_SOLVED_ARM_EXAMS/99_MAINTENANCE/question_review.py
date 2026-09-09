"""Single question-keyed teaching source and revision-bound evidence for exam pages."""
from pathlib import Path
from html import escape
import csv, hashlib, json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GUIDES = HERE.parent / '01_GUIDES_AND_INDEXES'
SOURCE = HERE / 'QUESTION_REVIEWS.json'

def read_reviews(verify_evidence=True):
    reviews = json.loads(SOURCE.read_text(encoding='utf-8'))
    indexed = {r['question_id'] for r in csv.DictReader((GUIDES/'QUESTION_INDEX.csv').open(encoding='utf-8-sig'))}
    if set(reviews) != indexed:
        raise ValueError('Question reviews and QUESTION_INDEX.csv differ')
    for qid, r in reviews.items():
        for field in ('contract', 'method', 'trace', 'explanation', 'mistakes', 'sources', 'pages', 'findings'):
            if not r.get(field):
                raise ValueError(f'{qid}: missing {field}')
        if verify_evidence:
            for source, expected in r.get('sourceHashes', {}).items():
                if digest(ROOT/source) != expected:
                    raise ValueError(f'{qid}: stale review evidence for {source}; rerun the applicable checks')
    return reviews

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def assembly_dependency(r):
    if any(s.endswith('.s') for s in r['sources']):
        return None
    main = next((ROOT/s for s in r['sources'] if s.endswith('/main.c')), None)
    if main:
        for path in (main.with_name('assembly.s'), main.parent.parent/'assembly.s'):
            if path.exists():
                return path
    return None

def current_sources(r):
    paths = [ROOT/s for s in r['sources']]
    dependency = assembly_dependency(r)
    if dependency: paths.append(dependency)
    return paths

def ordered(lines):
    return '<ol>'+''.join('<li>'+escape(x)+'</li>' for x in lines)+'</ol>'

def unordered(lines):
    return '<ul>'+''.join('<li>'+escape(x)+'</li>' for x in lines)+'</ul>'

def render(r, code, pdf_link, related, notes_link=''):
    e=escape
    limitations = unordered(r['limitations']) if r['limitations'] else '<p>No additional ambiguity found within the stated input contract.</p>'
    top = ''
    if 'unresolved' in r['reviewStatus'].lower() or 'conflicting' in r['reviewStatus'].lower():
        top = '<section class="section-block"><h2>Known correctness limitation</h2>'+limitations+'</section>'
    evidence = r.get('verification', {})
    tests = []
    for key, title in [('sourceReview','Source review'), ('instructionExecution','Assembly instruction execution'), ('peripheralExecution','C event-sequence checks'), ('nativeBuild','Native build'), ('physicalBoard','Physical board')]:
        value=evidence.get(key, {'status':'UNVERIFIED','detail':'No evidence recorded for this revision.'})
        if isinstance(value,str): value={'status':'UNVERIFIED','detail':value}
        tests.append('<h3>'+title+' — '+e(value['status'])+'</h3><p>'+e(value.get('detail',''))+'</p>'+unordered(value.get('cases',[])))
    integration = unordered(r.get('integration', []))
    return (top+'<section class="section-block"><p>'+e(r['reviewStatus'])+'</p><h2>Exact contract</h2><p>'+e(r['contract'])+'</p>'+pdf_link+'</section>'
        +'<section class="section-block"><h2>Solution reasoning</h2>'+ordered(r['method'])+'<h2>Worked trace</h2>'+ordered(r['trace'])+'</section>'
        +'<section class="section-block"><h2>Install the answer in the current template</h2>'+integration+notes_link+'</section>'
        +'<section class="section-block">'+code+'</section>'
        +'<section class="section-block"><h2>Code explanation</h2>'+unordered(r['explanation'])+'<h2>Complexity and memory</h2><p>'+e(r['complexity'])+'</p><h2>Relevant mistakes</h2>'+unordered(r['mistakes'])+'</section>'
        +'<section class="section-block"><h2>Paper interpretation and limits</h2>'+limitations+'<h2>Review findings and corrections</h2>'+unordered(r['findings'])+'</section>'
        +'<section class="section-block"><h2>Validation evidence for this answer</h2>'+''.join(tests)+'</section>'
        +'<section class="section-block"><h2>Related handbook pages</h2>'+related+'</section>')

def finalize():
    reviews=read_reviews(verify_evidence=False)
    assembly=json.loads((HERE/'QUESTION_EXECUTION_RESULTS.json').read_text(encoding='utf-8'))
    peripherals=json.loads((HERE/'QUESTION_PERIPHERAL_RESULTS.json').read_text(encoding='utf-8'))
    builds=json.loads((HERE/'QUESTION_NATIVE_BUILDS.json').read_text(encoding='utf-8'))
    assert len(reviews)==48 and set(builds)==set(reviews)
    for qid,r in reviews.items():
        r['reviewedOn']='2026-09-08'
        paths=current_sources(r)
        r['sourceHashes']={p.relative_to(ROOT).as_posix():digest(p) for p in paths}
        r['paperSha256']=digest(ROOT/r['paper'])
        native=builds[qid]
        assert native['status']=='PASS',(qid,native)
        # Bind the build result to the actual installed answer, including Q1 dependencies.
        for p in paths:
            suffix='Source\\sample.c' if p.name=='main.c' else 'Source\\ASM_funct.s' if p.suffix=='.s' else None
            matches=[h for name,h in native['sources'].items() if name==suffix or (suffix is None and name.endswith('\\'+p.name))]
            assert matches==[digest(p)],(qid,p,matches)
        check=next((x for x in assembly.values() if x.get('source') in r['sourceHashes'] and x.get('sourceSha256')==r['sourceHashes'][x['source']]),None)
        asm_e={'status':'UNVERIFIED','detail':'No matching instruction-execution result for the current source.'}
        if check:
            assert check['status']=='PASS',(qid,check)
            asm_e={'status':'PASS','detail':'Native ARMASM syntax was checked separately. Unicorn executed the delivered instruction stream after translating assembler directives and assembling with LLVM. Public function checks include returned values, memory effects, R4–R11 preservation and stack balance; the SVC live-R6 output is an explicit exception. Isolated Reset_Handler execution is reported only where listed below. Hardware reset-vector entry, system startup and physical exception entry remain unverified.','cases':check['cases']}
        c_e={'status':'NOT APPLICABLE','detail':'This question has no C peripheral answer.'}
        if any(p.suffix=='.c' for p in paths):
            check=peripherals[qid];assert check['status']=='PASS',(qid,check)
            assert all(r['sourceHashes'].get(s)==h for s,h in check['sourceHashes'].items()),qid
            c_e={'status':'PASS','detail':check['limits']+' The final foreground loop is stepped explicitly; API calls and assembly computations are mocked. This checks the C state transitions separately from the assembly algorithm.','cases':check['cases']}
        r['verification']={
            'sourceReview':{'status':'COMPLETE','detail':'Original PDF text and relevant diagrams were compared with the maintained answer, public interface, index and explanation. Findings and interpretation choices are recorded above.'},
            'instructionExecution':asm_e,'peripheralExecution':c_e,
            'nativeBuild':{'status':'PASS','detail':'Arm Compiler 6.22 / MDK 5.41 compiled and linked the SW_Debug target in an isolated copy of the current Official Combined Exam API template. Answer files were installed and duplicate IRQ definitions removed in that copy. This proves this build configuration only; it does not prove execution or timing.'},
            'physicalBoard':{'status':'UNVERIFIED','detail':'No physical-board testing was performed. Clock accuracy, button bounce, analog output and real interrupt latency remain unverified.'}}
        r['integration']=[]
        for p in paths:
            if p.name=='main.c':target='Source/sample.c'
            elif p.suffix=='.s':target='Source/ASM_funct.s'
            else:
                matches=list((ROOT/'01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/Source').rglob(p.name));assert len(matches)==1
                target=matches[0].relative_to(ROOT/'01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API').as_posix()
            r['integration'].append(f'Replace {target} with the complete {p.name} download shown below.')
        handlers=sorted({name for p in paths if p.suffix=='.c' for name in re.findall(r'\bvoid\s+(\w+_IRQHandler)\s*\(',p.read_text(encoding='utf-8-sig'))})
        for name in handlers:
            duplicates=[]
            for p in (ROOT/'01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API/Source').rglob('*.c'):
                if p.name in {x.name for x in paths if x.name.startswith('IRQ_')}:continue
                if re.search(r'\bvoid\s+'+name+r'\s*\(',p.read_text(encoding='utf-8-sig')):duplicates.append(p.relative_to(ROOT/'01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API').as_posix())
            if duplicates:r['integration'].append(f'Remove the existing {name} function from '+', '.join(duplicates)+'. The supplied answer owns that handler; retain the other functions in those files.')
        if any('EXPORT  Reset_Handler' in p.read_text(encoding='utf-8-sig') or re.search(r'EXPORT\s+Reset_Handler',p.read_text(encoding='utf-8-sig')) for p in paths if p.suffix=='.s'):
            r['integration'].append('Keep the template vector table and its weak Reset_Handler. The supplied strong Reset_Handler replaces it at link time. Do not add another strong reset handler.')
        if assembly_dependency(r):r['integration'].append('The assembly download is the computation dependency from Q1. The paper’s additional task here is the C implementation.')
        r['integration'].append('Use a copy of the clean template. The build verifier follows these placement and handler-ownership steps; it never edits the clean template.')
    SOURCE.write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Review of all 48 published exam questions','',
        'Reviewed September 8, 2026. Each record maps the original paper to maintained sources, the published answer, findings, tests and explicit limitations. The JSON teaching source is QUESTION_REVIEWS.json in 99_MAINTENANCE.','',
        f'Native SW_Debug builds: {len(builds)}/48 passed. Independent assembly result records: {len(assembly)} passed; identical source hashes can support dependent questions. C event-sequence fixtures: {len(peripherals)} passed. No physical-board tests were performed.','',
        'The original Kruskal procedure has four nonconvergent valid parameter pairs. The corresponding answers detect failure and report partial results; they do not claim a completed maze. The SDIV64S page records the conflict between the printed V formula and the prose description. The shortest-path page documents the distance-32 encoding limit.','',
        '## Reproduce the checks','',
        'Run VERIFY_EXAM_ANSWERS.py (ARMASM syntax and LLVM/Unicorn instruction checks), VERIFY_EXAM_PERIPHERALS.py (actual C with explicit mocks), and BUILD_EXAM_REVIEW_PROJECTS.py (native SW_Debug compile/link) from 99_MAINTENANCE. The scripts require the installed toolchains and Python dependencies. Then run question_review.py and REFRESH_QUESTION_REVIEWS.py. Use staging and the portal verifiers before publishing.','',
        'Native logs are scenario-native-logs/question-<question id>.log. QUESTION_NATIVE_BUILDS.json records installed source hashes; QUESTION_EXECUTION_RESULTS.json and QUESTION_PERIPHERAL_RESULTS.json record cases and source hashes. These are separate kinds of evidence.','']
    for qid,r in reviews.items():
        route='PORTAL/exams/'+qid.lower().replace('_','-')+'.html'
        lines+=['## '+qid,'',f'**{r["reviewStatus"]}.** [Open question]({route})','',
            f'Original: [{Path(r["paper"]).name}](../../../{r["paper"].replace(" ","%20")}#page={r["pages"][0]}); pages '+', '.join(map(str,r['pages']))+'.','',
            '**Contract:** '+r['contract'],'','**Findings:**','']+['- '+x for x in r['findings']]+['','**Maintained answer files:**','']
        lines+=['- ['+p+'](../../../'+p.replace(' ','%20')+')' for p in r['sourceHashes']]
        lines+=['','**Evidence:**','']
        for key,value in r['verification'].items():lines+=['- '+key+': '+value['status']+'. '+value['detail']]+['  - '+x for x in value.get('cases',[])]
        lines+=['','**Limitations:**','']+(['- '+x for x in r['limitations']] or ['- No additional ambiguity within the stated contract.'])+['']
    (GUIDES/'QUESTION_REVIEW_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'questions':len(reviews),'nativeBuilds':len(builds),'assemblyRecords':len(assembly),'CFixtures':len(peripherals)}))

if __name__=='__main__':finalize()
