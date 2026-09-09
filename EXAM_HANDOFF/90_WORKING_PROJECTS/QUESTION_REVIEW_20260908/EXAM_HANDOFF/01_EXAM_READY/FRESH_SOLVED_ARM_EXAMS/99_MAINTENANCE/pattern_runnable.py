"""Explicit pattern/project mapping, complete source generation and page coverage."""
from pathlib import Path
import csv, hashlib, json, re, shutil, xml.etree.ElementTree as ET
from urllib.parse import unquote
from pattern_board_projects import board_projects
from pattern_foundations import entries as foundations, SVC_MAIN, SVC_ASM
from legacy_algorithm_tests import entries as legacy_entries
from pattern_teaching import PATTERNS, WORKFLOWS

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
TEMPLATE=ROOT/'01_EXAM_READY/02_STARTING_TEMPLATES/Official Combined Exam API'
LIBRARY=ROOT/'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS'
OUT=LIBRARY/'03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/pattern-projects'

ALGORITHM_MAP={
 'Signed and unsigned array sorting':'pat-alg-selection-sort-001',
 'Bounded recurrence into an array':'pat-alg-indirect-recurrence-001',
 'Matrix and graph traversal':'pat-alg-bfs-001',
 
 'Fixed-point multiply and recurrence':'foundation-q15',
 'Nested loops with preserved outer state':'foundation-pair',
 'Balanced early exit from inner search':'foundation-pair',
 'Signed and unsigned byte arrays':'foundation-matrix-byte',
 'Word-array traversal':'foundation-word-max',
 'Row-major matrix addressing':'foundation-matrix-byte',
 'Four-register argument contract':'foundation-pair',
 'Fifth and later arguments':'foundation-sum7',
 'Non-leaf prologue and epilogue':'foundation-nonleaf',
 'APSR flag contract':'foundation-flags',
 'Register preservation and stack safety':'foundation-sum7',
}
BOARD_MAP={
 'Frequency-count comparison':['game-bulls-cows','game-mastermind'],
 'SVC immediate decoding':['svc-frame'],
 'MSP/PSP exception-frame selection':['svc-frame'],
 'Timer setup and ownership':['timer-periodic','timer-one-shot','timer-pause-resume','timer-exact-ticks','timer-multiple-matches','timer-capture-pin'],
 'GPIO event capture':['buttons-rit-timer','buttons-systick-timer','raw-capture-ff','ordered-binary','ordered-parameters'],
 'Joystick event state machine':['game-bulls-cows','game-mastermind','joystick-release','rhythm-first-movement'],
 'ADC sample conversion':['adc-button-sequence','adc-percentage'],
 'DAC table streaming':['dac-stream','dac-button-once','dac-duration','dac-three-timer-notes'],
 'ISR-to-foreground event loop':['event-handoff','buttons-rit-timer'],
 'Deterministic debounce':['buttons-rit-timer','buttons-systick-timer'],
 'Periodic match scheduling':['timer-periodic','timer-multiple-matches','dac-duration'],
 'Free-running timer seed':['raw-capture-ff','raw-capture-ffff'],
 'Atomic ISR event handoff':['event-handoff','ordered-binary'],
 'Exclusive interrupt-vector ownership':['buttons-rit-timer','dac-duration','svc-frame'],
 'Question prose to a contract':['ordered-binary'],
 'Assembly stub to real integration':['algorithm-foundation-word-max-assembly'],
 'Multi-peripheral ownership plan':['buttons-rit-timer','dac-duration'],
 'Event flags counters and queues':['event-handoff','timer-periodic','ordered-binary','algorithm-pat-ds-ring-buffer-001-c'],
 'Restart and persistent state':['game-bulls-cows'],
 'Adapt a partial pattern match':['algorithm-foundation-matrix-byte-assembly','algorithm-foundation-matrix-signed-byte-assembly'],
 'Build recovery and submission':['buttons-rit-timer'],
}

EXAM_PROJECTS={
 'game-bulls-cows':('2026-06-25_ARM1_BullsAndCows','Bulls-and-Cows: DOWN, LEFT, RIGHT, UP edit digits0,1,2,3 respectively. SELECT submits, shows, and begins the next guess while retaining the secret; four correct digits finish the game.','First SELECT captures Timer1 seed; edit four digits; SELECT evaluates; next SELECT resets guess only. Follow display_guess and increment_digit for the exact mapping.'),
 'game-mastermind':('2026-06-25_ARM2_Mastermind','Mastermind mapping and persistent game state.','UP, RIGHT, DOWN, LEFT edit digits0,1,2,3 respectively. First SELECT captures the secret; later SELECT submits. After a losing result, SELECT clears the guess while retaining the secret.'),
 'rhythm-first-movement':('2025-07-01_ARM1_LCG_Rhythm','First movement per interval; later movements deliberately ignored.','Keep the source timer threshold and IRQ algorithm call. The first movement consumes the active interval; do not replay ignored movements.'),
 'dac-three-timer-notes':('2026-02-18_ARM1_Three_Timers','Three-timer note sequencing with exact paper thresholds.','Timer A skips its tick while B or C runs; B writes one DAC sample; C stops B. Source constants and argument order are retained.'),
}

def algorithm_entries():
    entries={e['slug']:e for e in [*legacy_entries(),*foundations()]}
    # Derive the unsigned comparison variant from the maintained signed sort.
    e=entries['pat-alg-selection-sort-001'];asm=e['assembly']
    asm=re.sub(r'\bit\s+lt\b','it lo',asm);asm=re.sub(r'\bmovlt\b','movlo',asm)
    entries['selection-sort-unsigned']=dict(slug='selection-sort-unsigned',code=re.sub(r'\bint32_t\b','uint32_t',e['code']),assembly=asm,test='''#include <stdint.h>
void pat_alg_selection_sort_001(uint32_t*,uint32_t);
int test_main(void){uint32_t a[]={0xFFFFFFFFu,0,0x80000000u,7};pat_alg_selection_sort_001(a,4);CHECK(a[0]==0 && a[1]==7 && a[2]==0x80000000u && a[3]==0xFFFFFFFFu);pat_alg_selection_sort_001(a,0);CHECK(a[3]==0xFFFFFFFFu);return 0;}''',source=e['source'])
    return entries

def all_specs():
    specs=board_projects()
    specs['svc-frame']=dict(code=SVC_MAIN,assembly=SVC_ASM,purpose='SVC #7 with MSP/PSP frame selection and a C dispatcher.',actions='Debugger: svc_result=7 and returned=8. Assembly owns SVC_Handler; EXAM_ENABLE_SVC_HANDLER stays0.',resources=['SVC_Handler selects stacked MSP/PSP frame and tail-calls API decoder'])
    specs['event-handoff']=dict(code='''#include "exam_api.h"
volatile uint32_t consumed;
void TIMER0_IRQHandler(void){uint32_t f=exam_timer_ack(EXAM_TIMER0);if(exam_timer_match_happened(f,0u))exam_events_set(1u);}
int main(void){exam_init();if(exam_timer_config_ms(EXAM_TIMER0,500u,EXAM_TIMER_PERIODIC)!=EXAM_OK)for(;;){}exam_timer_start(EXAM_TIMER0);for(;;){if(exam_events_take(1u)){++consumed;exam_led_write((uint8_t)consumed);}}}
''',assembly='        END\n',purpose='A pending-work bit consumed in foreground.',actions='One or more IRQs before take produce one request. Three delayed identical events are not a count of3. Use direct command handling when every identity matters.',resources=['Timer0:500ms producer','main: atomic take and foreground display'])
    # Resolve exact named maintained answers; do not select a first related exam.
    answer_root=ROOT/'03_ADDITIONAL_STUDY_MATERIAL/03 - Solved Exams'
    index=list(csv.DictReader((LIBRARY/'01_GUIDES_AND_INDEXES/CURRENT_TEMPLATE_SOLUTION_INDEX.csv').open(encoding='utf-8-sig')))
    for key,(name,purpose,actions) in EXAM_PROJECTS.items():
        folder=answer_root/name/'Answer Source'
        if not folder.exists():
            raise ValueError('Explicit exam source missing: '+str(folder))
        code=(folder/'main.c').read_text();assembly=(folder/'assembly.s').read_text()
        specs[key]=dict(code=code,assembly=assembly,purpose=purpose,actions=actions,resources=({'game-bulls-cows':['Timer1:MR0=UINT32_MAX,PR0,no match IRQ; seed on first SELECT','RIT:10ms input sampling; RIT_IRQHandler publishes edges; main owns rounds'], 'game-mastermind':['Timer1:MR0=UINT32_MAX,PR0,no match IRQ; seed on first SELECT','RIT:10ms input sampling; RIT_IRQHandler publishes edges; main owns rounds'], 'rhythm-first-movement':['Timer0:3000ms; TIMER0_IRQHandler calls nextElementLCG and opens one movement window','RIT:10ms; RIT_IRQHandler handles first movement immediately'], 'dac-three-timer-notes':['Timer0 A:50ms; TIMER0_IRQHandler starts a note only when B and C stopped','Timer1 B:periodic waveform threshold from5351..1062; TIMER1_IRQHandler advances45-sample table','Timer2 C:one-shot duration threshold from(40000000..625000)/5; TIMER2_IRQHandler stops B']})[key],source=str(folder.relative_to(ROOT)))
    for key,e in algorithm_entries().items():
        for language in ('c','assembly'):
            test=e['test']
            if '#define CHECK' not in test:test='#define CHECK(x) do { if (!(x)) return __LINE__; } while (0)\n'+test
            code='#include "exam_api.h"\n'+test+'''\nvolatile int pattern_result;
int main(void){exam_init();pattern_result=test_main();exam_led_write(pattern_result?0xFFu:0x01u);for(;;){}}
'''
            specs[f'algorithm-{key}-{language}']=dict(code=code,assembly=e['assembly'] if language=='assembly' else '        END\n',reference=e['code'] if language=='c' else None,purpose=f"{key}: complete {language} implementation and executable cases.",actions='Run once: pattern_result=0 and LED mask0x01 means all included cases passed; otherwise pattern_result identifies the failed fixture line and LEDs show0xFF. Inspect test_main for exact inputs and results.',resources=['No periodic interrupts; main calls test_main once','Algorithm uses only the explicitly declared inputs and scratch storage'],entry=e,source=e.get('source','pattern_foundations.py'))
    # buttons_init enables all three EINT sources. Unused buttons still need
    # acknowledgement owners, otherwise they enter the startup default loop.
    for spec in specs.values():
        if 'exam_buttons_init(' in spec['code']:
            for i,button in enumerate(('INT0','KEY1','KEY2')):
                if not re.search(r'void\s+EINT'+str(i)+r'_IRQHandler\s*\(',spec['code']):
                    spec['code']+='\nvoid EINT'+str(i)+'_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_'+button+'); }\n'
    return specs

IRQ_FILES=['button_EXINT/IRQ_button.c','timer/IRQ_timer.c','RIT/IRQ_RIT.c','systick/IRQ_systick.c','adc/IRQ_adc.c']
def write_project(key,spec,clean,reuse=False):
    project=OUT/key
    if not reuse:
        def copy_changed(source,destination):
            if not Path(destination).is_file() or Path(source).read_bytes()!=Path(destination).read_bytes():
                return shutil.copy2(source,destination)
            return str(destination)
        shutil.copytree(TEMPLATE,project,dirs_exist_ok=True,copy_function=copy_changed,ignore=shutil.ignore_patterns('Objects','Listings','*.uvguix.*','*.bak','*.log','*.axf','*.htm'))
    files={'Source/sample.c':spec['code'],'Source/ASM_funct.s':spec['assembly']}
    files.update({'Source/'+p:'/* Handlers owned by Source/sample.c or Source/ASM_funct.s. */\n' for p in IRQ_FILES})
    if spec.get('reference') is not None:files['Source/reference.c']=spec['reference']
    files.update(spec.get('extra_files',{}))
    if reuse:
        for name,code in files.items():
            if not (project/name).exists() or (project/name).read_text(encoding='utf-8')!=clean(code,key):
                raise ValueError('Project source changed; regenerate before reusing: '+key+'/'+name)
        for source in (TEMPLATE/'Source').rglob('*'):
            if not source.is_file():continue
            name=str(source.relative_to(TEMPLATE)).replace('\\','/')
            if name not in files and source.read_bytes()!=(project/name).read_bytes():
                raise ValueError('Shared template source changed; regenerate: '+key+'/'+name)
        return files
    for name,code in files.items():
        text=clean(code,key);(project/name).parent.mkdir(parents=True,exist_ok=True);(project/name).write_text(text,encoding='utf-8')
    if spec.get('reference') is not None:
        path=project/'sample.uvprojx';tree=ET.parse(path)
        for groups in tree.findall('.//Target/Groups'):
            group=ET.SubElement(groups,'Group');ET.SubElement(group,'GroupName').text='Pattern reference'
            f=ET.SubElement(ET.SubElement(group,'Files'),'File')
            for tag,value in [('FileName','reference.c'),('FileType','1'),('FilePath','.\\Source\\reference.c')]:ET.SubElement(f,tag).text=value
        tree.write(path,encoding='utf-8',xml_declaration=True)
    if spec.get('extra_files'):
        path=project/'sample.uvprojx';tree=ET.parse(path)
        for groups in tree.findall('.//Target/Groups'):
            group=ET.SubElement(groups,'Group');ET.SubElement(group,'GroupName').text='Scenario support'
            files_node=ET.SubElement(group,'Files')
            for filename in spec['extra_files']:
                if not filename.endswith('.c'):continue
                f=ET.SubElement(files_node,'File')
                for tag,value in [('FileName',Path(filename).name),('FileType','1'),('FilePath','./'+filename)]:ET.SubElement(f,tag).text=value
        tree.write(path,encoding='utf-8',xml_declaration=True)
    readme=['# '+key,'',spec['purpose'],'','## Run and inspect','',spec['actions'],'','## Resource ownership','']+['- '+r for r in spec['resources']]+['','## Files to replace','','Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.']+['- '+p for p in files]
    if spec.get('reference') is not None:readme+=['','Add Source/reference.c to the project target when adapting manually.']
    (project/'README.md').write_text('\n'.join(readme)+'\n')
    return files

def project_label(key):
    label=re.sub(r'^algorithm-', '', key)
    label=re.sub(r'pat-(?:alg|ds|mem|data)-', '', label).replace('-001','').replace('foundation-','')
    return label.replace('-', ' ')

def install(c):
    previous=c['build_patterns']
    def build(rows,exams,solutions,items):
        links=previous(rows,exams,solutions,items)
        specs=all_specs();mapping={}
        for row in rows:
            title=row['title']
            if title in BOARD_MAP:mapping[title]=BOARD_MAP[title]
            else:
                key=ALGORITHM_MAP.get(title)
                if key is None:
                    path=unquote(row['c_source'])
                    match=re.search(r'/(PAT-[^/]+)/c/reference\.c$',path)
                    if not match:raise ValueError('Missing explicit implementation mapping: '+title)
                    key=match.group(1).lower()
                mapping[title]=[f'algorithm-{key}-assembly',f'algorithm-{key}-c']
        mapping.update({title:BOARD_MAP[title] for title,*_ in WORKFLOWS})
        mapping['Signed and unsigned array sorting'] += ['algorithm-selection-sort-unsigned-assembly','algorithm-selection-sort-unsigned-c']
        mapping['Signed and unsigned array sorting'] += ['algorithm-foundation-byte-sort-assembly','algorithm-foundation-byte-sort-c','algorithm-foundation-byte-sort-unsigned-assembly','algorithm-foundation-byte-sort-unsigned-c']
        mapping['Signed and unsigned byte arrays'] += ['algorithm-foundation-matrix-signed-byte-assembly','algorithm-foundation-matrix-signed-byte-c']
        used={p for projects in mapping.values() for p in projects}
        built={key:write_project(key,specs[key],c['clean_algorithm_code'],c.get('reuse_pattern_projects',False)) for key in sorted(used)}
        coverage=[]
        for title,keys in mapping.items():
            dest=links[title];body='<section class="section-block" data-runnable-pattern><h2>Complete runnable baseline and variants</h2>'
            body+='<nav class="contents" aria-label="Runnable variants">'+''.join('<a href="#variant-'+str(i)+'">'+c['esc'](project_label(key))+'</a>' for i,key in enumerate(keys))+'</nav>'
            record=dict(title=title,technique=PATTERNS[title]['use'],workedCase=PATTERNS[title]['trace'],projects=[])
            for i,key in enumerate(keys):
                spec=specs[key];folder=OUT/key;files=built[key]
                symbols=re.findall(r'(?m)^\s*EXPORT\s+(\w+)',spec['assembly'])
                funcs=re.findall(r'\b(?:void|int|uint\d+_t|int\d+_t)\s+(\w+)\s*\([^;{}]*\)\s*\{',spec['code'])
                body+=f'<h3 id="variant-{i}">{"Baseline" if i==0 else "Variant"}: {c["esc"](project_label(key))}</h3><p>{c["esc"](spec["purpose"])}</p><p>{c["esc"](spec["actions"])}</p>'
                body+=c['href'](folder/'sample.uvprojx',dest,'Open complete Keil project')+' · '+c['href'](folder/'README.md',dest,'Exact replacement instructions')
                body+='<table><thead><tr><th>Resource and owner</th></tr></thead><tbody>'+''.join('<tr><td>'+c['esc'](r)+'</td></tr>' for r in spec['resources'])+'</tbody></table>'
                body+='<p>Entry: main. Relevant functions: '+c['esc'](c['clean_algorithm_code'](', '.join(funcs+symbols),key))+'. All final files follow; keep a single definition of each IRQ.</p>'
                hashes={}
                for filename in files:
                    p=folder/filename;text=p.read_text(encoding='utf-8');hashes[filename]=hashlib.sha256(p.read_bytes()).hexdigest()
                    body+=c['details_code'](filename,text,p,dest,'Assembly' if p.suffix=='.s' else 'C',filename.endswith('sample.c'))
                record['projects'].append(dict(id=key,path=str(folder.relative_to(ROOT)),entry='main',symbols=c['clean_algorithm_code'](','.join(funcs+symbols),key).split(','),files=hashes,dependencies=['maintained template peripheral libraries','startup_LPC17xx.s'],resources=spec['resources'],expected=spec['actions'],test='test_main' if spec.get('entry') else 'peripheral scenario; see validation report',verificationReports=['PATTERN_NATIVE_BUILDS.json','PATTERN_ALGORITHM_RESULTS.json','PERIPHERAL_HELPER_VALIDATION.json','PATTERN_FLOW_RESULTS.json']))
            from peripheral_helper_docs import TIMER_BEHAVIOUR
            if any('Timer' in r for key in keys for r in specs[key]['resources']):
                body+='<h2>Timer call effects</h2><table><thead><tr><th>Call</th><th>Counter</th><th>Configuration and interrupts</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+c['esc'](v)+'</td>' for v in row)+'</tr>' for row in TIMER_BEHAVIOUR)+'</tbody></table>'
            body+='</section>'
            from pattern_teaching import render
            old=dest.read_text(encoding='utf-8')
            refs=re.search(r'<section class="section-block"><h2[^>]*>Exams where it appeared</h2>.*?</section>',old,re.S)
            body='<section class="section-block">'+render(title,c['esc'])+'</section>'+body+(refs[0] if refs else '')
            c['write'](dest,c['page'](dest,title,PATTERNS[title]['use'],body,[('Home',c['HOME']),('Solution Patterns',c['PORTAL']/'patterns/index.html'),(title,dest)],'Solution Patterns'))
            coverage.append(record)
        (HERE/'PATTERN_COVERAGE.json').write_text(json.dumps(coverage,indent=2)+'\n')
        index=c['PORTAL']/'courses/pattern-projects.html'
        body='<section class="section-block"><h2>Complete projects for Solution Patterns</h2><p>Each project opens in the maintained Keil template. The linked pattern identifies its baseline, variants, inputs, expected result and exact replacement files.</p><table><thead><tr><th>Project</th><th>Pattern and instructions</th></tr></thead><tbody>'
        for key in sorted(used):
            title=next(t for t,keys in mapping.items() if key in keys)
            label=project_label(key)
            body+='<tr><td>'+c['href'](OUT/key/'sample.uvprojx',index,label)+'</td><td>'+c['href'](links[title],index,title)+' · '+c['href'](OUT/key/'README.md',index,'Replacement files')+'</td></tr>'
        body+='</tbody></table></section>'
        c['write'](index,c['page'](index,'Complete pattern projects','Open the baseline or variant that fits the question.',body,[('Home',c['HOME']),('Courses',c['PORTAL']/'courses/index.html'),('Pattern projects',index)],'Courses'))
        items.append(dict(id='complete-pattern-projects',kind='Courses',title='Complete pattern projects',summary='Buildable baselines and variants with exact file replacement instructions',route=c['rel'](index,c['PORTAL']/'search.html'),examHistory='Extra practice',languages=['Both'],components=['Timer','Buttons','ADC','DAC','Joystick','Assembly'],topics=['Projects'],aliases=['complete examples'],relatedIds=[]))
        return links
    c['build_patterns']=build
