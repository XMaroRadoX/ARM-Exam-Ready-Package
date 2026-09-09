"""Complete board scenarios, classification, and exhaustive combination inventory.

Authoritative source; generated pages and projects are never edited manually.
"""
from pathlib import Path
from itertools import combinations
from urllib.parse import unquote, urlsplit
import csv, hashlib, json, re, zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
FAMILIES=('LED','Buttons','Joystick','Timer','RIT','SysTick','ADC','DAC')
PINS={'LED':'P2.0–P2.7: board labels LD11–LD4; byte display mask',
 'Buttons':'P2.10 INT0, P2.11 KEY1, P2.12 KEY2; active low',
 'Joystick':'P1.25 SELECT, P1.26 DOWN, P1.27 LEFT, P1.28 RIGHT, P1.29 UP; active low',
 'Timer':'Timer0: 10 ms status/control; Timer1: 8 kHz DAC samples when DAC is selected; no capture pins',
 'RIT':'10 ms input sampling; RIT_IRQHandler acknowledges the interrupt',
 'SysTick':'10 ms if primary clock; otherwise 100 ms supervisor counter; no peripheral acknowledgement',
 'ADC':'P1.31 / AD0.5 potentiometer; 0–4095; one conversion at a time',
 'DAC':'P0.26 / AOUT speaker; 0–1023; timed waveform with Timer1, static voltage otherwise'}
MODES=[
 ('counter',1,'Button up/down counter','Buttons LED','INT0 increments; KEY1 decrements; KEY2 resets; display wraps at 255.', 'Press INT0 twice with releases: 2. KEY1: 1. KEY2: 0.'),
 ('binary-entry',2,'Ordered binary entry','Buttons Joystick LED','KEY1 appends zero; joystick UP appends one; INT0 submits; ignore digits after 32.', 'UP, KEY1, KEY1, UP, UP, KEY1 with releases, INT0: 38.'),
 ('press-release-long',3,'Press, release and long-press actions','Buttons LED','INT0 press toggles bit 0; release toggles bit 1; 1 second hold toggles bit 2 once.', 'Hold INT0 for 150 steps: value 5. Release: 7. No repeated long action.'),
 ('stopwatch',4,'Stopwatch with pause and resume','Buttons LED','Elapsed hundredths advance only while running; INT0 pauses/resumes; KEY2 restarts.', '100 steps: 1 second; pause for 100 steps: no elapsed advance.'),
 ('countdown',5,'Countdown with latched timeout','Buttons LED','Count down from three seconds; pause with INT0; reset with KEY2; zero stays zero.', '300 steps: alarm 1, remaining 0; further steps cannot underflow.'),
 ('reaction',6,'Reaction time and false-start detection','Buttons LED','INT0 arms; one second later all LEDs light; KEY1 captures elapsed 10 ms units; early KEY1 is false start.', 'Arm; 100 total waiting steps open the window. KEY1 after 7 waiting-response steps records 7.'),
 ('movement',7,'Bounded joystick movement and hold repeat','Joystick LED','RIGHT increments position up to seven; LEFT decrements to zero; repeat begins at 500 ms, then every 100 ms.', 'RIGHT edge: 1; 49 more held steps: 2; sustained hold stops at 7.'),
 ('code-entry',8,'Four-command joystick code lock','Joystick LED','RIGHT, LEFT, RIGHT, LEFT encodes 0x66; SELECT checks and clears the input.', 'Correct four-command sequence then SELECT: 255; short or wrong sequence: 0.'),
 ('adc-percent',9,'Rounded potentiometer percentage','ADC LED','Scale the completed 12-bit ADC sample into rounded 0–100.', '0 => 0; 2048 => 50; 4095 => 100. No sample leaves the result unchanged.'),
 ('adc-hysteresis',10,'Threshold alarm with hysteresis','ADC LED','Latch on at 3000; clear at 2000; preserve the state between thresholds.', '3000 => on; 2500 => still on; 2000 => off; 2500 => still off.'),
 ('adc-average',11,'Eight-sample moving average','ADC LED','Average the samples received so far, then maintain an eight-element sliding window.', 'Eight 4095 samples => mean 4095; next zero => mean 3583; output 223.'),
 ('adc-capture',12,'Button capture of the latest completed sample','ADC Buttons LED','INT0 freezes the newest completed sample. Later pot changes update acquisition but not the captured result.', 'Sample 2048 then INT0 => result 2048; sample 4095 alone leaves result 2048.'),
 ('adc-rate',13,'Potentiometer-controlled blink interval','ADC LED','Map ADC to a bounded 50–1000 ms interval; retain elapsed progress when the setting changes.', 'ADC 0 selects five ticks; fifth tick toggles. ADC 4095 selects 100 ticks.'),
 ('audio-burst',14,'Button-triggered finite audio burst','Buttons Timer DAC LED','INT0 starts a 200 ms burst; active triggers are ignored; completion silences the DAC.', 'INT0 starts; 20 total control ticks stop output; release and press starts another burst.'),
 ('audio-controls',15,'Waveform selection, pause and restart','Buttons Joystick Timer DAC','INT0 pauses/resumes; RIGHT cycles sine, square, ramp; KEY2 resets application state.', 'RIGHT advances shape once; held RIGHT does not repeat. Paused output is zero.'),
 ('audio-sequence',16,'Notes separated by timed silence','Timer DAC LED','Play 200 ms, silence 100 ms, then advance through three sample-divider settings.', 'At tick 20 output stops; at tick 30 next note starts; phase wraps after three notes.'),
 ('adc-minmax',17,'Minimum and maximum sample monitor','ADC Buttons LED','Track extrema; INT0 selects minimum/maximum; KEY2 clears accumulated measurements.', 'Samples 1000,3000 => minimum 1000, maximum 3000; select changes the displayed statistic.'),
 ('adjustable-waveform',0,'Potentiometer-controlled waveform monitor','Buttons Joystick Timer ADC DAC LED','Potentiometer controls amplitude; INT0 pauses; KEY1/SELECT changes waveform; joystick LEFT/RIGHT adjusts display.', 'ADC 0 silences amplitude; 4095 reaches 1023; pause writes zero; reset clears application state.'),
]

def read_csv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def source_for(features,mode=0,poll=False):
    features=set(features)
    clock=2 if 'RIT' in features else 3 if 'SysTick' in features else 1 if 'Timer' in features else 0
    macros={'MODE':mode,'CONTROL_CLOCK':clock,'DEBOUNCE_STEPS':5 if clock else 1,'POLL_BUTTONS':int(poll or not clock)}
    macros.update({'HAS_'+x.upper():int(x in features) for x in FAMILIES})
    prefix=''.join(f'#define {k} {v}\n' for k,v in macros.items())
    return prefix+(HERE/'scenario_engine.c').read_text(encoding='utf-8'),clock

def practice_specs():
    result={}
    def add(key,title,features,mode,behavior,trace,group,poll=False):
        ordered=[f for f in FAMILIES if f in features]
        code,clock=source_for(ordered,mode,poll)
        timing='10 ms control clock; five consecutive changed samples confirm a transition (50 ms recipe).' if clock else 'Unpaced foreground polling. No elapsed-time or electrical debounce guarantee; use clean inputs.'
        result[key]=dict(code=code,assembly='        END\n',title=title,purpose=behavior,actions=trace,
          resources=[PINS[x] for x in ordered]+['Foreground: sole controller state owner; bounded FIFO of 31 usable snapshots; loss counter on overflow'],
          features=ordered,mode=mode,clock=clock,poll=poll,group=group,history='Additional practice',questions=[],
          timing=timing,states='Reset initializes running state, empty measurements, and zero display. Each confirmed input snapshot advances the described controller. KEY2 reset wins over simultaneous commands.',
          expected=trace,source='scenario_engine.c')
    for n in range(2,len(FAMILIES)+1):
        for subset in combinations(FAMILIES,n):
            key='mix-'+'-'.join(x.lower() for x in subset)
            desc='Compose a board monitor using '+', '.join(subset)+'. '
            desc+='INT0 toggles running and KEY1 selects the output mode. ' if 'Buttons' in subset else ''
            desc+='Joystick RIGHT/LEFT adjust the value and SELECT changes mode. ' if 'Joystick' in subset else ''
            desc+='ADC sets the value and analog amplitude. ' if 'ADC' in subset else ''
            desc+='LEDs show the low eight bits. ' if 'LED' in subset else ''
            desc+=('Timer1 streams an eight-sample waveform at 8 kHz. ' if 'Timer' in subset else 'DAC holds a static voltage; this combination makes no audio-frequency claim. ') if 'DAC' in subset else ''
            desc+='Inspect app, output_ticks and supervisor_ticks in the debugger for components without a visible output.'
            add(key,' + '.join(subset)+' monitor',subset,0,desc,'Reset: running=1, value=0. For available inputs: INT0 pauses; KEY2 resets; RIGHT increments; ADC 4095 sets value=255 and amplitude=1023. Release inputs between commands.','Combinations')
    for slug,mode,title,base,behavior,trace in MODES:
        for clock in ('RIT','SysTick'):
            features=set(base.split())|{clock}
            add('task-'+slug+'-'+clock.lower(),title+' — '+clock,features,mode,behavior,trace,'Worked applications')
        if 'Buttons' in base.split():
            add('task-'+slug+'-polling',title+' — sampled polling',set(base.split())|{'RIT'},mode,behavior,trace,'Worked applications',True)
    return result

def historical_specs(c):
    exams=c['read_csv'](c['COURSE']/'REVIEWED_EXAM_INDEX.csv')
    questions={q['question_id']:q for q in c['read_csv'](c['GUIDES']/'QUESTION_INDEX.csv')}
    manifest=json.loads((c['GENERATED_SOURCES']/'exam-solutions/manifest.json').read_text())
    answer_by_exam={}
    for answer in manifest['questions']:answer_by_exam.setdefault(answer['examId'],[]).append(questions[answer['questionId']])
    result={}
    for exam in exams:
        qs=[q for q in answer_by_exam[exam['exam_id']] if q['peripheral_tags'] or q['interrupt_tags'] or 'SVC' in q['requirement_summary'] or 'SysTick' in q['requirement_summary']]
        if not qs:continue
        folder=(c['ROOT']/exam['main_c']).parent
        text=(folder/'main.c').read_text(encoding='utf-8');assembly=(folder/'assembly.s').read_text(encoding='utf-8')
        tags='|'.join(q['peripheral_tags'] for q in qs)
        features=[f for f in FAMILIES if re.search(r'\b'+f+('\\d*' if f=='Timer' else '')+r'\b',tags)]
        notes=[]
        for name in ('EXAM_MAPPING.md','ADAPTATION_MAP.md','REVISION_REVIEW.md'):
            if (folder.parent/name).exists():notes.append((folder.parent/name).relative_to(c['ROOT']).as_posix())
        key='paper-'+c['slug'](exam['exam_id'])
        unused=[]
        if 'exam_buttons_init(' in text:
            unused=[i for i in range(3) if not re.search(r'void\s+EINT'+str(i)+r'_IRQHandler\s*\(',text)]
        extra_files={}
        if unused:
            support='#include "exam_api.h"\n/* Acknowledge enabled buttons unused by this paper. The answer source is unchanged. */\n'
            for i in unused:support+='void EINT'+str(i)+'_IRQHandler(void) { exam_button_ack(EXAM_BUTTON_'+('INT0','KEY1','KEY2')[i]+'); }\n'
            extra_files['Source/unused_buttons.c']=support
        if 'exam_systick_config' in text and 'SysTick_Handler' not in text+assembly:
            extra_files['Source/idle_systick.c']='/* The paper samples the SysTick counter; its enabled tick interrupt must return. */\nvoid SysTick_Handler(void) {}\n'
        result[key]=dict(code=text,assembly=assembly,extra_files=extra_files,title=exam['project'].replace('_',' '),purpose=' '.join(q['requirement_summary'] for q in qs),
          actions='Follow the exact input sequence and expected result in the linked original question and reviewed mapping.',
          resources=[q['question_id']+': '+q['function_or_handler']+'; '+q['argument_mapping']+'; '+q['constants'] for q in qs]+(['Unused enabled button vectors: acknowledge only in Source/unused_buttons.c; preserve the paper answer files.'] if unused else [])+(['SysTick counter-only use: Source/idle_systick.c owns a returning handler.'] if 'Source/idle_systick.c' in extra_files else []),
          features=features,group='Past exams',history='Appeared in past exams',questions=[q['question_id'] for q in qs],
          timing='; '.join(q['constants'] for q in qs),states='; '.join(q['requirement_summary'] for q in qs),
          source=folder.relative_to(c['ROOT']).as_posix(),paper=exam['source_pdf'],notes=notes,examId=exam['exam_id'])
    return result

FOUNDATION_TITLES={'Four-register argument contract','Fifth and later arguments','Non-leaf prologue and epilogue','APSR flag contract','Register preservation and stack safety','Signed and unsigned byte arrays','Word-array traversal','Row-major matrix addressing','Nested loops with preserved outer state','Balanced early exit from inner search','Assembly objects and exported symbols'}
GUIDE_TITLES={'Question prose to a contract','Assembly stub to real integration','Adapt a partial pattern match','Build recovery and submission'}

def classify(c,items):
    coverage=json.loads((HERE/'PATTERN_COVERAGE.json').read_text())
    inventory=json.loads((HERE/'ALGORITHM_INVENTORY.json').read_text())
    by_group={}
    for a in inventory:by_group.setdefault(a.get('source_group','').lower(),a['slug'])
    moves={};destinations={}
    for row in coverage:
        title=row['title'];old=c['PORTAL']/'patterns'/(c['slug'](title)+'.html')
        section='Solution Patterns';target=old
        if title in GUIDE_TITLES:section='Guides';target=c['PORTAL']/'guides'/('technique-'+old.name)
        elif title in FOUNDATION_TITLES:section='ASM Reference';target=c['PORTAL']/'asm'/('technique-'+old.name)
        elif title=='Frequency-count comparison':section='Algorithms';target=c['PORTAL']/'algorithms/consume-once-duplicate-safe-matching.html'
        elif all(p['id'].startswith('algorithm-') for p in row['projects']):
            section='Algorithms'
            group=re.sub(r'-(c|assembly)$','',row['projects'][0]['id'][10:])
            canonical=by_group.get(group)
            target=c['PORTAL']/'algorithms'/((canonical+'.html') if canonical else old.name)
        destinations[title]={'section':section,'route':c['rel'](target,c['PORTAL']/'search.html'),'projects':[p['id'] for p in row['projects']]}
        if target==old:continue
        text=old.read_text(encoding='utf-8')
        # Extract content only. Rebuild page chrome for the correct section.
        content=text.split('<div class="page-body">',1)[1].split('</main>',1)[0]
        content=content.rsplit('</div>',1)[0]
        content=rebase(content,old,target,{})
        namespace='method-'+old.stem+'-'
        for anchor in set(re.findall(r'\bid="([^"]+)"',content)):
            content=content.replace('id="'+anchor+'"','id="'+namespace+anchor+'"')
            content=content.replace('="#'+anchor+'"','="#'+namespace+anchor+'"')
        if section=='Algorithms' and target.stem in {a['slug'] for a in inventory}:
            current=target.read_text(encoding='utf-8')
            content='<section id="complete-project-method-'+old.stem+'"><h2>Complete projects and worked method</h2>'+content+'</section>'
            c['write'](target,current.replace('</main>',content+'</main>'))
        else:
            parent=target.parent/'index.html'
            c['write'](target,c['page'](target,title,row['technique'],content,[('Home',c['HOME']),(section,parent),(title,target)],section))
            index=parent.read_text(encoding='utf-8')
            c['write'](parent,index.replace('</main>','<section class="section-block">'+c['href'](target,parent,title)+'</section></main>'))
        moves[old.resolve()]=target
        for item in items:
            if urlsplit(item['route']).path==c['rel'](old,c['PORTAL']/'search.html'):
                item['route']=c['rel'](target,c['PORTAL']/'search.html');item['kind']=section
        body='<section class="section-block" data-compatibility-page><p>This material is now in '+c['esc'](section)+'.</p>'+c['href'](target,old,'Open '+title)+'</section>'
        c['write'](old,c['page'](old,title,'This bookmark remains available.',body,[('Home',c['HOME'])],section))
    (HERE/'SECTION_DESTINATIONS.json').write_text(json.dumps(destinations,indent=2)+'\n')
    return moves,destinations

def rebase(text,old,new,moves):
    import os
    def change(m):
        raw=m[2];url=urlsplit(raw)
        if url.scheme or url.netloc or not url.path:return m[0]
        resolved=(old.parent/unquote(url.path)).resolve();dest=moves.get(resolved,resolved)
        value=os.path.relpath(dest,new.parent).replace('\\','/')
        from urllib.parse import quote
        fragment=('method-'+resolved.stem+'-'+url.fragment) if resolved in moves and url.fragment else url.fragment
        value=quote(value,safe='/.-_')+('?' +url.query if url.query else '')+('#'+fragment if fragment else '')
        return m[1]+value+m[3]
    return re.sub(r'((?:href|src)=")([^"]+)(")',change,text)

def render_scenario(c,key,spec):
    from pattern_runnable import OUT,write_project
    try:
        files=write_project(key,spec,c['clean_algorithm_code'],reuse=True)
    except (ValueError,FileNotFoundError):
        files=write_project(key,spec,c['clean_algorithm_code'])
    folder=OUT/key;dest=c['PORTAL']/'patterns'/(key+'.html')
    archive=folder/(key+'.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file() and p!=archive and not any(x in p.parts for x in ('Objects','Listings')):z.write(p,p.relative_to(folder))
    link=lambda p,t:c['href'](p,dest,t)
    body='<section class="section-block"><p class="eyebrow">'+c['esc'](spec['history'])+'</p><h2>Problem and observable behavior</h2><p>'+c['esc'](spec['purpose'])+'</p><p>'+link(archive,'Download complete project ZIP')+' · '+link(folder/'sample.uvprojx','Open complete Keil project')+'</p>'
    body+='<h2>Resource and interrupt ownership</h2><table><thead><tr><th>Resource</th><th>Role</th></tr></thead><tbody>'
    for f in spec['features']:body+='<tr><td>'+c['esc'](f)+'</td><td>'+c['esc'](PINS[f] if spec['history']=='Additional practice' else 'Follow exact source ownership below; generic practice allocations do not apply.')+'</td></tr>'
    body+='</tbody></table><ul>'+''.join('<li>'+c['esc'](r)+'</li>' for r in spec['resources'])+'</ul>'
    body+='<h2>State transitions and event sequence</h2><p>'+c['esc'](spec['states'])+'</p><h2>Setup values and timing</h2><p>'+c['esc'](spec['timing'])+'</p>'
    if spec['history']=='Additional practice':
        body+='<p>Illustrative practice values, not paper constants. Timer0 uses 10 ms. Timer1 uses 8000 samples/second: eight samples give a 1000 Hz base tone. RIT uses 10 ms. SysTick uses 10 ms alone or 100 ms as a separate supervisor. API configuration derives thresholds from the actual configured clock. SysTick must fit its 24-bit reload.</p><p>The foreground owns app. The primary sampling interrupt is RIT, otherwise SysTick, otherwise Timer0; without those, polling has no time guarantee. ADC priority is 2; audio Timer1 priority is 1; input edge IRQ priority is 3. Unused clocks are not initialized. A 31-entry FIFO preserves sampled command order; overflow drops the newest snapshot and increments lost_inputs. ADC processing is latest-completed-sample acquisition, not a lossless high-rate recorder.</p><h2>Why the code is arranged this way</h2><ul><li>stable_mask requires five consistent samples and produces one change per hold.</li><li>controller_step owns the state transitions; capture_inputs owns physical input reads.</li><li>The ADC interrupt stores completion; only the sampling path consumes it and requests the next conversion.</li><li>The main loop restores the saved interrupt mask after queue and audio-state updates.</li><li>stream_sample keeps output in 0–1023 and writes zero when paused.</li></ul>'
    body+='<h2>Inputs, expected results and boundaries</h2><p>'+c['esc'](spec['actions'])+'</p><p>Check initial state, press and release, simultaneous reset and action, held inputs, endpoints, restart, and delayed foreground processing. No physical-board result is claimed.</p>'
    for q in spec['questions']:body+='<p>'+link(c['PORTAL']/'exams'/(c['slug'](q)+'.html'),q+' — exact question and reviewed answer')+'</p>'
    if spec.get('paper'):body+='<p>'+link(c['ROOT']/spec['paper'],'Original paper')+'</p>'
    for note in spec.get('notes',[]):body+='<p>'+link(c['ROOT']/note,Path(note).stem.replace('_',' '))+'</p>'
    body+='<h2>Verification</h2><p>'+link(HERE/'SCENARIO_VALIDATION.json','Behavioral and structural results')+' · '+link(HERE/'SCENARIO_NATIVE_BUILDS.json','Native build results')+'. Reports identify tests actually run; simulation does not establish electrical or analog behavior.</p></section>'
    body+='<section class="section-block" data-runnable-pattern><h2>Complete replacement files</h2>'
    hashes={}
    for name in files:
        p=folder/name;hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
        body+=c['details_code'](name,p.read_text(encoding='utf-8'),p,dest,'Assembly' if p.suffix=='.s' else 'C',name.endswith('sample.c'))
    body+='</section><section class="section-block"><h2>Related references</h2><p>'+link(c['PORTAL']/'algorithms/index.html','Algorithms')+' · '+link(c['PORTAL']/'patterns/index.html','All peripheral combinations')+'</p>'
    for fn in sorted(set(re.findall(r'\b(exam_\w+)\(',spec['code']))):
        p=c['PORTAL']/'api'/(fn.replace('_','-')+'.html')
        if p.exists():body+=link(p,fn)+' '
    body+='</section>'
    c['write'](dest,c['page'](dest,spec['title'],spec['purpose'],body,[('Home',c['HOME']),('Solution Patterns',dest.parent/'index.html'),(spec['title'],dest)],'Solution Patterns'))
    return dict(id=key,title=spec['title'],route=c['rel'](dest,c['PORTAL']/'search.html'),path=folder.relative_to(ROOT).as_posix(),files=hashes,features=spec['features'],history=spec['history'],questions=spec['questions'],group=spec['group'],mode=spec.get('mode'),clock=spec.get('clock'),resources=spec['resources'],expected=spec['actions'],source=spec['source'],externalQuestion=spec.get('externalQuestion'))

def build_index(c,records,destinations):
    dest=c['PORTAL']/'patterns/index.html';esc=c['esc']
    body='<section class="section-block"><h2>Choose the peripherals that must work together</h2><p>Each selection requires all checked peripherals. Exact combinations have their own complete project. Larger combinations retain explicit roles for every selected component. Worked applications add behavior-specific solutions and clock/polling variants.</p><p>'+c['href'](dest.parent/'coverage.html',dest,'Inspect exam and combination coverage')+'</p></section>'
    body+='<section class="section-block" data-scenario-browser><fieldset><legend>Required peripherals</legend>'+''.join('<label style="display:inline-block;margin:0.5rem"><input type="checkbox" data-required-peripheral value="'+f+'"> '+f+'</label>' for f in FAMILIES)+'</fieldset><label>Find a behavior <input type="search" data-scenario-query placeholder="Reaction, hysteresis, waveform, binary entry"></label><label>Collection <select data-scenario-group><option value="">All collections</option><option>Past exams</option><option>Worked applications</option><option>Combinations</option></select></label><p data-scenario-count role="status"></p>'
    for group in ('Past exams','Worked applications','Combinations'):
        body+='<section data-scenario-section><h2>'+group+'</h2><div class="grid">'
        for r in records:
            if r['group']!=group:continue
            body+='<article class="card" data-scenario-card data-features="'+esc('|'.join(r['features']))+'" data-group="'+group+'"><h3>'+c['href'](c['PORTAL']/r['route'],dest,r['title'])+'</h3><p>'+esc(' + '.join(r['features']))+'</p><p>'+esc(r['expected'])+'</p></article>'
        body+='</div></section>'
    body+='</section><section class="section-block"><h2>Hardware techniques and existing variants</h2><ul>'
    for title,d in destinations.items():
        if d['section']=='Solution Patterns':body+='<li>'+c['href'](c['PORTAL']/d['route'],dest,title)+'</li>'
    body+='</ul></section><script src="../assets/scenarios.js" defer></script>'
    c['write'](dest,c['page'](dest,'Solution Patterns','Complete peripheral scenarios, exact exam mappings, and runnable combinations.',body,[('Home',c['HOME']),('Solution Patterns',dest)],'Solution Patterns'))

def finalize(c,items):
    moves,destinations=classify(c,items)
    from lcd_scenario import spec as lcd_spec
    specs={**practice_specs(),**historical_specs(c),'paper-lcd-maze':lcd_spec(c)}
    records=[]
    for key,spec in specs.items():
        record=render_scenario(c,key,spec);records.append(record)
        items.append(dict(id=key,kind='Solution Patterns',title=spec['title'],summary=spec['purpose'],route=record['route'],languages=['Both'] if spec.get('paper') else ['C'],components=spec['features'],topics=[spec['group']],aliases=spec['questions'],examHistory=spec['history'],relatedIds=[]))
    (HERE/'SCENARIO_MANIFEST.json').write_text(json.dumps(records,indent=2)+'\n')
    matrix=[]
    for n in range(2,9):
        for subset in combinations(FAMILIES,n):
            key='mix-'+'-'.join(x.lower() for x in subset)
            matrix.append(dict(features=subset,scenario=key,status='Complete project',qualification=specs[key]['timing']))
    (HERE/'PERIPHERAL_COMBINATIONS.json').write_text(json.dumps(matrix,indent=2)+'\n')
    for name in ('SCENARIO_VALIDATION.json','SCENARIO_NATIVE_BUILDS.json'):
        if not (HERE/name).exists():(HERE/name).write_text(json.dumps({'status':'NOT_RUN','reason':'Run the scenario verifier after generation.'},indent=2))
    # Rewrite all callers after courses/exams are generated; bookmarks themselves
    # remain compatibility pages. Classification applies to search metadata too.
    for path in c['PORTAL'].rglob('*.html'):
        text=path.read_text(encoding='utf-8');updated=rebase(text,path,path,moves)
        if updated!=text:c['write'](path,updated)
    build_index(c,records,destinations)
    c['write'](c['PORTAL']/'assets/scenarios.js',(HERE/'portal_ui/scenarios.js').read_text())
    dest=c['PORTAL']/'patterns/coverage.html'
    body='<section class="section-block"><h2>Combination inventory</h2><p>28 pairs, 56 triples, and 163 larger exact combinations: 247 complete configurations. Clock-only combinations expose separate counters in the debugger. DAC without Timer is a static output, not waveform playback.</p><p>'+c['href'](HERE/'PERIPHERAL_COMBINATIONS.json',dest,'Complete machine-readable matrix')+' · '+c['href'](HERE/'SCENARIO_MANIFEST.json',dest,'Projects, source hashes, evidence and resources')+'</p><h2>Historical question coverage</h2><ul>'
    for r in records:
        if r['questions'] or r.get('externalQuestion'):body+='<li>'+c['href'](c['PORTAL']/r['route'],dest,', '.join(r['questions'] or [r['externalQuestion']])+' — '+r['title'])+'</li>'
    body+='</ul><p>'+c['href'](HERE/'PAPER_INVENTORY.json',dest,'Supplied-paper audit, including sources outside the reviewed index')+'</p></section>'
    c['write'](dest,c['page'](dest,'Peripheral coverage','Exact combinations and question-to-project mappings.',body,[('Home',c['HOME']),('Solution Patterns',dest.parent/'index.html')],'Solution Patterns'))
    print('Separated sections and generated',len(records),'complete peripheral scenarios',flush=True)

def install(c):
    c['scenario_finalize']=lambda items:finalize(c,items)
