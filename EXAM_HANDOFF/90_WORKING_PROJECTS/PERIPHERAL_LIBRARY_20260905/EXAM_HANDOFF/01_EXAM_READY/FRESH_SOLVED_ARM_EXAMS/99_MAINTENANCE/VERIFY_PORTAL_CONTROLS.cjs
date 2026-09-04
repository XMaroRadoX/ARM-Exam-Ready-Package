/* Run with Node.js; no browser, package installation, or network is required. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ui = path.join(__dirname, 'portal_ui');
const logic = require(path.join(ui, 'portal_logic.js'));
let checks = 0;
function check(actual, expected, label) { assert.deepEqual(actual, expected, label); checks++; }

check(logic.languageMatches(['Both'], 'C'), true, 'C includes combined-language entries');
check(logic.languageMatches(['Both'], 'Assembly'), true, 'Assembly includes combined-language entries');
check(logic.languageMatches(['C', 'Assembly'], 'Both'), true, 'Explicit language arrays remain compatible');
check(logic.languageMatches(['C'], 'Both'), false, 'C alone is not Both');
check(logic.languageMatches(['Assembly'], 'C'), false, 'Assembly alone is not C');
check(logic.componentMatches(['Timer0', 'ADC'], 'Timer'), true, 'Timer includes numbered timers');
check(logic.componentMatches(['SysTick'], 'Timer'), false, 'SysTick remains its own category');
check(logic.componentMatches(['Multi-timer'], 'Timer'), true, 'Timer includes multi-timer lessons');
check(logic.componentMatches(['ADC IRQ'], 'ADC'), true, 'ADC includes ADC IRQ lessons');
check(logic.componentMatches(['EINT0'], 'Buttons'), true, 'Buttons includes EINT handlers');
check(logic.componentMatches(['Arithmetic'], 'RIT'), false, 'RIT is not a substring match on arithmetic');
const items = [
  {title:'Timer cookbook',summary:'Examples for exam_timer_config_ms',aliases:[],topics:[]},
  {title:'exam_timer_config_ms',summary:'Configure Timer0',aliases:[],topics:['Timer']},
  {title:'Stack arguments',summary:'Pass a fifth argument safely',aliases:['AAPCS'],topics:['Assembly']},
  {title:'Shortest path',summary:'Find a route',topics:['graph']}
];
check(items.map(item=>({item,rank:logic.score(item,'EXAM_TIMER_CONFIG_MS')})).filter(x=>x.rank).sort((a,b)=>b.rank-a.rank)[0].item.title,'exam_timer_config_ms','Exact API title ranks first');
check(items.filter(item=>logic.score(item,'fifth argument')).map(x=>x.title),['Stack arguments'],'Multiword search');
check(items.filter(item=>logic.score(item,'graph shortest path')).map(x=>x.title),['Shortest path'],'Terms across title and topics');
check(items.filter(item=>logic.score(item,'fifth missingword')).length,0,'All query words required');
check(logic.norm('  MÉMOIRE  '),'memoire','Case, accent, and whitespace normalization');

async function clipboardCase(mode) {
  const source='PUSH {R4, LR}\nPOP {R4, PC}\n';
  let listener, copied='', selected=false, focused=false;
  const status={textContent:''}, code={textContent:source};
  const pre={focus(){focused=true;},querySelector(){return code;}};
  const frame={querySelector(selector){return selector==='pre'?pre:status;}};
  const control={addEventListener(event,fn){listener=fn;},closest(){return frame;}};
  const document={readyState:'complete',addEventListener(){},querySelector(){return null;},
    querySelectorAll(selector){return selector==='.copy-code'?[control]:[];},
    createRange(){return {selectNodeContents(target){selected=target===code;}};}};
  const window={ARM_PORTAL_LOGIC:logic,addEventListener(){},getSelection(){return {removeAllRanges(){},addRange(){}};}};
  const navigator = mode==='missing' ? {} : {clipboard:{async writeText(text){if(mode==='denied')throw new Error('Denied');copied=text;}}};
  vm.runInNewContext(fs.readFileSync(path.join(ui,'portal.js'),'utf8'),{document,window,navigator});
  await listener();
  if(mode==='success') {check(copied,source,'Exact text copied');check(status.textContent,'Code copied.','Copy success announced');}
  else {check(selected&&focused,true,`${mode} clipboard selects source`);check(status.textContent.includes('Ctrl+C'),true,`${mode} clipboard gives manual instructions`);}
}
async function main() {
  await clipboardCase('success'); await clipboardCase('missing'); await clipboardCase('denied');
  for (const value of ['light','dark','invalid']) {
    const document={documentElement:{dataset:{},classList:{add(){}}}};
    vm.runInNewContext(fs.readFileSync(path.join(ui,'theme.js'),'utf8'),{document,localStorage:{getItem(){return value;}}});
    check(document.documentElement.dataset.theme, value==='invalid'?undefined:value, 'Only valid theme choices restored');
  }
  const document={documentElement:{dataset:{},classList:{add(){}}}};
  vm.runInNewContext(fs.readFileSync(path.join(ui,'theme.js'),'utf8'),{document,localStorage:{getItem(){throw new Error('Storage blocked');}}});
  check(document.documentElement.dataset.theme,undefined,'Storage denial retains system default');
  console.log(`Portal control regressions passed: ${checks} checks.`);
}
main().catch(error=>{console.error(error);process.exitCode=1;});
