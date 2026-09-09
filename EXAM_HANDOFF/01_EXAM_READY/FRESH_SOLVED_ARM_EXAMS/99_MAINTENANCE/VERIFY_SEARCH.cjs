/* Exam retrieval, scoped parity, source identities, and relevance regressions. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const logic=require('./portal_ui/portal_logic.js');
const root=path.resolve(__dirname,'../../..'),base=path.join(root,'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS');
const box={window:{}};vm.runInNewContext(fs.readFileSync(path.join(base,'01_GUIDES_AND_INDEXES/PORTAL/assets/portal-data.js'),'utf8'),box);
const items=box.window.ARM_PORTAL_DATA.items,manifest=JSON.parse(fs.readFileSync(path.join(base,'03_COPY_PASTE_LIBRARY/CANONICAL_WORKSTATION/exam-solutions/manifest.json')));
let checks=0;const check=(value,message)=>{assert(value,message);checks++;};
const begin=performance.now(),engine=logic.prepare(items),prepareMs=performance.now()-begin;
const slug=s=>s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
check(new Set(items.map(i=>i.id)).size===items.length,'Unique corpus IDs');
check(items.filter(i=>i.id.startsWith('question-')).length===manifest.questions.length,'Question count');
for(const q of manifest.questions){
 const card=items.find(i=>i.id==='question-'+slug(q.questionId)),route=card.route;
 check(card.examId===q.examId,'Explicit exam relationship '+q.questionId);
 check(card.solutionRoutes.length===q.requiredFiles.length,'All answer files '+q.questionId);
 check(card.paperRoute.endsWith('.pdf'),'Original paper '+q.questionId);
 for(const f of q.functionsOrHandlers.split(/[;,]/).map(s=>s.trim()).filter(s=>/^\w+$/.test(s))){
   const found=engine.search(f,{kind:'Past Exams'});
   check(found.some(r=>r.item.route===route),'Function finds correct question '+q.questionId+' '+f);
   check(engine.scoped(f).has(route),'Scoped function recall '+q.questionId+' '+f);
 }
 for(const query of [q.date,q.date.replaceAll('-',''),new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(q.date))]){
   check(engine.search(query,{kind:'Past Exams'}).some(r=>r.item.route===route),'Date alias '+q.questionId+' '+query);
 }
}
for(const q of ['digitSum','digit sum','20230918','18 September 2023'])check(engine.scoped(q).has('exams/e2023-09-18.html'),'Past Exams search '+q);
check(engine.search('digitSum')[0].item.route==='exams/2023-09-18-q1.html','Exact function favors its question');
check(engine.search('20230918')[0].item.id==='exam-e2023-09-18','Compact date favors maintained exam');
check(engine.search('exam_timer_config_ms')[0].item.title==='exam_timer_config_ms','Exact API priority');
check(engine.search('Q1 Timer0')[0].item.contentRole!=='Supporting guidance','Warnings do not lead');
check(engine.search('Q1 Timer0')[0].item.route!=='exams/2023-02-07-q1.html#section-common-wrong-answers','Unrelated sort warning');
check(engine.search('Hofstadter')[0].item.contentRole!=='Filename only','Filename-only result does not lead');
check(engine.search('Hofstadter ARM1',{kind:'Past Exams'}).some(r=>r.item.examId==='E2026-02-18-A1'),'Variant search');
check(engine.search('surely_no_such_identifier_83918').length===0,'Unknown query');
check(engine.suggestions('debouce').includes('debounce'),'Explicit typo suggestion');
check(engine.search('interrupt handler').length===engine.search('ISR').length,'ISR synonym parity');
check(engine.search('20230918',{sourceClass:'Original',components:'Buttons',languages:'C'}).some(r=>r.item.paperRoute),'Original PDF retains filters');
check(engine.search('',{sourceClass:'Original'}).length>0,'Source-only filter exposes original material');
for(const filter of [{components:'Timer',languages:'C'},{year:'2026',question:'Q1'},{sourceClass:'Original'},{materialType:'Solution code'}]){
 const found=engine.search('Timer',filter);
 check(found.every(r=>logic.matchesFilters(r.item,filter)),'Filter parity '+JSON.stringify(filter));
 const scoped=engine.scoped('Timer',filter);
 for(const [route,results] of scoped)check(results.every(r=>found.some(f=>f.item.id===r.item.id)),'Scoped results subset '+route);
}
const duplicate=items.find(i=>(i.alternateSources||[]).some(a=>a.id&&a.sourceClass!==i.sourceClass));
check(!!duplicate,'Cross-source duplicate fixture');
const alt=duplicate.alternateSources.find(a=>a.id&&a.sourceClass!==duplicate.sourceClass);
check(engine.search(alt.title,{sourceClass:alt.sourceClass}).some(r=>r.item.route===alt.route),'Duplicate identity remains retrievable');
check(engine.search('may update C',{kind:'ASM Reference'}).some(r=>r.item.route==='asm/index.html#mov'),'ASM flag details indexed');
check(engine.scoped('may update C',{kind:'ASM Reference'}).has('asm/index.html#mov'),'ASM scoped full text');
const timings=[];
for(const query of ['digitSum','20230918','18 September 2023','Q1 Timer0','Hofstadter','exam_timer_config_ms','fifth argument','Timer0 ADC','graph shortest path','quicksort','LDRSB','short-circuit']){
 const samples=[];for(let i=0;i<5;i++){const t=performance.now();engine.search(query);samples.push(performance.now()-t);}timings.push({query,maxMs:Math.max(...samples),medianMs:samples.sort((a,b)=>a-b)[2]});
}
if(!timings.every(t=>t.maxMs<200))console.error(JSON.stringify(timings,null,2));
check(timings.every(t=>t.maxMs<200),'Search timing target 200 ms');
const report={checks,records:items.length,prepareMs,timings,status:'PASS'};
fs.writeFileSync(path.join(__dirname,'SEARCH_REGRESSION_RESULTS.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
