/* Search quality, bounded timings, and progress validation without browser services. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const {performance}=require('node:perf_hooks');
const logic=require('./portal_ui/portal_logic.js'),state=require('./portal_ui/workstation_state.js');
const base=path.resolve(__dirname,'../01_GUIDES_AND_INDEXES/PORTAL');
const box={window:{}};vm.runInNewContext(fs.readFileSync(path.join(base,'assets/portal-data.js'),'utf8'),box);
const items=JSON.parse(JSON.stringify(box.window.ARM_PORTAL_DATA.items));
let checks=0;function check(value,message){assert(value,message);checks++;}
const start=performance.now(),engine=logic.prepare(items),loadMs=performance.now()-start;
const queries=['Mastermind','fifth argument','Timer0 ADC','graph shortest path','quicksort','exam_timer_config_ms','exam_adc_take','stack alignment','interrupt handler','LDRSB','undefined symbol','collection destination','zero byte','confirmation_ms'];
const timings=[];
for(const query of queries){
  const samples=[];
  for(let i=0;i<5;i++){const t=performance.now();const found=engine.search(query);samples.push(performance.now()-t);check(found.length>0,'No result for '+query);}
  timings.push({query,maxMs:Math.max(...samples),medianMs:samples.sort((a,b)=>a-b)[2]});
}
check(engine.search('exam_timer_config_ms')[0].item.title==='exam_timer_config_ms','Exact API name must rank first');
check(engine.search('stack argument').some(r=>/fifth|stack/i.test(r.item.title+' '+r.item.heading)),'Stack/fifth synonym missing');
check(engine.search('interrupt handler').length===engine.search('ISR').length,'ISR synonym differs');
check(engine.suggestions('debouce').includes('debounce'),'Typo suggestion missing');
check(engine.search('surely_no_such_identifier_83918').length===0,'Unknown query matched');
check(engine.search('ADC',{sourceClass:'Original'}).every(r=>r.item.sourceClass==='Original'),'Original source filter leaks');
check(engine.search('Timer',{languages:'C'}).every(r=>logic.languageMatches(r.item.languages,'C')),'Language filter leaks');
check(items.some(i=>i.text&&i.text.includes('short-circuit')&&!String(i.summary).includes('short-circuit')),'Need body-only content');
check(engine.search('short-circuit').length>0,'Body-only term not searchable');
const e=state.empty();e.completed=['c-program'];e.exam.step=5;e.exam.checks=['prepare-0'];e.exam.fields={duration:'90',notes:'Attempt <one> & verify'};
const round=state.validate(JSON.parse(JSON.stringify(e)));
check(round.exam.step===5&&round.completed[0]==='c-program','Export/import round trip');
check(round.exam.fields.notes==='Attempt <one> & verify','Notes corrupted');
check(state.budget(90).submit===9,'Budget calculation');
check(state.budget('')===null,'Blank duration should not invent a budget');
for(const bad of [null,{version:2},{...e,exam:{...e.exam,step:99}},{...e,exam:{...e.exam,fields:{duration:'-1'}}}]){
  let threw=false;try{state.validate(bad);}catch(_){threw=true;}check(threw,'Malformed progress accepted');
}
const tests={checks,catalogSize:items.length,indexPreparationMs:loadMs,searchTimings:timings,within200ms:timings.every(x=>x.maxMs<200)};
fs.writeFileSync(path.join(__dirname,'WORKSTATION_CONTROLS_RESULTS.json'),JSON.stringify(tests,null,2));
console.log(JSON.stringify(tests,null,2));
check(tests.within200ms,'Search exceeded 200ms on this machine');
