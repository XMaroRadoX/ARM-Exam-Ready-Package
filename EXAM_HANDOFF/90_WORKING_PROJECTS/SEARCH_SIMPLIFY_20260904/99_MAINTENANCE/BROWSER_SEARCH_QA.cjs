/* Browser checks for scoped search and local-file portability. */
const path=require('node:path'),fs=require('node:fs'),assert=require('node:assert/strict'),{pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/marwa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../../..'),portal=path.join(root,'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL'),out=path.join(__dirname,'.search-qa');fs.mkdirSync(out,{recursive:true});
const url=(name,q='')=>pathToFileURL(path.join(portal,name)).href+q;
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 try {
 const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),errors=[],external=[];let checks=0;
 const check=(v,m)=>{assert(v,m);checks++;};page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(!/^(file|data|blob):/.test(r.url()))external.push(r.url());});
 const search=async(q)=>{await page.goto(url('search.html','?q='+encodeURIComponent(q)));await page.locator('.search-result').first().waitFor();};
 await search('digitSum');check((await page.locator('.search-result h3 a').first().getAttribute('href')).startsWith('exams/2023-09-18-q1.html'),'Global function result');
 await search('20230918');check((await page.locator('.search-result h3 a').first().getAttribute('href')).startsWith('exams/e2023-09-18.html'),'Compact date');
 await search('18 September 2023');await page.screenshot({path:path.join(out,'global-desktop.png')});
 await page.locator('[data-search-advanced]').evaluate(e=>e.open=true);await page.locator('[data-search-filter="sourceClass"]').selectOption('Original');
 await page.waitForFunction(()=>location.search.includes('sourceClass=Original'));
 check((await page.locator('.result-meta').allTextContents()).every(v=>v.startsWith('Original')),'Original filter');
 await page.goBack();check(await page.locator('[data-search-filter="sourceClass"]').inputValue()==='','Global Back restores filter');
 await page.goto(url('exams/index.html'));const input=page.locator('[data-filter="text"]');await input.fill('digitSum');
 await page.waitForFunction(()=>document.querySelector('[data-results-note]').textContent.startsWith('1 of'));
 check(await page.locator('[data-filter-item]:visible').count()===1,'Exam scope finds one reviewed exam');
 check((await page.locator('[data-filter-item]:visible [data-scope-match] a').getAttribute('href')).includes('2023-09-18-q1.html'),'Exam matched-question link');
 await input.press('Tab');check(page.url().includes('f-text=digitSum'),'Scoped URL state');
 check((await page.getByRole('link',{name:'Search whole package',exact:true}).getAttribute('href')).includes('q=digitSum'),'Whole-package query retained');
 await page.locator('[data-filter="year"]').selectOption('2026');check(await page.locator('[data-filter-item]:visible').count()===0,'Scoped combined filters');
 await page.goBack();await page.waitForFunction(()=>document.querySelector('[data-filter="year"]').value==='');
 check(await page.locator('[data-filter-item]:visible').count()===1,'Scoped Back restores results');
 await page.screenshot({path:path.join(out,'exams-desktop.png')});
 await page.goto(url('api/index.html'));const api=page.locator('[data-api-nav-search]');await api.fill('confirmation_ms');
 await page.waitForFunction(()=>document.querySelector('[data-api-nav-count]').textContent.match(/^[1-9]/));
 check(await page.locator('[data-api-entry]:visible').count()>0,'API searches documentation body');await api.press('Tab');check(page.url().includes('api-q=confirmation_ms'),'API URL state');
 await page.screenshot({path:path.join(out,'api-desktop.png')});
 for(const [name,query] of [['algorithms/index.html','quicksort'],['patterns/index.html','fifth argument']]){
   await page.goto(url(name));await page.locator('[data-filter="text"]').fill(query);
   await page.waitForFunction(()=>document.querySelector('[data-results-note]').textContent.match(/^[1-9]/));
   check(await page.locator('[data-filter-item]:visible [data-scope-match]:visible').count()>0,'Section body matching '+name);
 }
 await page.goto(url('asm/index.html'));await page.locator('#asm-filter').fill('may update C');
 await page.waitForFunction(()=>document.querySelector('#asm-count').textContent.match(/^[1-9]/));
 check(await page.locator('[data-asm-entry]:visible h3').allTextContents().then(a=>a.some(t=>t.includes('MOV'))),'ASM full-entry flag text');
 await page.locator('#asm-filter').press('Tab');check(page.url().includes('asm-q='),'ASM URL state');
 check((await page.getByRole('link',{name:'Search whole package',exact:true}).getAttribute('href')).includes('q=may+update+C'),'ASM whole-package link');
 await page.goto(url('exams/2023-02-07-q2.html'));check((await page.locator('[data-exam-search-metadata]').textContent()).includes('Timer IRQ'),'Visible interrupt tags');
 await page.screenshot({path:path.join(out,'question-topics-desktop.png')});
 await page.setViewportSize({width:390,height:844});
 for(const [name,query] of [['search.html','?q=18%20September%202023'],['exams/index.html','?f-text=digitSum'],['api/index.html','?api-q=confirmation_ms']]){
   await page.goto(url(name,query));await page.locator(name==='search.html'?'.search-result':name.startsWith('exams')?'[data-filter-item]:visible [data-scope-match]:visible':'[data-api-entry]:visible').first().waitFor();
   check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Narrow overflow '+name);
   await page.screenshot({path:path.join(out,'narrow-'+name.replaceAll('/','-')+'.png')});
 }
 await page.goto(url('search.html','?q=surely_no_such_identifier_83918'));await page.locator('.empty-state').waitFor();
 check(await page.locator('.empty-state').count()>0,'Empty results');
 check(errors.length===0,'Browser errors '+JSON.stringify(errors));check(external.length===0,'No external requests');
 const report={status:'PASS',checks,errors,externalRequests:external,screenshots:fs.readdirSync(out).filter(n=>n.endsWith('.png'))};fs.writeFileSync(path.join(__dirname,'SEARCH_BROWSER_RESULTS.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
