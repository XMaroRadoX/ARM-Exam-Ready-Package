/* Real-browser QA against local file URLs in a disposable browser context. */
const {chromium}=require('C:/Users/marwa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'../../..'),portal=path.join(root,'01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PORTAL');
const out=path.join(__dirname,'.workstation-qa');fs.mkdirSync(out,{recursive:true});
const url=relative=>pathToFileURL(path.join(portal,relative)).href;
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 globalThis.qaBrowser=browser;
 const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
 const page=await context.newPage(),errors=[],external=[],timings=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(!/^(file|data|blob):/.test(r.url()))external.push(r.url());});
 let checks=0;const check=(v,m)=>{assert(v,m);checks++;};
 await page.goto(pathToFileURL(path.join(root,'START_HERE.html')).href);
 await page.getByRole('link',{name:'I’m in the exam — guide me',exact:true}).waitFor();
 await page.screenshot({path:path.join(out,'home-desktop.png')});
 for(const relative of ['courses/index.html','courses/c-pointers.html','in-exam/index.html','patterns/fifth-and-later-arguments.html']){
   await page.goto(url(relative));await page.locator('h1').waitFor();
   check(await page.locator('h1').count()===1,'One h1');
   check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Desktop overflow '+relative);
   await page.screenshot({path:path.join(out,relative.replaceAll('/','-')+'.png')});
 }
 await page.goto(url('courses/c-program.html'));
 await page.locator('[data-lesson-complete]').check();
 await page.reload();check(await page.locator('[data-lesson-complete]').isChecked(),'Lesson persists after reload');
 await page.goto(url('in-exam/index.html'));
 await page.locator('[data-exam-field="duration"]').fill('90');
 await page.locator('[data-exam-field="notes"]').fill('QA session: keep the timed version.');
 await page.locator('[data-exam-check="confirm-0"]').check();
 await page.locator('[data-exam-next]:visible').click();
 check(await page.locator('[data-exam-step="1"]').isVisible(),'Next step');
 check(!(await page.locator('[data-exam-sitting]').evaluate(el=>el.open)),'Sitting details collapse after setup');
 await page.screenshot({path:path.join(out,'in-exam-step-two.png')});
 for(const key of ['build','output','fault','interrupt','bounce','time']){
   await page.locator('#help-'+key+' summary').click();
   check(await page.locator('#help-'+key+' li').first().isVisible(),'Troubleshooting branch '+key);
   await page.locator('#help-'+key+' summary').click();
 }
 await page.locator('[data-go-step="7"]').click();
 check(await page.locator('[data-exam-step="7"]').isVisible(),'Free navigation to submission');
 await page.locator('[data-go-step="1"]').click();
 await page.reload();check(await page.locator('[data-exam-step="1"]').isVisible(),'Step persists');
 check(await page.locator('[data-exam-field="notes"]').inputValue()==='QA session: keep the timed version.','Notes persist');
 await page.locator('[data-exam-all]').click();
 check(await page.locator('[data-exam-step]:visible').count()===9,'Full checklist');
 page.once('dialog',d=>d.dismiss());
 await page.locator('[data-exam-reset]').click();
 check(await page.locator('[data-exam-field="notes"]').inputValue()!=='','Cancelled reset keeps notes');
 const downloadEvent=page.waitForEvent('download');
 await page.locator('[data-progress-export]').click();
 const download=await downloadEvent,progressFile=path.join(out,'progress.json');await download.saveAs(progressFile);
 check(JSON.parse(fs.readFileSync(progressFile,'utf8')).exam.fields.duration==='90','Export content');
 page.once('dialog',d=>d.accept());
 await page.locator('[data-exam-reset]').click();
 check(await page.locator('[data-exam-field="notes"]').inputValue()==='','Confirmed reset');
 page.once('dialog',d=>d.accept());
 await page.locator('[data-progress-import]').setInputFiles(progressFile);
 await page.waitForFunction(()=>document.querySelector('[data-exam-field="notes"]').value.includes('QA session'));
 check(await page.locator('[data-exam-field="duration"]').inputValue()==='90','Import restores fields');
 for(const query of ['exam_timer_config_ms','short-circuit','interrupt handler','Timer0 ADC','LDRSB']){
   await page.goto(url('search.html')+'?q='+encodeURIComponent(query));
   await page.locator('.best-matches .search-result').first().waitFor();
   timings.push({query,renderMs:Number(await page.locator('[data-global-search]').getAttribute('data-last-search-ms'))});
   check(await page.locator('.search-result').count()>0,'Results '+query);
 }
 await page.locator('[data-search-filter="sourceClass"]').selectOption('Original');
 await page.waitForFunction(()=>location.search.includes('sourceClass=Original'));
 check(await page.locator('.result-meta').allTextContents().then(a=>a.every(s=>s.startsWith('Original'))),'Source filter');
 await page.goBack();
 check(await page.locator('[data-search-filter="sourceClass"]').inputValue()==='','Back restores filter');
 await page.goto(url('search.html')+'?q=debouce');
 await page.getByRole('button',{name:'debounce',exact:true}).waitFor();
 await page.getByRole('button',{name:'debounce',exact:true}).click();
 check((await page.locator('[name=q]').inputValue())==='debounce','Explicit typo suggestion');
 await page.screenshot({path:path.join(out,'search-desktop.png')});
 await page.goto(url('courses/c-pointers.html'));
 await page.getByText('Hint 1',{exact:true}).click();
 check(await page.locator('.lesson-reveal').first().getAttribute('open')!==null,'Hint reveals');
 await page.keyboard.press('/');
 await page.waitForURL(/search\.html/);check(page.url().includes('search.html'),'Slash shortcut');
 for(const relative of ['courses/index.html','courses/c-pointers.html','in-exam/index.html','search.html?q=fifth%20argument']){
   await page.setViewportSize({width:390,height:844});
   const [file,query]=relative.split('?');await page.goto(url(file)+(query?'?'+query:''));
   await page.locator('h1').waitFor();
   check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Narrow overflow '+relative);
   await page.screenshot({path:path.join(out,'narrow-'+file.replaceAll('/','-')+'.png')});
 }
 // Denied storage and clipboard must not disable the guide or copying fallback.
 const denied=await browser.newContext({viewport:{width:1000,height:800}});
 await denied.addInitScript(()=>{
   Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage denied for QA');}});
   Object.defineProperty(navigator,'clipboard',{get(){return undefined;}});
 });
 const dp=await denied.newPage();dp.on('pageerror',e=>errors.push(e.message));
 await dp.goto(url('in-exam/index.html'));await dp.locator('[data-exam-next]:visible').click();
 check(await dp.locator('[data-exam-step="1"]').isVisible(),'Guide works without storage');
 await dp.goto(url('courses/c-pointers.html'));await dp.locator('.copy-code').first().click();
 check((await dp.locator('.copy-status').first().textContent()).includes('Ctrl+C'),'Clipboard fallback');
 const nojs=await browser.newContext({javaScriptEnabled:false});const np=await nojs.newPage();
 await np.goto(url('in-exam/index.html'));
 check(await np.locator('[data-exam-step]:visible').count()===9,'No-JS full checklist');
 await np.goto(url('courses/c-pointers.html'));await np.getByText('Reveal the worked answer',{exact:true}).click();
 check(await np.locator('details').filter({has:np.locator('summary',{hasText:'Reveal the worked answer'})}).getAttribute('open')!==null,'Native answer reveal without JS');
 check(errors.length===0,'Browser errors: '+errors.join('; '));check(external.length===0,'Unexpected network requests');
 check(timings.every(t=>t.renderMs<200),'Browser rendering exceeded 200 ms');
 const report={checks,errors,externalRequests:external,searchTimings:timings,screenshots:fs.readdirSync(out).filter(x=>x.endsWith('.png'))};
 fs.writeFileSync(path.join(__dirname,'WORKSTATION_BROWSER_RESULTS.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report,null,2));
 await browser.close();
})().catch(async error=>{console.error(error);if(globalThis.qaBrowser)await globalThis.qaBrowser.close();process.exitCode=1;});
